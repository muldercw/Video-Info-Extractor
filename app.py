from flask import Flask, request, jsonify, render_template_string
import requests
from moviepy.editor import VideoFileClip
from PIL import Image
import base64
import io

app = Flask(__name__)

def get_video_info(url):
    try:
        response = requests.head(url)
        if 'content-type' in response.headers:
            mime_type = response.headers['content-type']
            extension = mime_type.split("/")[-1]
        else:
            mime_type = "Unknown"
            extension = "Unknown"

        content_length = response.headers.get("content-length", "Unknown")
        content_encoding = response.headers.get("content-encoding", "Unknown")
        server = response.headers.get("server", "Unknown")
        last_modified = response.headers.get("last-modified", "Unknown")
        content_disposition = response.headers.get("content-disposition", "Unknown")
        content_language = response.headers.get("content-language", "Unknown")

        video_duration = "N/A"
        resolution = "N/A"
        fps = "N/A"
        estimated_frames = "N/A"
        thumbnail_base64 = None

        if mime_type.startswith("video"):
            try:
                video_clip = VideoFileClip(url)
                video_duration = {
                    "seconds": video_clip.duration,
                    "minutes": video_clip.duration / 60
                }
                resolution = {
                    "width": video_clip.size[0],
                    "height": video_clip.size[1]
                }
                fps = video_clip.fps

                estimated_frames = "{:,}".format(int(video_clip.duration * fps))

                thumbnail = video_clip.get_frame(50)  
                with Image.fromarray(thumbnail) as img:
                    img_byte_array = io.BytesIO()
                    img.save(img_byte_array, format="JPEG")
                    thumbnail_base64 = base64.b64encode(img_byte_array.getvalue()).decode()

            except Exception as e:
                video_duration = "Unknown"
                resolution = "Unknown"
                fps = "Unknown"
                estimated_frames = "Unknown"

        video_info = {
            "url": url,
            "mime_type": mime_type,
            "extension": extension,
            "content_length": content_length,
            "content_encoding": content_encoding,
            "server": server,
            "last_modified": last_modified,
            "content_disposition": content_disposition,
            "content_language": content_language,
            "video_duration": video_duration,
            "resolution": resolution,
            "fps": fps,
            "estimated_frames": estimated_frames,
            "thumbnail_base64": thumbnail_base64  
        }
        return video_info

    except Exception as e:
        return {"error": str(e)}

@app.route('/video_info', methods=['POST'])
def video_info_api():
    data = request.get_json()

    if 'url' not in data:
        return jsonify({"error": "URL parameter missing"}), 400

    video_url = data['url']
    video_info = get_video_info(video_url)
    return jsonify(video_info)
@app.route('/', methods=['GET', 'POST'])
@app.route('/video_info/form', methods=['GET', 'POST'])
def video_info_form():
    video_info = None

    if request.method == 'POST':
        url = request.form.get('url')
        video_info = get_video_info(url)

    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Information Form</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f3f3f3;
                margin: 0;
                padding: 0;
            }
            h1 {
                background-color: #3498db;
                color: #fff;
                padding: 20px;
                text-align: center;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border: 1px solid #e1e1e1;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            label, input {
                display: block;
                margin: 10px 0;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            input[type="submit"] {
                background-color: #3498db;
                color: #fff;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            h2 {
                margin: 20px 0 10px;
            }
            p {
                margin: 5px 0;
            }
            img {
                max-width: 100%;
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>Video Information Form</h1>
        <div class="container">
            <form method="POST" action="/video_info/form">
                <label for="url">Video URL:</label>
                <input type="text" name="url" id="url" value="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4" required>
                <input type="submit" value="Submit">
            </form>
            {% if video_info %}
            <h2>Video Information:</h2>
            <p><strong>Video URL:</strong> {{ video_info.url }}</p>
            <p><strong>MIME Type:</strong> {{ video_info.mime_type }}</p>
            <p><strong>Extension:</strong> {{ video_info.extension }}</p>
            <p><strong>Content Length:</strong> {{ video_info.content_length }} bytes</p>
            <p><strong>Content Encoding:</strong> {{ video_info.content_encoding }}</p>
            <p><strong>Content Disposition:</strong> {{ video_info.content_disposition }}</p>
            <p><strong>Content Language:</strong> {{ video_info.content_language }}</p>
            <p><strong>Video Duration (seconds):</strong> {{ video_info.video_duration.seconds }} seconds</p>
            <p><strong>Video Duration (minutes):</strong> {{ video_info.video_duration.minutes }} minutes</p>
            <p><strong>Resolution (Width):</strong> {{ video_info.resolution.width }} pixels</p>
            <p><strong>Resolution (Height):</strong> {{ video_info.resolution.height }} pixels</p>
            <p><strong>FPS (Frames per Second):</strong> {{ video_info.fps }} FPS</p>
            <p><strong>Estimated Frames:</strong> {{ video_info.estimated_frames }} frames</p>
            {% if video_info.thumbnail_base64 %}
            <img src="data:image/jpeg;base64, {{ video_info.thumbnail_base64 }}" alt="Video Thumbnail">
            {% endif %}
            {% endif %}
        </div>
    </body>
    </html>
    """

    return render_template_string(template, video_info=video_info)

if __name__ == '__main__':
    app.run(debug=True)
