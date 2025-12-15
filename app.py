from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid
import re

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

@app.route("/")
def health():
    return "OK"

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    file_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_DIR}/{file_id}.mp4"

    ydl_opts = {
    "outtmpl": output_path,
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "cookies": "cookies.txt",
    "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            title = safe_filename(info.get("title", "video"))

        response = send_file(
            output_path,
            as_attachment=True,
            download_name=f"{title}.mp4"
        )

        # Cleanup AFTER response is prepared
        @response.call_on_close
        def cleanup():
            if os.path.exists(output_path):
                os.remove(output_path)

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()

