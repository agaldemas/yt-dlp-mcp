# yt-dlp-mcp

Standalone MCP server for extracting metadata and downloading videos (TikTok, YouTube, etc.) via yt-dlp.

## Features

- Extract video metadata (title, description, uploader, duration)
- Get direct `.mp4` link without downloading
- **Download videos locally** to a `downloads` folder
- **Clear downloads cache** to free up disk space
- Support for multiple platforms (TikTok, YouTube, Vimeo, etc.)

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

Extracts video metadata and direct link without downloading.

```
extract_video_info("https://www.tiktok.com/@username/video/123456789")
```

Returns:
- `title` : Video title
- `description` : Video description
- `uploader` : Uploader name
- `duration` : Duration in seconds
- `url` : Direct video link (.mp4)
- `webpage_url` : Original page URL
- `thumbnail` : Thumbnail URL

#### 2. download_video

Downloads the video to the local `downloads` folder and returns the local file path.

```
download_video("https://www.tiktok.com/@username/video/123456789")
```

Returns:
- `success` : Boolean indicating success
- `title` : Video title
- `video_id` : Unique video identifier
- `filename` : Local filename
- `local_path` : Absolute path to the downloaded file
- `webpage_url` : Original page URL
- `message` : Status message

#### 3. clear_downloads

Clears all files from the downloads folder (cache management).

```
clear_downloads()
```

Returns:
- `success` : Boolean indicating success
- `deleted_count` : Number of files deleted
- `message` : Status message

## Updating dependencies

```bash
uv add --upgrade yt-dlp
```

## Requirements

- Python 3.10+
- uv (Python package manager)
- ffmpeg (optional, for video processing)
