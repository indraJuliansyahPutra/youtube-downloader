import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile

def list_formats(url):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get("formats", [])
        format_str = ""
        for f in formats:
            format_id = f.get("format_id", "")
            ext = f.get("ext", "")
            res = f.get("resolution", f"{f.get('height', 'audio')}")
            filesize = f.get("filesize", 0)
            filesize_mb = f"{round(filesize / 1024 / 1024, 2)} MB" if filesize else "?"
            format_str += f"{format_id} | {ext} | {res} | {filesize_mb}\n"
        return format_str

def download_video(url, mode, format_code=None):
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

    if mode == "Best Video + Audio":
        ydl_opts = {
            'format': 'bv*+ba/best',
            'merge_output_format': 'mp4',
            'outtmpl': output_path
        }
    else:
        ydl_opts = {
            'format': f'{format_code}+bestaudio',
            'merge_output_format': 'mp4',
            'outtmpl': output_path
        }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return temp_dir

# ----------------------------
# STREAMLIT GUI
# ----------------------------
st.title("🎬 YouTube Video Downloader with yt-dlp")
st.markdown("Gunakan yt-dlp untuk mendownload video dari YouTube.")

video_url = st.text_input("📌 Masukkan URL YouTube:")

if video_url:
    download_mode = st.radio(
        "📥 Pilih mode download:",
        ["Best Video + Audio", "Pilih Format Manual"]
    )

    if download_mode == "Pilih Format Manual":
        if st.button("🔍 Lihat Daftar Format"):
            with st.spinner("Mengambil daftar format..."):
                format_list = list_formats(video_url)
                st.text_area("🎞️ Daftar Format:", format_list, height=300)

        format_code = st.text_input("🎯 Masukkan Format Code (contoh: 244):")

        if st.button("⬇️ Download Video"):
            if format_code:
                with st.spinner("Mendownload video..."):
                    path = download_video(video_url, download_mode, format_code)
                st.success("✅ Video berhasil diunduh!")
                st.write(f"📁 Disimpan di folder sementara: `{path}`")
            else:
                st.warning("⚠️ Harap masukkan format code terlebih dahulu!")

    else:
        if st.button("⬇️ Download Best Quality"):
            with st.spinner("Mendownload video kualitas terbaik..."):
                path = download_video(video_url, download_mode)
            st.success("✅ Video berhasil diunduh!")
            st.write(f"📁 Disimpan di folder sementara: `{path}`")
