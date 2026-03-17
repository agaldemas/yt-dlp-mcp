# yt-dlp-mcp

Standalone MCP server for extracting metadata and downloading videos (TikTok, YouTube, etc.) via yt-dlp.

## Features

- Extract video metadata (title, description, uploader, duration)
- Get direct `.mp4` link without downloading
- **Download videos locally** to a `downloads` folder (now generates both universal MP4 and separate MP3 audio file)
- **Clear downloads cache** to free up disk space
- Support for multiple platforms (TikTok, YouTube, Facebook, Vimeo, etc.)

## Installation

```bash
# Project initialization (already done)
uv init

# Install dependencies (already done)
uv add "mcp[cli]" yt-dlp
```

## Usage

### Start the server

```bash
uv run server.py
```

The server runs in `stdio` mode and is ready to be used by any MCP client.

### Usage with various MCP clients

#### Cline /cline (VS Code)

Add to your `~/.cline/mcp_settings.json`:

```json
{
  "mcpServers": {
    "yt-dlp": {
      "command": "uv",
      "args": ["run", "--directory", "~/Documents/mcp/yt-dlp-mcp", "server.py"]
    }
  }
}
```

#### OpenCode

Add to your `~/.opencode/mcp.json`:

```json
{
  "servers": {
    "yt-dlp": {
      "command": "uv",
      "args": ["run", "--directory", "~/Documents/mcp/yt-dlp-mcp", "server.py"]
    }
  }
}
```

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yt-dlp": {
      "command": "uv",
      "args": ["run", "--directory", "~/Documents/mcp/yt-dlp-mcp", "server.py"]
    }
  }
}
```

#### Zed

Add to your `~/.config/zed/settings.json`:

```json
{
  "mcp": {
    "servers": {
      "yt-dlp": {
        "command": "uv",
        "args": ["run", "--directory", "~/Documents/mcp/yt-dlp-mcp", "server.py"]
      }
    }
  }
}
```

#### Cursor

Add to your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "yt-dlp": {
      "command": "uv",
      "args": ["run", "--directory", "~/Documents/mcp/yt-dlp-mcp", "server.py"]
    }
  }
}
```

### Available Tools

#### 1. extract_video_info

Extracts metadata and direct link from a video. Supports Facebook via lightweight regex and fb-video scraper as fallback.

```python
extract_video_info(url="https://www.tiktok.com/@username/video/123456789")
```

**Parameters:**
- `url` (str): The URL of the video to extract

**Returns:**
- `title` : Video title
- `description` : Video description
- `uploader` : Uploader name
- `duration` : Duration in seconds
- `url` : Direct video link (.mp4)
- `webpage_url` : Original page URL
- `thumbnail` : Thumbnail URL
- `error` : Error message if extraction failed
- `source` : Scraper source (if using Facebook fallbacks)

#### 2. download_video

Downloads a video and generates both a universal MP4 (H.264/AAC/FastStart) and a separate MP3 audio file to the local `downloads` folder.

```python
download_video(url="https://www.tiktok.com/@username/video/123456789")
```

**Parameters:**
- `url` (str): The URL of the video to download

**Returns:**
- `success` : Boolean indicating success
- `title` : Video title
- `filename_mp4` : Local MP4 filename
- `filename_mp3` : Local MP3 filename
- `local_path_mp4` : Absolute path to the downloaded MP4 file
- `local_path_mp3` : Absolute path to the downloaded MP3 file
- `message` : Status message
- `error` : Error message if download failed

#### 3. clear_downloads

Clears all files from the downloads folder.

```python
clear_downloads()
```

**Returns:**
- `success` : Boolean indicating success
- `deleted_count` : Number of files deleted
- `error` : Error message if operation failed

## Updating dependencies

```bash
uv add --upgrade yt-dlp
```

## Requirements

- Python 3.10+
- uv (Python package manager)
- ffmpeg (optional, for video processing)
