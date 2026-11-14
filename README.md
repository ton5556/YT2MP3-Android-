# YT2MP3 Android For My DAD

A lightweight YouTube to MP3 converter designed for Android devices. It runs locally through **Termux** and provides a simple, responsive web interface for converting and downloading audio.

Powered by Python, Flask, yt-dlp, and FFmpeg.

## Features

- **Simple Web Interface** – Convert YouTube videos through a mobile-friendly interface.
- **MP3 Conversion** – Extract audio and convert it to MP3 format at 192 kbps.
- **Real-time Progress** – Display download and conversion progress.
- **SD Card Support** – Save converted audio directly to your preferred storage location.
- **Automatic Cleanup** – Automatically delete temporary audio files after one hour.
- **Duration Limit** – Supports videos up to 90 minutes by default.
- **Light and Dark Mode** – Automatically follows your device's appearance settings.
- **One-Tap Launch** – Start the converter directly from your Android home screen using Termux:Widget.
- **No Cloud Server Required** – Processing runs locally on your Android device.

## Screenshots

<!-- Add your application screenshots here -->

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main application logic |
| Flask | Local web server and API |
| yt-dlp | YouTube video and audio extraction |
| FFmpeg | Audio conversion to MP3 |
| HTML / CSS / JavaScript | Web interface |
| Termux | Android execution environment |
| Termux:Widget | Home screen shortcuts |

## Requirements

- Android device
- Termux
- Termux:Widget
- Internet connection
- Storage permission

**Important:** Install both Termux and Termux:Widget from the same source, preferably F-Droid. Avoid mixing installations from different sources.

## Installation

### 1. Install Termux

Download and install:

- Termux
- Termux:Widget

### 2. Prepare storage

Open Termux and execute:

```bash
termux-setup-storage
```

Grant the requested storage permission.

### 3. Download the project

Download the repository ZIP and place it in your Android Download folder.

Extract the project:

```bash
pkg install -y unzip

unzip ~/storage/downloads/yt2mp3-android.zip -d ~
```

### 4. Install dependencies

Run the installation script:

```bash
bash ~/yt2mp3/setup.sh
```

The setup script automatically installs:

- Python
- FFmpeg
- Node.js
- Flask
- yt-dlp

It also creates the Termux home screen shortcuts.

### 5. Launch the application

Run:

```bash
bash ~/.shortcuts/YT2MP3
```

The local web interface will open in your browser:

```text
http://localhost:5000
```

## How to Use

1. Launch YT2MP3 from your Android home screen.
2. Open the web interface in Chrome.
3. Paste a valid YouTube URL.
4. Press **Convert to MP3**.
5. Wait for the conversion to complete.
6. Press **Download** to save the MP3 file.
7. Choose your preferred storage location or SD card.

## Home Screen Shortcuts

You can create shortcuts using Termux:Widget.

Available shortcuts:

| Shortcut | Function |
|---|---|
| YT2MP3 | Start the local server and open the web interface |
| YT2MP3-stop | Stop the server and release the wake lock |

## Configuration

The application supports environment variables:

| Variable | Default | Description |
|---|---|---|
| PORT | 5000 | Web server port |
| HOST | 0.0.0.0 | Server binding address |
| MAX_DURATION_MIN | 90 | Maximum video duration in minutes |

Example:

```bash
MAX_DURATION_MIN=120 HOST=127.0.0.1 python app.py
```

Note: The Android launcher explicitly binds the server to `127.0.0.1` so it is accessible only from the device itself.

## Troubleshooting

**YouTube extraction errors**

Update yt-dlp:

```bash
pip install -U yt-dlp
```

**Check application logs**

```bash
cat ~/yt2mp3.log
```

**Web interface does not open**

Try launching the application manually:

```bash
bash ~/.shortcuts/YT2MP3
```

**FFmpeg conversion errors**

Make sure FFmpeg is installed:

```bash
pkg install ffmpeg
```

## Project Structure

```text
yt2mp3/
│
├── app.py                 # Flask application and conversion logic
├── setup.sh               # Automatic Termux installation
├── requirements.txt       # Python dependencies
│
├── templates/
│   └── index.html         # Web interface
│
├── launcher/
│   ├── YT2MP3             # Start application shortcut
│   └── YT2MP3-stop        # Stop application shortcut
│
└── downloads/             # Temporary converted MP3 files
```

## Disclaimer

This project is intended for personal use and for converting content that you own or have permission to download.

Please respect copyright laws, YouTube's Terms of Service, and the rights of content creators.

The developer does not encourage unauthorized downloading or distribution of copyrighted material.

## License

No license has been specified yet. Please add a LICENSE file before publishing this project as open source.

---

**Built with Python and Termux for Android.**
