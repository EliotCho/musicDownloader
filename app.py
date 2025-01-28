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
            return "Missing parameters", 400

        downloads_path = str(Path.home() / "Downloads")
        response = requests.get(video_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"})
        # print(f"The response code: {response}")

        response = requests.head(video_url, headers={"User-Agent": "..."} )
        if response.status_code != 200:
            return "Invalid URL", 400


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
        }


        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Return a success response
        return jsonify({"message": "Download successful"}), 200

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
