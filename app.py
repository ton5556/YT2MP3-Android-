"""
YouTube -> MP3 (ใช้ส่วนตัวในบ้าน)
รัน:  python app.py   แล้วเปิด http://localhost:5000
"""
import os
import re
import shutil
import socket
import threading
import time
import uuid
from pathlib import Path

import yt_dlp
from flask import Flask, abort, jsonify, render_template, request, send_file
from yt_dlp.utils import sanitize_filename

BASE = Path(__file__).parent
DOWNLOADS = BASE / "downloads"
DOWNLOADS.mkdir(exist_ok=True)

# ถ้าวาง ffmpeg.exe / ffprobe.exe ไว้ข้าง app.py จะใช้ตัวนั้น ไม่งั้นหาจาก PATH
FFMPEG_DIR = str(BASE) if any((BASE / n).exists() for n in ("ffmpeg.exe", "ffmpeg")) else None

MAX_DURATION = int(os.environ.get("MAX_DURATION_MIN", "90")) * 60  # นาที -> วินาที
KEEP_SECONDS = 60 * 60  # ลบไฟล์ที่แปลงแล้วหลัง 1 ชั่วโมง
YT_RE = re.compile(r"^https?://([\w-]+\.)?(youtube\.com|youtu\.be)/", re.I)

app = Flask(__name__)
jobs: dict[str, dict] = {}


def cleanup_loop():
    while True:
        now = time.time()
        for f in DOWNLOADS.glob("*"):
            try:
                if now - f.stat().st_mtime > KEEP_SECONDS:
                    f.unlink()
            except OSError:
                pass
        for jid in [j for j, v in jobs.items() if now - v["created"] > KEEP_SECONDS]:
            jobs.pop(jid, None)
        time.sleep(300)


def run_job(job_id: str, url: str):
    job = jobs[job_id]

    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                job["progress"] = min(90, int(d["downloaded_bytes"] / total * 90))
        elif d["status"] == "finished":
            job["stage"] = "converting"
            job["progress"] = 92

    opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "outtmpl": str(DOWNLOADS / f"{job_id}.%(ext)s"),
        "progress_hooks": [hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    if FFMPEG_DIR:
        opts["ffmpeg_location"] = FFMPEG_DIR
    # YouTube บางช่วงต้องใช้ JS runtime ช่วยถอดรหัส (ใน Termux ติดตั้ง nodejs ไว้ให้แล้ว)
    if shutil.which("node") and not shutil.which("deno"):
        opts["js_runtimes"] = {"node": {}}

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info.get("duration") or 0
            if duration > MAX_DURATION:
                raise ValueError(
                    f"คลิปยาวเกินกำหนด ({duration // 60} นาที, สูงสุด {MAX_DURATION // 60} นาที)"
                )
            job["title"] = info.get("title", "audio")
            job["license"] = info.get("license") or "ไม่ระบุ"
            job["is_cc"] = "creative commons" in (info.get("license") or "").lower()
            job["stage"] = "downloading"
            ydl.process_ie_result(info, download=True)

        mp3 = DOWNLOADS / f"{job_id}.mp3"
        if not mp3.exists():
            raise RuntimeError("แปลงไฟล์ไม่สำเร็จ (ตรวจสอบว่าติดตั้ง ffmpeg แล้ว)")
        job["filename"] = sanitize_filename(job["title"]) + ".mp3"
        job["progress"] = 100
        job["stage"] = "done"
    except Exception as e:  # noqa: BLE001
        job["stage"] = "error"
        job["error"] = str(e).replace("ERROR: ", "")[:300]


@app.get("/")
def index():
    return render_template("index.html", max_min=MAX_DURATION // 60)


@app.post("/api/convert")
def convert():
    url = (request.get_json(silent=True) or {}).get("url", "").strip()
    if not YT_RE.match(url):
        return jsonify(error="กรุณาวางลิงก์ YouTube ที่ถูกต้อง"), 400
    job_id = uuid.uuid4().hex
    jobs[job_id] = {
        "stage": "starting",
        "progress": 0,
        "created": time.time(),
    }
    threading.Thread(target=run_job, args=(job_id, url), daemon=True).start()
    return jsonify(id=job_id)


@app.get("/api/status/<job_id>")
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        abort(404)
    return jsonify({k: v for k, v in job.items() if k != "created"})


@app.get("/download/<job_id>")
def download(job_id):
    job = jobs.get(job_id)
    if not job or job.get("stage") != "done":
        abort(404)
    return send_file(
        DOWNLOADS / f"{job_id}.mp3",
        as_attachment=True,
        download_name=job["filename"],
        mimetype="audio/mpeg",
    )


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


if __name__ == "__main__":
    threading.Thread(target=cleanup_loop, daemon=True).start()
    port = int(os.environ.get("PORT", "5000"))
    print(f"\n  บนเครื่องนี้:         http://localhost:{port}")
    print(f"  จากมือถือ/เครื่องอื่น: http://{lan_ip()}:{port}  (ต้องอยู่ Wi-Fi เดียวกัน)\n")
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=port, threaded=True)
