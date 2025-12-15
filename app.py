from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    filename = str(uuid.uuid4())

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/{filename}.%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        ext = info["ext"]
        title = info["title"]

    file_path = f"{DOWNLOAD_DIR}/{filename}.{ext}"

    return send_file(
        file_path,
        as_attachment=True,
        download_name=f"{title}.mp4"
    )

if __name__ == "__main__":
    app.run()
