# VideoInfoExtractor

VideoInfoExtractor is a Flask web application that extracts and displays essential information about a video based on its URL. This application is designed to provide details such as MIME type, extension, content length, content encoding, server, last modified, content disposition, content language, video duration, resolution, frames per second (FPS), estimated frames, and even a thumbnail image of the video.

## Features

- Extracts video information: The application retrieves crucial video details from a provided URL.
- MIME Type and Extension: Identify the format and file extension of the video.
- Content Details: Display content length, content encoding, server, last modified time, content disposition, and content language.
- Video Duration: Get the video's duration in seconds and minutes.
- Resolution: Determine the video's width and height in pixels.
- FPS (Frames Per Second): Discover the frames per second rate of the video.
- Estimated Frames: Calculate the estimated number of frames in the video.
- Thumbnail Image: Display a thumbnail image of the video.
- JSON API: Access video information programmatically via a JSON API.
- User-Friendly Web Form: Easily input a video URL and retrieve its details through a web form.

## Usage

1. Clone or download this repository.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Run the Flask application: `python app.py`.

Access the web application through your browser and input a video URL to retrieve its information. You can also programmatically access the details via the JSON API.

## Dependencies

- Flask
- requests
- moviepy
- Pillow (PIL)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve this application.

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.
