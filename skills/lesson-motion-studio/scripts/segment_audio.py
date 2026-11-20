"""Find speech segments in a narration file from its pauses (ffmpeg silencedetect).

Use when no speech-to-text model is available. Output is a measured starting point
for timeline.json, not proof of what was said: confirm segment-to-sentence matching
with the user or a transcript before treating it as synchronised.
"""
import argparse, json, re, subprocess
from pathlib import Path


def duration(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                          '-of', 'csv=p=0', str(path)], text=True))


def silences(path, noise_db, min_silence):
    log = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af',
                          f'silencedetect=noise={noise_db}dB:d={min_silence}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', log)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def segments(path, noise_db=-35, min_silence=0.35, expected=None):
    total = duration(path)
    gaps = [(max(0.0, s), total if e is None else e) for s, e in silences(path, noise_db, min_silence)]
    speech, cursor = [], 0.0
    for s, e in gaps:
        if s - cursor > 0.05:
            speech.append({'start': round(cursor, 3), 'end': round(s, 3)})
        cursor = e
    if total - cursor > 0.05:
        speech.append({'start': round(cursor, 3), 'end': round(total, 3)})
    if expected and len(speech) > expected:
        # Merge across the shortest pauses until the count matches the script.
        while len(speech) > expected:
            i = min(range(len(speech) - 1), key=lambda k: speech[k + 1]['start'] - speech[k]['end'])
            speech[i] = {'start': speech[i]['start'], 'end': speech[i + 1]['end']}
            del speech[i + 1]
    for i, seg in enumerate(speech):
        seg['index'] = i
        seg['pause_after'] = round((speech[i + 1]['start'] if i + 1 < len(speech) else total) - seg['end'], 3)
    return {'audio': str(path), 'duration': round(total, 3), 'noise_db': noise_db,
            'min_silence': min_silence, 'segments': speech,
            'note': 'Pause-based estimate; confirm sentence mapping before final sync'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('audio', type=Path)
    p.add_argument('--noise-db', type=float, default=-35)
    p.add_argument('--min-silence', type=float, default=0.35)
    p.add_argument('--expected', type=int, help='number of script sentences or segments')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    result = segments(a.audio, a.noise_db, a.min_silence, a.expected)
    if a.expected and len(result['segments']) < a.expected:
        result['warning'] = (f"Found {len(result['segments'])} segments, expected {a.expected}; "
                             'lower --min-silence or --noise-db, or align manually')
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if a.output:
        a.output.write_text(text)
    print(text)
