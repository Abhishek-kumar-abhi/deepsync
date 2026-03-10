# Setup Guide

## Quick Install

### Option 1: Terminal Mode Only (No Installation)
```bash
python agent.py
```
Works immediately - uses only Python standard library!

### Option 2: Full Features (Voice + GUI)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Windows users - PyAudio fix:**
   If `pyaudio` fails to install, download pre-built wheel:
   - Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
   - Download matching your Python version (e.g., `PyAudio-0.2.11-cp39-cp39-win_amd64.whl`)
   - Install: `pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl`

3. **For offline voice recognition (optional):**
   ```bash
   pip install pocketsphinx
   ```

4. **Run GUI:**
   ```bash
   python gui_app.py
   ```
   Or double-click `run_gui.bat`

## Troubleshooting

### Voice Recognition Not Working?
- Make sure microphone is connected and enabled
- Check Windows Privacy Settings → Microphone → Allow apps to access microphone
- Try: `pip install --upgrade SpeechRecognition pyaudio`

### GUI Not Starting?
- Verify Python has Tkinter: `python -m tkinter` (should open a window)
- On Linux, install: `sudo apt-get install python3-tk`
- On macOS, Tkinter comes with Python

### Text-to-Speech Not Working?
- Windows: Should work automatically
- Linux: Install `espeak`: `sudo apt-get install espeak espeak-data`
- macOS: Should work automatically

## Features Overview

| Feature | Requires Install | Works Offline |
|---------|-----------------|---------------|
| Terminal Mode | No | Yes |
| GUI Mode | No (Tkinter built-in) | Yes |
| Voice Input | Yes (SpeechRecognition) | Optional (pocketsphinx) |
| Voice Output | Yes (pyttsx3) | Yes |
