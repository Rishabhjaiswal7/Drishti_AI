from pydub import AudioSegment
import os

ffmpeg_path = r"C:\Users\sayal\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

AudioSegment.converter = ffmpeg_path

print("ffmpeg exists:", os.path.exists(ffmpeg_path))
print("✅ pydub configured!")