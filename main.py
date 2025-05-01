import os
import yt_dlp
import streamlit as st
from pathlib import Path

# Set up configuration
st.set_page_config(page_title="YT Grab Pro", page_icon="🚀", layout="centered")

# Premium CSS styling with animations
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

# Get download directory
def get_download_dir():
    """
    Returns the default downloads directory for the user's operating system
    """
    # First try to get standard Downloads folder
    if os.name == 'nt':  # Windows
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    elif os.name == 'posix':  # macOS, Linux, and other Unix-like systems
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        # Fallback to Videos folder in home directory
        download_dir = os.path.join(os.path.expanduser('~'), 'Videos')
    
    # Create the directory if it doesn't exist
    Path(download_dir).mkdir(exist_ok=True)
    
    # Create a Videos subdirectory in the downloads folder
    videos_dir = os.path.join(download_dir, 'Yt Grab ')
    Path(videos_dir).mkdir(exist_ok=True)
    
    return videos_dir

# Set up download directory
DOWNLOAD_PATH = get_download_dir()

# App UI
st.markdown('<div class="header"><h1 style="margin:0;font-size:2.5rem;">🚀 YT Grab Pro</h1><p style="margin:0.5rem 0 0;font-size:1.1rem;">Download Videos from Popular Platforms</p></div>', unsafe_allow_html=True)
st.markdown("<div class='main'>", unsafe_allow_html=True)

st.markdown("### 📥 Download Media Content")
url = st.text_input("Paste URL here", placeholder="📌 Example: https://youtube.com/watch?v=... or https://tiktok.com/@user/video/...")

# Save location display and option
st.markdown(f"**Save location:** {DOWNLOAD_PATH}")
use_custom_path = st.checkbox("Use custom save location")

if use_custom_path:
    custom_path = st.text_input("Custom save location (full path):", 
                               value=DOWNLOAD_PATH,
                               help="Enter a valid path on your device where files should be saved")
    if custom_path and Path(custom_path).exists():
        download_path = custom_path
    else:
        if custom_path:
            st.warning("Path does not exist. Will use default location.")
        download_path = DOWNLOAD_PATH
else:
    download_path = DOWNLOAD_PATH

# Detect platform automatically
platform = None
if url:
    if "youtube.com" in url or "youtu.be" in url:
        platform = "YouTube"
    elif "tiktok.com" in url:
        platform = "TikTok"

format_choice = st.selectbox(
    "🎚️ Select Format",
    ["Best Video", "Best Audio", "MP4 720p", "MP4 480p", "MP3"],
    index=0
)

if st.button("🚀 Start Download"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        ydl_opts = {
            "outtmpl": f"{download_path}/%(title)s.%(ext)s",
            "quiet": True,
            "no_warnings": True
        }
        
        if platform == "YouTube":
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
                ydl_opts["format"] = "bestvideo[height<=720]+bestaudio/best"
                ydl_opts["merge_output_format"] = "mp4"
            elif format_choice == "MP4 480p":
                ydl_opts["format"] = "bestvideo[height<=480]+bestaudio/best"
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
                
        elif platform == "TikTok":
            if format_choice in ["Best Audio", "MP3"]:
                ydl_opts.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                })
            else:
                ydl_opts["format"] = "best"
        else:
            st.error("Unsupported platform. Currently supports YouTube and TikTok.")
            st.stop()

        with st.spinner("⏳ Downloading... This might take a moment"):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    st.success("🎉 Download completed!")
                    st.markdown(f'<div class="download-info">'
                                f'<strong>Saved file:</strong><br>'
                                f'<code>{filename}</code><br><br>'
                                f'<strong>Download location:</strong><br>'
                                f'<code>{download_path}</code></div>', 
                                unsafe_allow_html=True)
                    st.balloons()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer with platform detection
st.markdown(f"""
    <div class="footer">
        <div class="platforms">
            <span class="platform-badge {'active' if platform == 'YouTube' else ''}">YouTube</span>
            <span class="platform-badge {'active' if platform == 'TikTok' else ''}">TikTok</span>
            <span class="platform-badge">Instagram</span>
            <span class="platform-badge">Twitter/X</span>
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
    <div class="watermark">v2.1.0</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)