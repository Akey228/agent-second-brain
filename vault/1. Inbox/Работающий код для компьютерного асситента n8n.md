---
Created: 2026-01-26T20:10
References:
Tags:
  - info
Links:
  - "[[MOC - n8n Assistant]]"
  - "[[MOC - Patrick - digital assistant]]"
---
```
"""
Desktop Voice Recorder -> n8n webhook
File: desktop_voice_recorder.py

WHAT IT DOES
- Runs on Windows (Win10/11), listens for a global hotkey combo
  (Ctrl + Shift + Alt + Escape + L) held down.
- When the combo is pressed and held, the script starts recording from
  the selected microphone and writes audio to a temporary WAV file.
- When the combo is released, recording stops and the WAV file is uploaded
  to a configured n8n Webhook URL (multipart/form-data).
- No speech-to-text or voice reply is performed here — only audio file upload.

FEATURES
- Uses a streaming approach: audio is written to disk while recording,
  so long recordings (minutes) are possible without huge memory use.
- Includes a helper to list available audio devices so you can pick the right
  microhone index if the default isn't correct.
- Has basic error handling and logging to console.
- Autostart instructions included below (manual steps for Windows).

DEPENDENCIES (install in a venv or globally):
  pip install keyboard sounddevice soundfile requests

NOTES / WINDOWS PERMISSIONS
- The `keyboard` package may require running the script with
  Administrator privileges to capture global hotkeys on Windows.
  If your hotkey doesn't register, try running the script as admin.

USAGE
1) Edit the WEBHOOK_URL variable in the script and set your n8n webhook URL.
   Example: https://example.com/webhook/voice

2) (optional) Set DEVICE_INDEX to the index of your Fifine AM8 by running the
   program with --list-devices and choosing the index.

3) Start the script. Preferably run it once to ensure it sees your mic.

4) Press and HOLD Ctrl + Shift + Alt + Escape + L to start recording. When you
   release any of these keys the recording stops and is uploaded.

AUTOSTART (simple manual method)
- Create a shortcut to python.exe with argument path\to\desktop_voice_recorder.py
  and place the shortcut into the Windows Startup folder:
  %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

- Alternatively use Task Scheduler to run the script at login.

SECURITY
- The webhook URL is sent the file; make sure your n8n webhook is protected
  (use a secret path, HTTP auth, or other protections).

---

CODE STARTS HERE
"""

import argparse
import threading
import queue
import tempfile
import os
import sys
import time
import requests
import sounddevice as sd
import soundfile as sf
import keyboard

# === CONFIGURATION ===
WEBHOOK_URL = "https://andratozplay123.app.n8n.cloud/webhook/voice" 
SAMPLE_RATE = 16000  # common choice; change if you prefer 44100
CHANNELS = 1
SUBTYPE = 'PCM_16'  # wav format
CHUNK_SIZE = 1024
DEVICE_INDEX = 1  # None = default; set to integer device index if needed
UPLOAD_FIELD_NAME = 'file'  # name of form field in multipart

# Keys that must be simultaneously pressed to record (user requested combo):
HOTKEY_KEYS = ['ctrl', 'shift', 'alt', 'l']

# Internal state
is_recording = False
_recording_lock = threading.Lock()
_audio_queue = queue.Queue()
_current_wav_path = None
_stream = None
_writer = None


def list_audio_devices():
    print("Available audio devices:")
    for i, dev in enumerate(sd.query_devices()):
        print(f"{i}: {dev['name']} (inputs: {dev['max_input_channels']})")


def audio_callback(indata, frames, time_info, status):
    """Callback called by sounddevice.InputStream for each audio block."""
    if status:
        print("Audio status:", status, file=sys.stderr)
    # Write raw frames to queue to be written to file by the writer thread
    _audio_queue.put(indata.copy())


def writer_thread_func(wav_path, samplerate, channels):
    """Thread that writes audio frames from queue to wav file using soundfile."""
    global _writer
    try:
        with sf.SoundFile(wav_path, mode='w', samplerate=samplerate,
                          channels=channels, subtype=SUBTYPE) as f:
            _writer = f
            print(f"Writing audio to: {wav_path}")
            while True:
                try:
                    block = _audio_queue.get(timeout=0.5)
                except queue.Empty:
                    # if recording stopped and queue empty, break
                    if not is_recording and _audio_queue.empty():
                        break
                    else:
                        continue
                f.write(block)
    except Exception as e:
        print("Writer thread error:", e)
    finally:
        _writer = None
        print("Writer thread ended")


def start_recording():
    """Start the input stream and the writer thread."""
    global is_recording, _stream, _current_wav_path
    with _recording_lock:
        if is_recording:
            return
        is_recording = True
        # create temp wav file path
        fd, path = tempfile.mkstemp(prefix='voice_rec_', suffix='.wav')
        os.close(fd)
        _current_wav_path = path
        # start writer thread
        t = threading.Thread(target=writer_thread_func, args=(path, SAMPLE_RATE, CHANNELS), daemon=True)
        t.start()
        # open input stream
        try:
            _stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS,
                                     callback=audio_callback, blocksize=CHUNK_SIZE,
                                     device=DEVICE_INDEX)
            _stream.start()
            print("Recording started... (release hotkey to stop)")
        except Exception as e:
            print("Failed to start input stream:", e)
            is_recording = False


def stop_recording_and_upload():
    """Stop stream, wait for writer to flush queue, then upload file."""
    global is_recording, _stream, _current_wav_path
    with _recording_lock:
        if not is_recording:
            return
        is_recording = False
        # stop stream
        try:
            if _stream is not None:
                _stream.stop()
                _stream.close()
        except Exception as e:
            print("Error stopping stream:", e)
        # wait for queue to drain
        print("Finishing write...")
        time.sleep(0.6)
        # upload
        if _current_wav_path and os.path.exists(_current_wav_path):
            try:
                print(f"Uploading {_current_wav_path} to {WEBHOOK_URL} ...")
                with open(_current_wav_path, 'rb') as f:
                    files = {UPLOAD_FIELD_NAME: (os.path.basename(_current_wav_path), f, 'audio/wav')}
                    resp = requests.post(WEBHOOK_URL, files=files, timeout=60)
                if resp.ok:
                    print("Upload success (status code:", resp.status_code, ")")
                else:
                    print("Upload failed (status code:", resp.status_code, ")", resp.text)
            except Exception as e:
                print("Upload exception:", e)
            finally:
                try:
                    os.remove(_current_wav_path)
                except Exception:
                    pass
                _current_wav_path = None
        else:
            print("No audio file to upload.")


def check_hotkey_and_update(event):
    """This function is called for every keyboard event; it checks whether
    the full hotkey combination is pressed. When all keys are down -> start
    recording. When any key released (so combo not pressed) -> stop and upload.
    """
    # We examine current pressed keys using keyboard.is_pressed
    try:
        all_pressed = all(keyboard.is_pressed(k) for k in HOTKEY_KEYS)
    except Exception:
        # keyboard.is_pressed may raise if run without admin privileges for some keys
        all_pressed = False

    if all_pressed and not is_recording:
        start_recording()
    if (not all_pressed) and is_recording:
        # stop recording
        stop_recording_and_upload()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list-devices', action='store_true', help='List audio devices and exit')
    parser.add_argument('--webhook', type=str, help='Override webhook url')
    args = parser.parse_args()

    global WEBHOOK_URL, DEVICE_INDEX
    if args.webhook:
        WEBHOOK_URL = args.webhook

    if args.list_devices:
        list_audio_devices()
        return

    if WEBHOOK_URL == "https://YOUR_N8N_WEBHOOK_HERE":
        print("Please set your WEBHOOK_URL variable in the script or run with --webhook <url>")
        return

    print("Desktop Voice Recorder for n8n starting...")
    print("Hotkey combo:", ' + '.join(HOTKEY_KEYS))
    print("Press and HOLD the combo to record, release to stop and upload.")

    # register a lightweight hook: we do not bind to a single key event but
    # hook global events and check current pressed state
    keyboard.hook(check_hotkey_and_update)

    try:
        print("Running. Press Ctrl+C in console to exit.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        # if recording when exiting, finalize
        if is_recording:
            stop_recording_and_upload()


if __name__ == '__main__':
    main()

```
#### Linked References to "Работающий код для компьютерного асситента n8n"
```dataview
list from [[Работающий код для компьютерного асситента n8n]]
```