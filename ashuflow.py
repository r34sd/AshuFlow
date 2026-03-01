"""
AshuFlow - YouTube, Instagram & Spotify Downloader
A modern Windows application for downloading media content.
Fully automatic - no manual installations required!
"""

import subprocess
import sys
import os
import threading
import zipfile
import shutil
import urllib.request
from pathlib import Path

# App directory for storing dependencies
APP_DIR = Path(__file__).parent.absolute()
FFMPEG_DIR = APP_DIR / "ffmpeg"
FFMPEG_EXE = FFMPEG_DIR / "ffmpeg.exe"


def install_package(package):
    """Install a Python package using pip."""
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-U", package, "-q"],
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )


def update_yt_dlp():
    """Update yt-dlp to the latest version for best compatibility."""
    try:
        print("Updating yt-dlp to latest version...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp", "-q"],
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
    except Exception as e:
        print(f"yt-dlp update warning: {e}")


def check_and_install_dependencies():
    """Check and install all required Python packages."""
    required_packages = {
        "customtkinter": "customtkinter",
        "PIL": "pillow",
        "yt_dlp": "yt-dlp",
        "requests": "requests",
    }

    # First ensure pip is available
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
    except:
        print("Installing pip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])

    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            print(f"Installing {package}...")
            install_package(package)


def download_ffmpeg():
    """Download FFmpeg if not present."""
    if FFMPEG_EXE.exists():
        return str(FFMPEG_DIR)

    print("Downloading FFmpeg (one-time setup)...")

    # FFmpeg download URL (Windows build)
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = APP_DIR / "ffmpeg_temp.zip"

    try:
        # Download with progress
        urllib.request.urlretrieve(ffmpeg_url, zip_path)

        print("Extracting FFmpeg...")

        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(APP_DIR / "ffmpeg_temp")

        # Find and move ffmpeg binaries
        FFMPEG_DIR.mkdir(exist_ok=True)

        # Find the extracted folder
        temp_dir = APP_DIR / "ffmpeg_temp"
        for item in temp_dir.iterdir():
            if item.is_dir() and "ffmpeg" in item.name.lower():
                bin_dir = item / "bin"
                if bin_dir.exists():
                    for exe in bin_dir.glob("*.exe"):
                        shutil.copy(exe, FFMPEG_DIR)
                break

        # Cleanup
        zip_path.unlink(missing_ok=True)
        shutil.rmtree(temp_dir, ignore_errors=True)

        print("FFmpeg installed successfully!")
        return str(FFMPEG_DIR)

    except Exception as e:
        print(f"FFmpeg download failed: {e}")
        print("Some features may not work without FFmpeg.")
        return None


def download_spotdl():
    """Ensure spotdl is installed."""
    try:
        import spotdl
    except ImportError:
        print("Installing spotdl...")
        install_package("spotdl")


# Run initial setup before importing GUI libraries
print("=" * 50)
print("  AshuFlow - Media Downloader")
print("  Checking dependencies...")
print("=" * 50)

check_and_install_dependencies()
update_yt_dlp()  # Always update yt-dlp for best compatibility
ffmpeg_path = download_ffmpeg()
download_spotdl()

print("Setup complete! Starting application...\n")

# Now import the GUI libraries (after they're installed)
import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AshuFlow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Store FFmpeg path
        self.ffmpeg_path = ffmpeg_path

        # Configure window
        self.title("AshuFlow - Media Downloader")
        self.geometry("800x600")
        self.minsize(700, 500)

        # Default download path
        self.download_path = str(Path.home() / "Downloads" / "AshuFlow")
        os.makedirs(self.download_path, exist_ok=True)

        # Create main layout
        self.create_widgets()

    def create_widgets(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, height=80, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="AshuFlow",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=20)

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="YouTube | Instagram | Spotify Downloader",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 10))

        # Tab view for different platforms
        self.tabview = ctk.CTkTabview(self.main_frame, width=750, height=400)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Create tabs
        self.tab_youtube = self.tabview.add("YouTube")
        self.tab_instagram = self.tabview.add("Instagram")
        self.tab_spotify = self.tabview.add("Spotify")

        # Setup each tab
        self.setup_youtube_tab()
        self.setup_instagram_tab()
        self.setup_spotify_tab()

        # Download path section
        self.path_frame = ctk.CTkFrame(self.main_frame)
        self.path_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.path_label = ctk.CTkLabel(self.path_frame, text="Download Location:")
        self.path_label.pack(side="left", padx=10)

        self.path_entry = ctk.CTkEntry(self.path_frame, width=400)
        self.path_entry.pack(side="left", padx=5)
        self.path_entry.insert(0, self.download_path)

        self.browse_btn = ctk.CTkButton(
            self.path_frame,
            text="Browse",
            width=80,
            command=self.browse_folder
        )
        self.browse_btn.pack(side="left", padx=5)

        self.open_folder_btn = ctk.CTkButton(
            self.path_frame,
            text="Open Folder",
            width=100,
            command=self.open_download_folder
        )
        self.open_folder_btn.pack(side="left", padx=5)

        # Status bar
        self.status_frame = ctk.CTkFrame(self.main_frame, height=30)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=760)
        self.progress_bar.pack(padx=20, pady=(0, 20))
        self.progress_bar.set(0)

    def setup_youtube_tab(self):
        # YouTube URL input
        url_frame = ctk.CTkFrame(self.tab_youtube, fg_color="transparent")
        url_frame.pack(fill="x", padx=20, pady=20)

        url_label = ctk.CTkLabel(url_frame, text="YouTube URL:", font=ctk.CTkFont(size=14))
        url_label.pack(anchor="w")

        self.yt_url_entry = ctk.CTkEntry(url_frame, width=600, height=40, placeholder_text="Paste YouTube video or playlist URL here...")
        self.yt_url_entry.pack(fill="x", pady=(5, 10))

        # Options frame
        options_frame = ctk.CTkFrame(self.tab_youtube, fg_color="transparent")
        options_frame.pack(fill="x", padx=20)

        # Quality selection
        quality_label = ctk.CTkLabel(options_frame, text="Quality:")
        quality_label.pack(side="left", padx=(0, 10))

        self.yt_quality_var = ctk.StringVar(value="best")
        self.yt_quality_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["best", "1080p", "720p", "480p", "360p", "audio only"],
            variable=self.yt_quality_var,
            width=120
        )
        self.yt_quality_menu.pack(side="left", padx=5)

        # Format selection
        format_label = ctk.CTkLabel(options_frame, text="Format:")
        format_label.pack(side="left", padx=(20, 10))

        self.yt_format_var = ctk.StringVar(value="mp4")
        self.yt_format_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["mp4", "mkv", "webm", "mp3", "m4a"],
            variable=self.yt_format_var,
            width=100
        )
        self.yt_format_menu.pack(side="left", padx=5)

        # Download button
        self.yt_download_btn = ctk.CTkButton(
            self.tab_youtube,
            text="Download",
            width=200,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.download_youtube
        )
        self.yt_download_btn.pack(pady=30)

        # Info text
        info_label = ctk.CTkLabel(
            self.tab_youtube,
            text="Supports: Videos, Playlists, Shorts, Live streams",
            text_color="gray"
        )
        info_label.pack()

    def setup_instagram_tab(self):
        # Instagram URL input
        url_frame = ctk.CTkFrame(self.tab_instagram, fg_color="transparent")
        url_frame.pack(fill="x", padx=20, pady=20)

        url_label = ctk.CTkLabel(url_frame, text="Instagram URL:", font=ctk.CTkFont(size=14))
        url_label.pack(anchor="w")

        self.ig_url_entry = ctk.CTkEntry(url_frame, width=600, height=40, placeholder_text="Paste Instagram post, reel, or story URL here...")
        self.ig_url_entry.pack(fill="x", pady=(5, 10))

        # Options frame
        options_frame = ctk.CTkFrame(self.tab_instagram, fg_color="transparent")
        options_frame.pack(fill="x", padx=20)

        # Content type
        self.ig_type_var = ctk.StringVar(value="post")
        type_label = ctk.CTkLabel(options_frame, text="Content Type:")
        type_label.pack(side="left", padx=(0, 10))

        self.ig_type_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["post", "reel", "story", "profile"],
            variable=self.ig_type_var,
            width=120
        )
        self.ig_type_menu.pack(side="left", padx=5)

        # Download button
        self.ig_download_btn = ctk.CTkButton(
            self.tab_instagram,
            text="Download",
            width=200,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.download_instagram
        )
        self.ig_download_btn.pack(pady=30)

        # Info text
        info_label = ctk.CTkLabel(
            self.tab_instagram,
            text="Supports: Posts, Reels, Stories, Profile pictures",
            text_color="gray"
        )
        info_label.pack()

    def setup_spotify_tab(self):
        # Spotify URL input
        url_frame = ctk.CTkFrame(self.tab_spotify, fg_color="transparent")
        url_frame.pack(fill="x", padx=20, pady=20)

        url_label = ctk.CTkLabel(url_frame, text="Spotify URL:", font=ctk.CTkFont(size=14))
        url_label.pack(anchor="w")

        self.sp_url_entry = ctk.CTkEntry(url_frame, width=600, height=40, placeholder_text="Paste Spotify track, album, or playlist URL here...")
        self.sp_url_entry.pack(fill="x", pady=(5, 10))

        # Options frame
        options_frame = ctk.CTkFrame(self.tab_spotify, fg_color="transparent")
        options_frame.pack(fill="x", padx=20)

        # Audio format
        format_label = ctk.CTkLabel(options_frame, text="Audio Format:")
        format_label.pack(side="left", padx=(0, 10))

        self.sp_format_var = ctk.StringVar(value="mp3")
        self.sp_format_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["mp3", "m4a", "flac", "opus", "ogg"],
            variable=self.sp_format_var,
            width=100
        )
        self.sp_format_menu.pack(side="left", padx=5)

        # Bitrate
        bitrate_label = ctk.CTkLabel(options_frame, text="Bitrate:")
        bitrate_label.pack(side="left", padx=(20, 10))

        self.sp_bitrate_var = ctk.StringVar(value="320k")
        self.sp_bitrate_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["128k", "192k", "256k", "320k"],
            variable=self.sp_bitrate_var,
            width=100
        )
        self.sp_bitrate_menu.pack(side="left", padx=5)

        # Download button
        self.sp_download_btn = ctk.CTkButton(
            self.tab_spotify,
            text="Download",
            width=200,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.download_spotify
        )
        self.sp_download_btn.pack(pady=30)

        # Info text
        info_label = ctk.CTkLabel(
            self.tab_spotify,
            text="Supports: Tracks, Albums, Playlists, Artist top tracks",
            text_color="gray"
        )
        info_label.pack()

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def open_download_folder(self):
        path = self.path_entry.get()
        if os.path.exists(path):
            os.startfile(path)
        else:
            os.makedirs(path, exist_ok=True)
            os.startfile(path)

    def update_status(self, message):
        self.status_label.configure(text=message)
        self.update_idletasks()

    def set_progress(self, value):
        self.progress_bar.set(value)
        self.update_idletasks()

    def progress_hook(self, d):
        """Progress hook for yt-dlp."""
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    progress = downloaded / total
                    self.after(0, lambda p=progress: self.set_progress(p))
                    percent = int(progress * 100)
                    self.after(0, lambda p=percent: self.update_status(f"Downloading... {p}%"))
            except:
                pass
        elif d['status'] == 'finished':
            self.after(0, lambda: self.update_status("Processing..."))
            self.after(0, lambda: self.set_progress(0.95))

    def download_youtube(self):
        url = self.yt_url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL!")
            return

        quality = self.yt_quality_var.get()
        format_type = self.yt_format_var.get()
        output_path = self.path_entry.get()

        # Disable button during download
        self.yt_download_btn.configure(state="disabled")
        self.update_status("Starting YouTube download...")
        self.set_progress(0)

        def download_thread():
            try:
                # Build yt-dlp options
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                    'retries': 3,
                    'fragment_retries': 3,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    },
                    'socket_timeout': 30,
                }

                # Add FFmpeg location
                if self.ffmpeg_path and os.path.exists(self.ffmpeg_path):
                    ydl_opts['ffmpeg_location'] = self.ffmpeg_path

                # Check for cookies file
                cookies_file = APP_DIR / "cookies.txt"
                if cookies_file.exists():
                    ydl_opts['cookiefile'] = str(cookies_file)

                # Set format based on quality and format type
                if format_type in ["mp3", "m4a"] or quality == "audio only":
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3' if format_type == "mp3" or quality == "audio only" else format_type,
                        'preferredquality': '192',
                    }]
                else:
                    # Use more flexible format selection that falls back gracefully
                    if quality == "best":
                        ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    else:
                        height = quality.replace("p", "")
                        ydl_opts['format'] = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'

                    # Always merge to the selected format
                    ydl_opts['merge_output_format'] = format_type

                self.after(0, lambda: self.update_status("Connecting..."))

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                self.after(0, lambda: self.set_progress(1))
                self.after(0, lambda: self.update_status("Download completed!"))
                self.after(0, lambda: messagebox.showinfo("Success", "YouTube download completed!"))

            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)[:300]
                self.after(0, lambda: self.update_status("Download failed!"))
                self.after(0, lambda m=error_msg: messagebox.showerror("Error", f"Download failed:\n{m}"))
            except Exception as e:
                error_msg = str(e)[:300]
                self.after(0, lambda: self.update_status("Error occurred!"))
                self.after(0, lambda m=error_msg: messagebox.showerror("Error", f"Error:\n{m}"))
            finally:
                self.after(0, lambda: self.yt_download_btn.configure(state="normal"))
                self.after(0, lambda: self.set_progress(0))

        threading.Thread(target=download_thread, daemon=True).start()

    def download_instagram(self):
        url = self.ig_url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter an Instagram URL!")
            return

        output_path = self.path_entry.get()

        # Disable button during download
        self.ig_download_btn.configure(state="disabled")
        self.update_status("Starting Instagram download...")
        self.set_progress(0)

        def download_thread():
            try:
                # Build yt-dlp options for Instagram
                ydl_opts = {
                    'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                    'retries': 3,
                    'fragment_retries': 3,
                    'socket_timeout': 30,
                    'extractor_args': {'instagram': {'skip': ['dash']}},
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    },
                }

                # Add FFmpeg location
                if self.ffmpeg_path and os.path.exists(self.ffmpeg_path):
                    ydl_opts['ffmpeg_location'] = self.ffmpeg_path

                # Check for cookies file for authenticated content
                cookies_file = APP_DIR / "cookies.txt"
                if cookies_file.exists():
                    ydl_opts['cookiefile'] = str(cookies_file)

                self.after(0, lambda: self.update_status("Connecting to Instagram..."))

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                self.after(0, lambda: self.set_progress(1))
                self.after(0, lambda: self.update_status("Download completed!"))
                self.after(0, lambda: messagebox.showinfo("Success", "Instagram download completed!"))

            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)[:300]
                self.after(0, lambda: self.update_status("Download failed!"))
                self.after(0, lambda m=error_msg: messagebox.showerror("Error", f"Download failed:\n{m}"))
            except Exception as e:
                error_msg = str(e)[:300]
                self.after(0, lambda: self.update_status("Error occurred!"))
                self.after(0, lambda m=error_msg: messagebox.showerror("Error", f"Error:\n{m}"))
            finally:
                self.after(0, lambda: self.ig_download_btn.configure(state="normal"))
                self.after(0, lambda: self.set_progress(0))

        threading.Thread(target=download_thread, daemon=True).start()

    def download_spotify(self):
        url = self.sp_url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a Spotify URL!")
            return

        output_path = self.path_entry.get()
        audio_format = self.sp_format_var.get()
        bitrate = self.sp_bitrate_var.get()

        # Disable button during download
        self.sp_download_btn.configure(state="disabled")
        self.update_status("Starting Spotify download...")
        self.set_progress(0)

        def download_thread():
            try:
                # Build environment with FFmpeg path
                env = os.environ.copy()
                if self.ffmpeg_path:
                    env["PATH"] = self.ffmpeg_path + os.pathsep + env.get("PATH", "")

                # Use spotdl for Spotify
                cmd = [
                    sys.executable, "-m", "spotdl",
                    "--output", output_path,
                    "--format", audio_format,
                    "--bitrate", bitrate,
                    "download", url
                ]

                self.after(0, lambda: self.update_status("Downloading from Spotify..."))
                self.after(0, lambda: self.set_progress(0.3))

                process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    env=env,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                )

                if process.returncode == 0:
                    self.after(0, lambda: self.set_progress(1))
                    self.after(0, lambda: self.update_status("Download completed!"))
                    self.after(0, lambda: messagebox.showinfo("Success", "Spotify download completed!"))
                else:
                    error_msg = process.stderr[:300] if process.stderr else process.stdout[:300] if process.stdout else "Unknown error"
                    self.after(0, lambda: self.update_status("Download failed!"))
                    self.after(0, lambda m=error_msg: messagebox.showerror("Error", f"Download failed:\n{m}"))

            except Exception as e:
                error_msg = str(e)[:300]
                self.after(0, lambda: self.update_status("Error occurred!"))
                self.after(0, lambda m=error_msg: messagebox.showerror("Error", f"Error:\n{m}"))
            finally:
                self.after(0, lambda: self.sp_download_btn.configure(state="normal"))
                self.after(0, lambda: self.set_progress(0))

        threading.Thread(target=download_thread, daemon=True).start()


if __name__ == "__main__":
    app = AshuFlow()
    app.mainloop()
