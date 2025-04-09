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
    temp_dir = tempfile.mkdtemp()  # folder sementara untuk tiap user
    output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

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

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # Cari file mp4 yang telah diunduh
    for file in os.listdir(temp_dir):
        if file.endswith(".mp4"):
            return os.path.join(temp_dir, file)

    raise FileNotFoundError("File mp4 tidak ditemukan setelah download.")

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
                    try:
                        video_path = download_video(video_url, download_mode, format_code)
                        st.success("✅ Video berhasil diunduh!")

                        file_name = os.path.basename(video_path)
                        with open(video_path, "rb") as f:
                            st.download_button(
                                label="💾 Klik untuk menyimpan ke perangkat",
                                data=f,
                                file_name=file_name,
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

                    file_name = os.path.basename(video_path)
                    with open(video_path, "rb") as f:
                        st.download_button(
                            label="💾 Klik untuk menyimpan ke perangkat",
                            data=f,
                            file_name=file_name,
                            mime="video/mp4"
                        )
                except Exception as e:
                    st.error(f"Gagal mengunduh video: {e}")
