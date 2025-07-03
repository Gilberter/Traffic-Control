video_url = "https://youtu.be/ByED80IKdIU"
id_video_url = "ByED80IKdIU"
# Download the video using ytarchive and ffmpeg
# Had to install Go
# go install github.com/Kethsar/ytarchive@dev
# Download FFmpeg:
# Go to the official FFmpeg download page: https://ffmpeg.org/download.html
# Click “Windows” and choose a build, e.g., Gyan.dev builds.
# ytarchive --ffmpeg-path "C:\ffmpeg\bin\ffmpeg.exe" --live-from -00:05:00 --capture-duration 1m https://www.youtube.com/watch?v=ByED80IKdIU best
