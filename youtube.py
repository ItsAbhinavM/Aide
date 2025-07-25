import yt_dlp
import re
from urllib.parse import urlparse, parse_qs
import json
import tempfile
import os

def extract_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.strip("/")
    return None

def youtube_loader(url: str) -> str:
    """Loads and returns the transcript of a YouTube video using yt-dlp."""
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'en-US', 'en-GB'],  # Prefer English subtitles
            'subtitlesformat': 'vtt',
            'skip_download': True,  # Don't download the video, just subtitles
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,  # Suppress output
            'no_warnings': True,
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extract video info first
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', 'Unknown Title')
                    
                    # Download subtitles
                    ydl.download([url])
                    
                    # Find the subtitle file
                    subtitle_files = []
                    for file in os.listdir('.'):
                        if file.endswith('.vtt'):
                            subtitle_files.append(file)
                    
                    if not subtitle_files:
                        return "No subtitles/transcript found for this video. The video may not have captions available."
                    
                    # Use the first subtitle file found
                    subtitle_file = subtitle_files[0]
                    
                    # Read and parse the VTT file
                    with open(subtitle_file, 'r', encoding='utf-8') as f:
                        vtt_content = f.read()
                    
                    # Parse VTT content
                    transcript = parse_vtt_content(vtt_content)
                    
                    if not transcript:
                        return "Failed to parse transcript content."
                    
                    return f"YouTube Video Transcript - {video_title}:\n\n{transcript}"
                    
            finally:
                os.chdir(original_cwd)
                
    except yt_dlp.DownloadError as e:
        return f"Error downloading subtitles: {str(e)}"
    except Exception as e:
        return f"Error extracting transcript with yt-dlp: {str(e)}"

def parse_vtt_content(vtt_content: str) -> str:
    """Parse VTT subtitle content and return formatted transcript."""
    lines = vtt_content.split('\n')
    transcript_parts = []
    current_text = ""
    
    for line in lines:
        line = line.strip()
        
        # Skip VTT header and timing lines
        if line.startswith('WEBVTT') or line.startswith('NOTE') or '-->' in line or not line:
            continue
            
        # Skip timestamp-only lines (like "00:00:01.000")
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}$', line):
            continue
            
        # Clean up subtitle text
        # Remove HTML tags
        clean_line = re.sub(r'<[^>]+>', '', line)
        # Remove extra whitespace
        clean_line = ' '.join(clean_line.split())
        
        if clean_line:
            current_text += clean_line + " "
    
    # Clean up the final text
    transcript = current_text.strip()
    
    # Break into paragraphs for better readability (every ~100 words)
    words = transcript.split()
    paragraphs = []
    current_paragraph = []
    
    for i, word in enumerate(words):
        current_paragraph.append(word)
        if len(current_paragraph) >= 50 or i == len(words) - 1:  # Create paragraph every 50 words
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []
    
    return '\n\n'.join(paragraphs)

# Alternative function if you want to get subtitles with timestamps
def youtube_loader_with_timestamps(url: str) -> str:
    """Loads and returns the transcript with timestamps."""
    try:
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'en-US', 'en-GB'],
            'subtitlesformat': 'vtt',
            'skip_download': True,
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', 'Unknown Title')
                    
                    ydl.download([url])
                    
                    subtitle_files = [f for f in os.listdir('.') if f.endswith('.vtt')]
                    
                    if not subtitle_files:
                        return "No subtitles/transcript found for this video."
                    
                    with open(subtitle_files[0], 'r', encoding='utf-8') as f:
                        vtt_content = f.read()
                    
                    transcript = parse_vtt_with_timestamps(vtt_content)
                    
                    return f"YouTube Video Transcript with Timestamps - {video_title}:\n\n{transcript}"
                    
            finally:
                os.chdir(original_cwd)
                
    except Exception as e:
        return f"Error extracting transcript with timestamps: {str(e)}"

def parse_vtt_with_timestamps(vtt_content: str) -> str:
    """Parse VTT content and return transcript with timestamps."""
    lines = vtt_content.split('\n')
    transcript_parts = []
    current_timestamp = ""
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for timestamp lines
        if '-->' in line:
            # Extract start time
            start_time = line.split(' --> ')[0].strip()
            current_timestamp = start_time
            i += 1
            
            # Get the subtitle text (might be multiple lines)
            subtitle_text = ""
            while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                clean_line = re.sub(r'<[^>]+>', '', lines[i].strip())
                if clean_line:
                    subtitle_text += clean_line + " "
                i += 1
            
            if subtitle_text.strip():
                transcript_parts.append(f"[{current_timestamp}] {subtitle_text.strip()}")
        else:
            i += 1
    
    return '\n\n'.join(transcript_parts)