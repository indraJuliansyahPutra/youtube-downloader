import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile

def list_formats(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'listformats': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        formats = result.get("formats", [])
        format_list = ""
        for fmt in formats:
            format_list += f"{fmt['format_id']} - {fmt['ext']} - {fmt.get('format_note', '')} - {fmt.get('resolution', '')}\n"
        return format_list

def download_video(url, mode, format_code=None):
    temp_dir = tempfile.gettempdir()  # Folder sementara server
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
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)

    return filename  # Full file path (misalnya: /tmp/video_title.mp4)

# ----------------------------
# STREAMLIT APP GUI
# ----------------------------
st.set_page_config(page_title="YouTube Downloader", page_icon="📽️")
st.title("🎬 YouTube Video Downloader with yt-dlp")
st.markdown("Gunakan **yt-dlp** untuk mendownload video dari YouTube secara langsung.")

video_url = st.text_input("📌 Masukkan URL YouTube:")

if video_url:
    download_mode = st.radio(
        "📥 Pilih mode download:",
        ["Best Video + Audio", "Pilih Format Manual"]
    )

    if download_mode == "Pilih Format Manual":
        if st.button("🔍 Lihat Daftar Format"):
            with st.spinner("Mengambil daftar format..."):
                try:
                    format_list = list_formats(video_url)
                    st.text_area("🎞️ Daftar Format:", format_list, height=300)
                except Exception as e:
                    st.error("Gagal mengambil format. Pastikan URL valid dan video dapat diakses.")

        format_code = st.text_input("🎯 Masukkan Format Code (contoh: 244):")

        if st.button("⬇️ Download Video"):
            if format_code:
                with st.spinner("Mendownload video..."):
                    try:
                        video_path = download_video(video_url, download_mode, format_code)
                        st.success("✅ Video berhasil diunduh!")
                        with open(video_path, "rb") as f:
                            st.download_button(
                                label="📥 Klik untuk menyimpan ke perangkat",
                                data=f,
                                file_name=os.path.basename(video_path),
                                mime="video/mp4"
                            )
                    except Exception as e:
                        st.error(f"Gagal mengunduh video: {e}")
            else:
                st.warning("⚠️ Harap masukkan format code terlebih dahulu!")

    else:
        if st.button("⬇️ Download Best Quality"):
            with st.spinner("Mendownload video kualitas terbaik..."):
                try:
                    video_path = download_video(video_url, download_mode)
                    st.success("✅ Video berhasil diunduh!")
                    with open(video_path, "rb") as f:
                        st.download_button(
                            label="📥 Klik untuk menyimpan ke perangkat",
                            data=f,
                            file_name=os.path.basename(video_path),
                            mime="video/mp4"
                        )
                except Exception as e:
                    st.error(f"Gagal mengunduh video: {e}")
