import os
import yt_dlp
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="YT Grab Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        @keyframes float {
            0% {transform: translateY(0px);}
            50% {transform: translateY(-10px);}
            100% {transform: translateY(0px);}
        }
        
        @keyframes shine {
            to {background-position: 200% center;}
        }
        
        @keyframes pulse {
            0% {transform: scale(1);}
            50% {transform: scale(1.05);}
            100% {transform: scale(1);}
        }
        
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --accent: #ec4899;
            --background: #f8fafc;
        }
        
        body {
            background: linear-gradient(45deg, #f3f4f6, #e5e7eb) !important;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        
        .main {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            animation: float 6s ease-in-out infinite;
            margin: 1rem auto;
            max-width: 800px;
        }
        
        .header {
            text-align: center;
            padding: 3rem 0;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            background-size: 200% 200%;
            animation: gradient 8s ease infinite;
            color: white;
            border-radius: 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .header::after {
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            animation: shine 3s infinite;
        }
        
        .stTextInput>div>div>input {
            border-radius: 15px !important;
            padding: 14px 24px !important;
            border: 2px solid #e2e8f0 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-size: 1rem;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
        }
        
        .stSelectbox>div>div>select {
            border-radius: 15px !important;
            padding: 12px 20px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton>button {
            width: 100%;
            border-radius: 15px !important;
            padding: 16px 32px !important;
            background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
            color: white !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative;
            overflow: hidden;
            border: none !important;
            animation: pulse 2s infinite;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3) !important;
            animation: none;
        }
        
        .stButton>button::after {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(255, 255, 255, 0.3),
                transparent
            );
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }
        
        .download-info {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin-top: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            animation: slideIn 0.5s ease-out;
        }
        
        .path-info {
            background: linear-gradient(135deg, #f8fafc, #e2e8f0);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid var(--primary);
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }
        
        .footer {
            text-align: center;
            padding: 2rem 0;
            margin-top: 3rem;
            color: #64748b;
            position: relative;
        }
        
        .platforms {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 1.5rem 0;
            flex-wrap: wrap;
        }
        
        .platform-badge {
            background: rgba(99, 102, 241, 0.1);
            padding: 0.6rem 1.2rem;
            border-radius: 25px;
            font-size: 0.9rem;
            color: var(--primary);
            border: 1px solid rgba(99, 102, 241, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .platform-badge:hover {
            transform: translateY(-2px);
            background: rgba(99, 102, 241, 0.15);
            box-shadow: 0 4px 6px rgba(99, 102, 241, 0.1);
        }
        
        .platform-badge.active {
            background: var(--primary);
            color: white;
            font-weight: 500;
        }
        
        @keyframes slideIn {
            from {transform: translateY(20px); opacity: 0;}
            to {transform: translateY(0); opacity: 1;}
        }
        
        .stSpinner>div {
            border-color: var(--primary) transparent transparent transparent !important;
        }
        
        .watermark {
            position: fixed;
            bottom: 10px;
            right: 10px;
            opacity: 0.5;
            font-size: 0.8rem;
            color: #64748b;
        }
    </style>
""", unsafe_allow_html=True)

def get_download_dir():
    """
    Returns a well-defined downloads directory for the user's operating system
    """
    # Get user's home directory
    home_dir = Path.home()
    
    # Define the download directory path
    if os.name == 'nt':  # Windows
        # Try common Windows download locations
        downloads_dir = home_dir / 'Downloads'
        if not downloads_dir.exists():
            downloads_dir = home_dir / 'Desktop'
    else:  # macOS, Linux, and other Unix-like systems
        downloads_dir = home_dir / 'Downloads'
        if not downloads_dir.exists():
            downloads_dir = home_dir / 'Desktop'
    
    # Create downloads directory if it doesn't exist
    downloads_dir.mkdir(exist_ok=True)
    
    # Create YT Grab Pro subfolder
    yt_grab_dir = downloads_dir / 'YT_Grab_Pro'
    yt_grab_dir.mkdir(exist_ok=True)
    
    return str(yt_grab_dir)

def validate_custom_path(path_str):
    """
    Validates if a custom path exists and is writable
    """
    try:
        path = Path(path_str)
        if path.exists() and path.is_dir():
            # Test if we can write to the directory
            test_file = path / '.test_write'
            try:
                test_file.touch()
                test_file.unlink()
                return True, str(path)
            except PermissionError:
                return False, "Permission denied - cannot write to this directory"
        else:
            return False, "Directory does not exist"
    except Exception as e:
        return False, f"Invalid path: {str(e)}"

# Initialize download path
DEFAULT_DOWNLOAD_PATH = get_download_dir()

st.markdown('<div class="header"><h1 style="margin:0;font-size:2.5rem;">🚀 YT Grab Pro</h1><p style="margin:0.5rem 0 0;font-size:1.1rem;">Download Videos from Popular Platforms</p></div>', unsafe_allow_html=True)
st.markdown("<div class='main'>", unsafe_allow_html=True)

st.markdown("### 📥 Download Media Content")
url = st.text_input("Paste URL here", placeholder="📌 Example: https://youtube.com/watch?v=... or https://tiktok.com/@user/video/...")

# Download path configuration
st.markdown("### 📂 Download Location")
st.markdown(f'<div class="path-info">📁 Default: {DEFAULT_DOWNLOAD_PATH}</div>', unsafe_allow_html=True)

use_custom_path = st.checkbox("Use custom save location")

if use_custom_path:
    custom_path = st.text_input("Custom save location:", 
                               value=DEFAULT_DOWNLOAD_PATH,
                               help="Enter a valid directory path where files should be saved")
    
    if custom_path:
        valid, message = validate_custom_path(custom_path)
        if valid:
            download_path = message
            st.success(f"✅ Valid path: {download_path}")
        else:
            st.error(f"❌ {message}")
            st.warning("Using default location instead.")
            download_path = DEFAULT_DOWNLOAD_PATH
    else:
        download_path = DEFAULT_DOWNLOAD_PATH
else:
    download_path = DEFAULT_DOWNLOAD_PATH

# Platform detection
platform = None
if url:
    if "youtube.com" in url or "youtu.be" in url:
        platform = "YouTube"
    elif "tiktok.com" in url:
        platform = "TikTok"
    elif "instagram.com" in url:
        platform = "Instagram"
    elif "twitter.com" in url or "x.com" in url:
        platform = "Twitter/X"

format_choice = st.selectbox(
    "🎚️ Select Format",
    ["Best Video", "Best Audio", "MP4 720p", "MP4 480p", "MP3"],
    index=0
)

if st.button("🚀 Start Download"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        # Ensure download directory exists
        Path(download_path).mkdir(parents=True, exist_ok=True)
        
        ydl_opts = {
            "outtmpl": f"{download_path}/%(title)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "restrictfilenames": True,  # Avoid special characters in filenames
        }
        
        # Format-specific configurations
        if format_choice == "Best Audio":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        elif format_choice == "MP4 720p":
            ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best[height<=720]"
            ydl_opts["merge_output_format"] = "mp4"
        elif format_choice == "MP4 480p":
            ydl_opts["format"] = "bestvideo[height<=480]+bestaudio/best[height<=480]"
            ydl_opts["merge_output_format"] = "mp4"
        elif format_choice == "MP3":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        else:  # Best Video
            ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

        with st.spinner("⏳ Downloading... This might take a moment"):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract info first to get the title
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Unknown')
                    
                    # Now download
                    ydl.download([url])
                    
                    st.success("🎉 Download completed successfully!")
                    
                    # Show download information
                    st.markdown(f'''
                    <div class="download-info">
                        <h4>📁 Download Complete!</h4>
                        <p><strong>Title:</strong> {title}</p>
                        <p><strong>Format:</strong> {format_choice}</p>
                        <p><strong>Platform:</strong> {platform or "Unknown"}</p>
                        <p><strong>Saved to:</strong></p>
                        <code>{download_path}</code>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Show files in directory
                    try:
                        files = list(Path(download_path).glob("*"))
                        if files:
                            st.markdown("### 📋 Recent Downloads")
                            for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                                if file.is_file():
                                    file_size = file.stat().st_size / (1024 * 1024)  # Convert to MB
                                    st.write(f"📄 {file.name} ({file_size:.1f} MB)")
                    except Exception:
                        pass  # Don't show error if we can't list files
                        
            except Exception as e:
                st.error(f"❌ Download failed: {str(e)}")
                st.info("💡 Try checking if the URL is valid and accessible.")

st.markdown(f"""
    <div class="footer">
        <div class="platforms">
            <span class="platform-badge {'active' if platform == 'YouTube' else ''}">YouTube</span>
            <span class="platform-badge {'active' if platform == 'TikTok' else ''}">TikTok</span>
            <span class="platform-badge {'active' if platform == 'Instagram' else ''}">Instagram</span>
            <span class="platform-badge {'active' if platform == 'Twitter/X' else ''}">Twitter/X</span>
            <span class="platform-badge">Facebook</span>
        </div>
        <p style="margin:1rem 0">Made with ❤️ by IntechX</p>
        <div style="display:flex; justify-content:center; gap:1rem; margin:1rem 0;">
            <a href="#" style="color:#64748b; text-decoration:none;">📜 Terms</a>
            <a href="#" style="color:#64748b; text-decoration:none;">🔒 Privacy</a>
            <a href="#" style="color:#64748b; text-decoration:none;">📧 Contact</a>
        </div>
        <hr style="height:2rem;border:none;border-top:1px solid #e2e8f0;">
        <p style="font-size:0.8rem; color:#94a3b8;">
            © 2025 YT Grab Pro. All rights reserved.<br>
            This tool is for educational purposes only.
        </p>
    </div>
    <div class="watermark">v2.2.0</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)