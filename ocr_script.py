import easyocr
import sys
import os

reader = easyocr.Reader(['fr', 'en'])
downloads_dir = "/Users/alaingaldemas/Documents/mcp/yt-dlp-mcp/downloads/"
frames = [f for f in os.listdir(downloads_dir) if f.startswith("frame_") and f.endswith(".jpg")]
frames.sort()

for frame in frames:
    print(f"--- {frame} ---")
    results = reader.readtext(os.path.join(downloads_dir, frame))
    for (bbox, text, prob) in results:
        print(f"{text} (conf: {prob:.2f})")
