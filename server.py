from mcp.server.fastmcp import FastMCP
from pydantic import Field
import yt_dlp
import os
import re
import requests
from fb_video import FacebookVideoScraper

# Get the project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(PROJECT_DIR, "downloads")

mcp = FastMCP("YTDLP-Extractor")

def _scrape_facebook_regex(url: str) -> dict:
    """Ninja scraper using Regex for Facebook Reels (Lightweight)"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        hd_match = re.search(r'"browser_native_hd_url":"([^"]+)"', html)
        sd_match = re.search(r'"browser_native_sd_url":"([^"]+)"', html)
        video_url = ""
        if hd_match: video_url = hd_match.group(1).replace('\\/', '/')
        elif sd_match: video_url = sd_match.group(1).replace('\\/', '/')
        if video_url: return {"title": "Facebook Reel", "url": video_url, "webpage_url": url, "source": "regex"}
    except Exception: pass
    return {}

def _scrape_facebook_lib(url: str) -> dict:
    """Fallback using fb-video library (Lightweight)"""
    try:
        scraper = FacebookVideoScraper()
        info = scraper.get_info(url)
        if info and info.get("url"): return {"title": info.get("title", "Facebook Video"), "url": info.get("url"), "webpage_url": url, "source": "fb-video"}
    except Exception: pass
    return {}

@mcp.tool()
def extract_video_info(
    url: str = Field(description="The URL of the video to extract")
) -> dict:
    """Extracts metadata and direct link from a video."""
    ydl_opts = {'quiet': True, 'skip_download': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "No title"),
                "description": info.get("description", ""),
                "uploader": info.get("uploader", "Unknown"),
                "duration": info.get("duration", 0),
                "url": info.get("url", ""),
                "webpage_url": info.get("webpage_url", url),
                "thumbnail": info.get("thumbnail", "")
            }
    except Exception as e:
        if "facebook.com" in url:
            res = _scrape_facebook_regex(url)
            if res and res.get("url"): return res
            res = _scrape_facebook_lib(url)
            if res and res.get("url"): return res
        return {"error": str(e)}

@mcp.tool()
def download_video(
    url: str = Field(description="The URL of the video to download")
) -> dict:
    """
    Downloads a video and generates both a universal MP4 (H.264/AAC/FastStart) 
    and a separate MP3 audio file.
    """
    # 1. First download the best multiplexed MP4 (simplest, most reliable base)
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(id)s_raw.%(ext)s'),
        'noplaylist': True,
    }

    try:
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get("id", "unknown")
            if "?" in video_id: video_id = video_id.split("?")[0]
            if "/" in video_id: video_id = video_id.split("/")[-1]
            
            raw_path = os.path.join(DOWNLOADS_DIR, f"{video_id}_raw.mp4")
            # Fallback for raw path if extension differs
            if not os.path.exists(raw_path):
                 for ext in ['mkv', 'webm']:
                    if os.path.exists(os.path.join(DOWNLOADS_DIR, f"{video_id}_raw.{ext}")):
                        raw_path = os.path.join(DOWNLOADS_DIR, f"{video_id}_raw.{ext}")
                        break

            final_mp4 = os.path.join(DOWNLOADS_DIR, f"{video_id}.mp4")
            final_mp3 = os.path.join(DOWNLOADS_DIR, f"{video_id}.mp3")

            # 2. Use FFmpeg manually to guarantee Universal MP4 (H.264/MP3 for VS Code compatibility)
            # We use libmp3lame because VS Code/Electron often lacks AAC license/support
            # -profile:v high -level:v 4.0 and -ar 44100 -ac 2 ensure maximum compatibility
            ffmpeg_cmd = (
                f'ffmpeg -i "{raw_path}" '
                f'-c:v libx264 -profile:v high -level:v 4.0 -pix_fmt yuv420p '
                f'-c:a libmp3lame -ar 44100 -ac 2 -b:a 192k '
                f'-movflags +faststart -y "{final_mp4}" > /dev/null 2>&1'
            )
            os.system(ffmpeg_cmd)
            
            # 3. Use FFmpeg manually to extract MP3
            os.system(f'ffmpeg -i "{final_mp4}" -vn -acodec libmp3lame -ab 192k -y "{final_mp3}" > /dev/null 2>&1')

            # 4. Clean up the raw file
            if os.path.exists(raw_path): os.remove(raw_path)
            
            # Fallback for extensions if needed
            if not os.path.exists(final_mp4):
                for ext in ['mkv', 'webm']:
                    p = os.path.join(DOWNLOADS_DIR, f"{video_id}.{ext}")
                    if os.path.exists(p):
                        final_mp4 = p
                        break
            
            return {
                "success": True,
                "title": info.get("title", "No title"),
                "filename_mp4": os.path.basename(final_mp4),
                "filename_mp3": os.path.basename(final_mp3),
                "local_path_mp4": final_mp4,
                "local_path_mp3": final_mp3,
                "message": f"Universal MP4 and MP3 downloaded to {DOWNLOADS_DIR}"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def clear_downloads() -> dict:
    """Clears all files from the downloads folder."""
    try:
        if not os.path.exists(DOWNLOADS_DIR): return {"success": True, "deleted_count": 0}
        files = os.listdir(DOWNLOADS_DIR)
        deleted_count = 0
        for filename in files:
            file_path = os.path.join(DOWNLOADS_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count += 1
        return {"success": True, "deleted_count": deleted_count}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run(transport='stdio')
