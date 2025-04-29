import os
import json
from pathlib import Path
import streamlit as st
import yt_dlp
from datetime import datetime

# Constants
HISTORY_FILE = "history.json"
DEFAULT_PATH = str(Path.home() / "Downloads" / "YouTube")

# Streamlit Config
st.set_page_config(page_title="🎥 YouTube Downloader", page_icon="📥", layout="wide")

# Load Download History
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def add_to_history(title, output_path, type_):
    history = load_history()
    history.insert(0, {
        "title": title,
        "path": output_path,
        "type": type_,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_history(history)

# Metadata Fetcher
def get_video_info(url):
    ydl_opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

# Downloader
def download_with_ytdlp(video_url, quality, output_path, is_playlist=False):
    os.makedirs(output_path, exist_ok=True)
    format_option = resolution_map.get(quality, resolution_map["1080p"])

    ydl_opts = {
        'format': format_option,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    if is_playlist:
        ydl_opts.update({
            'extract_flat': False,
            'outtmpl': os.path.join(output_path, '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s'),
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        return info

# Resolution options
resolution_map = {
    'Best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'Worst': 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]/worst',
    '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=1080]',
    '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]',
    '480p': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480]',
    '360p': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best[height<=360]',
    '240p': 'bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/best[height<=240][ext=mp4]/best[height<=240]',
    '144p': 'bestvideo[height<=144][ext=mp4]+bestaudio[ext=m4a]/best[height<=144][ext=mp4]/best[height<=144]',
}

# Sidebar
with st.sidebar:
    st.header("📜 Download History")
    history = load_history()
    if history:
        for item in history[:10]:
            st.markdown(f"**{item['title']}**  \n📁 `{item['path']}`  \n📅 *{item['timestamp']}*  \n📦 {item['type']}")
            st.markdown("---")
    else:
        st.info("No downloads yet.")

# Main UI
st.title("📥 YouTube Downloader with yt-dlp")

url = st.text_input("Enter YouTube Video or Playlist URL")
col1, col2 = st.columns([2, 1])
with col1:
    download_type = st.radio("Download Type", ["Single Video", "Playlist"])
with col2:
    resolution = st.selectbox("Select Resolution", list(resolution_map.keys()), index=1)

custom_path = st.text_input("Optional: Enter custom download path", "")

if url:
    try:
        info = get_video_info(url)
        st.subheader("🔍 Preview")
        st.image(info['thumbnail'], width=300)
        st.markdown(f"**Title:** {info.get('title')}")
        st.markdown(f"**Uploader:** {info.get('uploader')}")
        st.markdown(f"**Duration:** {int(info.get('duration', 0)) // 60} min")
        st.markdown(f"**Views:** {info.get('view_count'):,}")
    except Exception as e:
        st.error(f"Failed to fetch metadata: {e}")

if st.button("⬇️ Start Download"):
    if not url:
        st.warning("Please enter a YouTube URL.")
    else:
        with st.spinner("Downloading..."):
            path = custom_path or DEFAULT_PATH
            is_playlist = download_type == "Playlist"
            try:
                result = download_with_ytdlp(url, resolution, path, is_playlist)
                title = result.get("title", "Unknown")
                add_to_history(title, path, "Playlist" if is_playlist else "Video")
                st.success(f"✅ Download complete! Saved to: `{path}`")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
