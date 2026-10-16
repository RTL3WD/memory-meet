MEET MEMORY — private meeting recorder + local Whisper transcription
=====================================================================

Runs entirely in Google Chrome locally. Nothing is uploaded: the page can only talk to
http://localhost, and the Whisper model (Small, English) runs from this project.

MODEL WEIGHTS
  The .onnx weight files are not in git (GitHub rejects files over 100 MB).
  If app/models/onnx-community/whisper-small.en/onnx/ has no .onnx files, download
  these from Hugging Face onnx-community/whisper-small.en and put them in that folder:
    encoder_model.onnx
    encoder_model_quantized.onnx
    decoder_model_merged_q4.onnx
    decoder_model_merged_quantized.onnx
  Tokenizer and config JSON are already included.

START
  Option A: double-click "Start Meet Memory.command"
            (if macOS blocks it: right-click > Open, or use option B)
  Option B: open Terminal in this folder and run:   python3 serve.py
  Chrome opens http://localhost:8765/ . Keep the Terminal window open while you use the app.
  To stop: press Ctrl+C in that window.

USE
  1. Click "Detect microphones", pick your mic.
  2. Click "Start recording". In Chrome's share picker choose Entire Screen (or the meeting tab)
     and turn on "Share system audio" / "Share tab audio". Only audio is saved, never video.
  3. Click "Stop & transcribe" (or Chrome's "Stop sharing"). Transcription starts automatically.
  4. Review, edit, copy, or download the recording and transcript. Past meetings are listed
     in the app and kept in this Chrome profile (IndexedDB) until you delete them.

NOTES
  - Use Chrome 141 or newer for system audio on macOS. Allow Chrome under System Settings >
    Privacy & Security > Screen & System Audio Recording and Microphone.
  - Recording continues while you use other apps, but keep this Chrome tab open until the
    transcript finishes. Closing it mid-recording is recoverable: the audio is saved every second
    and reappears the next time you open the app.
  - Transcription uses WebGPU when available and falls back to the CPU (slower) otherwise.
  - Use only where recording is authorized and everyone has consented.
  - Browser storage belongs to http://localhost:8765 — always start the app on the same port.
