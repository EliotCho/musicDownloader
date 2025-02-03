from flask import Flask, request, jsonify, send_file, render_template
import os
import requests
from pathlib import Path
import yt_dlp as youtube_dl

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        video_url = data.get('videoUrl')
        file_format = data.get('format')
        quality = data.get('quality')

        if not video_url or not file_format or not quality:
            return jsonify({"error": "Missing parameters"}), 400

        # Define temporary storage path for downloads
        downloads_path = "/tmp"
        os.makedirs(downloads_path, exist_ok=True)  # Ensure the directory exists

        # Export cookies from environment variable to a file
        cookies_path = "/tmp/cookies.txt"
        cookies_content = os.getenv("YTDLP_COOKIES", "")
        
        if not cookies_content:
            return jsonify({"error": "Missing YouTube cookies. Please set YTDLP_COOKIES in environment variables."}), 400

        with open(cookies_path, "w") as f:
            f.write(cookies_content)

        # Validate URL
        response = requests.head(video_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            return jsonify({"error": "Invalid URL"}), 400

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': file_format,
                    'preferredquality': quality,
                },
            ],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            },
            'cookies': cookies_path,  # Pass cookies
        }

        # Download the video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return jsonify({"message": "Download successful"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
