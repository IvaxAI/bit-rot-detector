# Bit Rot Detector 🛡️

A cross-platform (Windows/macOS/Linux) video integrity checker.

## How it works
This tool uses **FFmpeg** to decode every frame of your video files. If it encounters a frame that cannot be decoded due to bit-flipping, corruption, or missing data, it marks the file as **Corrupt**.

## Requirements
1.  **Python 3.x**
2.  **FFmpeg** must be installed and added to your system's `PATH`.
    *   **macOS:** `brew install ffmpeg`
    *   **Windows:** [Download from ffmpeg.org](https://ffmpeg.org/download.html) and add to environment variables.

## How to use (CLI)
1.  Open your terminal or command prompt.
2.  Run the detector by passing the files you want to check:
    ```bash
    python detector.py "path/to/video1.mp4" "path/to/video2.mkv"
    ```
3.  **Drag and Drop:** On most systems, you can type `python detector.py ` and then drag multiple files into the terminal window—it will auto-fill the paths for you!

## Roadmap
- [x] Initialized `bit-rot-detector/detector.py` (CLI version).
- [x] Initialized `bit-rot-detector/gui.py` (GUI version).
- [ ] Add recursive folder scanning for Bit Rot Detector.
