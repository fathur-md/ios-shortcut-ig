import os
import yt_dlp
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()


class InstagramRequest(BaseModel):
    url_instagram: str


def hapus_file_temp(path: str):
    if os.path.exists(path):
        os.remove(path)
        print(f"File sementara {path} berhasil dihapus dari laptop.")


@app.post("/api/download")
def parse_instagram(data: InstagramRequest, background_tasks: BackgroundTasks):
    url = data.url_instagram
    print(f"Menerima request download untuk: {url}")

    nama_file_temp = "video_sementara.mp4"

    ydl_opts = {
        "outtmpl": nama_file_temp,
        "format": "best",
        "quiet": False,
    }

    try:
        print("Memulai ekstraksi dan download dari Instagram...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        background_tasks.add_task(hapus_file_temp, nama_file_temp)

        print("Mengirim file ke iPhone...")

        return FileResponse(
            path=nama_file_temp,
            media_type="video/mp4",
            filename="IG_Video_Download.mp4",
        )

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail="Gagal memproses video dari link tersebut."
        )
