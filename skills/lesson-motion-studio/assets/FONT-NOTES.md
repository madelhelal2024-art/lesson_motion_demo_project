# Arial font setup

This public repository does **not** redistribute Microsoft Arial font binaries. Obtain/use appropriately licensed Arial files on your own device. The project owner supplied two font files for local use.

Place these files inside this folder before producing or validating lessons:

- `Arial-Regular.ttf` — copy from `ARIAL.TTF`
- `Arial-Bold.ttf` — copy from `ARIALBD.TTF`

For Arabic set RTL text shaping with a suitable shaping engine (for Pillow, RAQM). Keep diacritics and joined Arabic glyphs intact. `scripts/validate_timeline.py` rejects substitute fonts. Do not publish or redistribute these files without appropriate permission.
