# AshuFlow

A modern Windows application for downloading media content from YouTube, Instagram, and Spotify.

## Features

- **YouTube Downloads** - Videos, playlists, shorts, and audio extraction
- **Instagram Downloads** - Posts, reels, stories, and profile pictures
- **Spotify Downloads** - Tracks, albums, and playlists
- **Quality Options** - Choose from 360p to 1080p, or best available
- **Format Selection** - MP4, MKV, WebM, MP3, M4A, FLAC, and more
- **Modern UI** - Clean dark-themed interface

## Download

### Option 1: Clone the Repository
```bash
git clone https://github.com/r34sd/AshuFlow.git
cd AshuFlow
```

### Option 2: Download ZIP
1. Go to https://github.com/r34sd/AshuFlow
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract to your preferred location

## Setup on Windows

### Automatic Setup (Recommended)
1. Double-click `setup.bat`
2. The script will automatically:
   - Install Python if not present
   - Install all required packages
   - Create a desktop shortcut
3. Click "Y" when asked to launch the app

### Manual Setup
1. Install Python 3.10+ from https://python.org (check "Add to PATH")
2. Open Command Prompt in the AshuFlow folder
3. Run:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch with:
   ```bash
   python ashuflow.py
   ```

## How to Use

### Downloading from YouTube
1. Open AshuFlow
2. Go to the **YouTube** tab
3. Paste the video/playlist URL
4. Select quality (best, 1080p, 720p, etc.)
5. Select format (mp4, mkv, mp3 for audio)
6. Click **Download**

### Downloading from Instagram
1. Go to the **Instagram** tab
2. Paste the post/reel/story URL
3. Click **Download**

### Downloading from Spotify
1. Go to the **Spotify** tab
2. Paste the track/album/playlist URL
3. Select audio format (mp3, flac, m4a)
4. Select bitrate (128k - 320k)
5. Click **Download**

### Changing Download Location
- Click **Browse** to select a custom folder
- Click **Open Folder** to view downloaded files
- Default location: `Downloads/AshuFlow`

## Requirements

- Windows 10/11
- Python 3.10 or higher
- Internet connection

## Files

| File | Description |
|------|-------------|
| `ashuflow.py` | Main application |
| `setup.bat` | Automatic installer |
| `AshuFlow.bat` | Quick launcher |
| `install.py` | Python dependency installer |
| `requirements.txt` | Package list |

## Troubleshooting

**App won't start?**
- Run `setup.bat` again to reinstall dependencies

**Download fails?**
- Update yt-dlp: `pip install -U yt-dlp`
- Check if the URL is valid and accessible

**FFmpeg errors?**
- Delete the `ffmpeg` folder and restart the app
- FFmpeg will be re-downloaded automatically

## License

MIT License - Free to use and modify.
