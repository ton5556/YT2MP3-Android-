#!/data/data/com.termux/files/usr/bin/bash
# รันครั้งเดียวใน Termux:  bash ~/yt2mp3/setup.sh
set -e
cd "$(dirname "$0")"
APP_DIR="$(pwd)"

echo "== 1/3 ติดตั้งแพ็กเกจ (python, ffmpeg, nodejs) =="
pkg update -y
pkg install -y python ffmpeg curl nodejs

echo "== 2/3 ติดตั้งไลบรารี Python =="
pip install -U flask yt-dlp

echo "== 3/3 สร้างปุ่มลัด =="
mkdir -p "$HOME/.shortcuts"
for f in YT2MP3 YT2MP3-stop; do
  sed "s|__APP_DIR__|$APP_DIR|g" "launcher/$f" > "$HOME/.shortcuts/$f"
  chmod +x "$HOME/.shortcuts/$f"
done

echo
echo "เสร็จแล้ว! ขั้นต่อไป: เพิ่มปุ่มลัด YT2MP3 บนหน้าจอหลักตามใน README.md"
echo "ทดสอบเร็ว ๆ ตอนนี้ได้ด้วย:  bash ~/.shortcuts/YT2MP3"
