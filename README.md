# Kali Lab Terminal v2

A Kali-inspired desktop terminal emulator with:

- GUI tabs
- command history (Up/Down)
- Tab autocomplete
- selectable themes
- simulated filesystem
- built-in simulated cyber lab
- simulated network/scan output

## Run

Python 3.10+ is recommended.

```bash
python kali_lab_terminal.py
```

On Linux, Tkinter may need to be installed separately (for example, the `python3-tk` package).

## Lab commands

```text
lab status
lab hosts
lab scan 10.10.10.0/24
```

The lab is intentionally simulated: it does not send network packets or perform real scans.

#kalrav723
