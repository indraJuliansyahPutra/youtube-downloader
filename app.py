import streamlit as st
import subprocess
import os
import tempfile

def list_formats(url):
    result = subprocess.run(
        ["yt-dlp", "-F", url],
        capture_output=True, text=True
    )
    return result.stdout

def download_video(url, mode, format_code=None):
    save_folder = "Downloaded_Videos"
    os.makedirs(save_folder, exist_ok=True)
    output_path = os.path.join(save_folder, "%(title)s.%(ext)s")

    if mode == "Best Video + Audio":
        cmd = [
            "yt-dlp", "-f", "bv*+ba/best", 
            "--merge-output-format", "mp4", 
            "-o", output_path, url
        ]
    else:
        cmd = [
            "yt-dlp", "-f", f"{format_code}+bestaudio", 
            "--merge-output-format", "mp4", 
            "-o", output_path, url
        ]

    subprocess.run(cmd)
    return save_folder

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
                st.write(f"📁 Disimpan di folder: `{path}`")
            else:
                st.warning("⚠️ Harap masukkan format code terlebih dahulu!")

    else:
        if st.button("⬇️ Download Best Quality"):
            with st.spinner("Mendownload video kualitas terbaik..."):
                path = download_video(video_url, download_mode)
            st.success("✅ Video berhasil diunduh!")
            st.write(f"📁 Disimpan di folder: `{path}`")
