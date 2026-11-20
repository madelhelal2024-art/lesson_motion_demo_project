# Lesson Motion Studio

A reusable educational video skill for whiteboard animation in Arabic or English

## Features

- Intake covering age or grade country learning goal duration language and landscape or portrait orientation
- Arial typography with Arabic RTL and English LTR
- Detailed whiteboard illustrations with progressive pen writing circles arrows and highlighting
- Age appropriate explanations and country sensitive examples
- Google AI Studio narration handoff: two copy-ready fields (Style of speech and Voiceover text), then scene timing aligned to the returned audio, plus a retrieval question with a thinking interval
- MP4 delivery and explicit quality checks

## Contents

The editable source of truth is in [`skills/lesson-motion-studio`](skills/lesson-motion-studio)
It includes `SKILL.md` references Arial fonts (user-supplied) plus audio segmentation timeline validation and encoding scripts

## Requirements

Use an assistant environment that supports skills image generation and local code execution
The user generates the narration in Google AI Studio and returns the audio file
The bundled scripts require Python Pillow ffmpeg and ffprobe
This is an assistant workflow with validation and encoding helpers rather than a standalone automatic video renderer
The host environment selects and implements the scene rendering tools

## Use

Load or install `skills/lesson-motion-studio` using the skill mechanism supported by your assistant
Then provide the lesson topic or screenshot and answer any missing intake questions
The assistant supplies a one-line Style of speech and the Voiceover text to paste into Google AI Studio; generate the audio there and return the WAV or MP3 file so the assistant can align and finish the MP4
Target scene timings stay inside the project and are estimates until the returned recording is measured
Do not treat unperformed listening or visual checks as passed

## Using it in Claude

- **claude.ai or the Claude app:** zip the `skills/lesson-motion-studio` folder (the zip must contain the `lesson-motion-studio` folder with `SKILL.md` inside) and upload it as a skill. Code execution must be on
- **Claude Code:** copy the folder to `~/.claude/skills/lesson-motion-studio` or use the updater below
- Claude has no built-in image generator, so the skill draws characters and objects in code as vector paths, which is also what the pen-drawing reveal needs
- Claude cannot listen to audio or watch video in real time. It measures the narration, finds sentence boundaries from pauses with `scripts/segment_audio.py`, and reviews exported frames. Watch and listen to each delivered video yourself before calling it final
- Arabic text is shaped with Pillow's raqm layout engine; the skill checks that it is available before rendering

## Edit and update

Edit files directly in `skills/lesson-motion-studio` using GitHub's file editor or clone this repository locally

```bash
git clone https://github.com/madelhelal2024-art/lesson_motion_demo_project.git
cd lesson-motion-studio
```

Commit source changes normally. Local Codex and Claude Code users can opt into the updater below; it checks GitHub's main branch once a day and updates their installed skill copy automatically.

```bash
# Run from this repository after cloning it.
python3 skills/lesson-motion-studio/scripts/auto_update.py install --install-dir ~/.codex/skills/lesson-motion-studio
# For Claude Code, use ~/.claude/skills/lesson-motion-studio instead.
```

On Windows, run the same script with `py -3` and pass a full destination such as `%USERPROFILE%\.codex\skills\lesson-motion-studio` or `%USERPROFILE%\.claude\skills\lesson-motion-studio`.

If a skill copy already exists, add `--replace` to the one-time install command. The updater saves the previous copy outside the active skills folder as a backup. It refuses later automatic updates if the installed files were edited locally. Use `check` for an immediate read-only version check, or `update` to apply a newer version immediately. Add `--no-daily` to install without the background schedule and run `enable-daily` later if wanted. Daily jobs run at 09:00 local time using launchd on macOS, Task Scheduler on Windows, or cron on Linux; the computer and scheduler must be available.

This updater manages local skill directories only. A skill uploaded directly to ChatGPT or Claude web is a separate copy and cannot be silently replaced by GitHub. Publish a new version through the platform's skill or plugin management flow. Claude shared skills propagate their owner's updates at next use; independently uploaded copies do not inherit those changes. New sessions may be needed to load changed local skill instructions.

The root `lesson-motion-studio.zip` is an optional original snapshot and is not automatically updated
Use the source folder for the current version
GitHub's Code → Download ZIP downloads the current repository including its source files

## Install the Arial fonts

The public repository intentionally excludes proprietary Arial binaries. Copy your licensed `ARIAL.TTF` and `ARIALBD.TTF` locally to `skills/lesson-motion-studio/assets/` as `Arial-Regular.ttf` and `Arial-Bold.ttf`. See [`FONT-NOTES.md`](skills/lesson-motion-studio/assets/FONT-NOTES.md). The timeline validator requires these files and checks that they are genuine Arial. An installation downloaded from GitHub is incomplete for rendering until the local fonts are supplied.

