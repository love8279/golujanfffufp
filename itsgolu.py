import os
import re
import time
import json
import asyncio
import logging
import requests
import subprocess
from math import ceil
from utils import progress_bar
from pyrogram import Client, filters
from pyrogram.types import Message
from vars import * from db import Database

# --- API CONFIGURATION ---
# Teri Vercel API ka base link
CP_API_URL = "https://cpapigolu.vercel.app/ITsGOLU_OFFICIAL"

async def get_api_link(video_url):
    """
    Injected Function: Fetches signed/bypassed URL from your Vercel API.
    """
    try:
        # Link ko encode karke API bhej rahe hain
        api_call = f"{CP_API_URL}?url={video_url}"
        response = requests.get(api_call, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Agar API 'url' ya 'signed_url' key bhej rahi hai
            new_url = data.get("url") or data.get("signed_url")
            if new_url:
                logging.info(f"Successfully bypassed link via API")
                return new_url
    except Exception as e:
        logging.error(f"API Error: {e}")
    
    return video_url # Kuch gadbad hui toh purana link use karega

# --- ORIGINAL FUNCTIONS UPDATED WITH API LOGIC ---

def get_duration(filename):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def split_large_video(file_path, max_size_mb=1900):
    size_bytes = os.path.getsize(file_path)
    max_bytes = max_size_mb * 1024 * 1024

    if size_bytes <= max_bytes:
        return [file_path]

    duration = get_duration(file_path)
    parts = ceil(size_bytes / max_bytes)
    part_duration = duration / parts
    base_name = file_path.rsplit(".", 1)[0]
    output_files = []

    for i in range(parts):
        start_time = i * part_duration
        part_name = f"{base_name}_part_{i+1}.mp4"
        subprocess.run([
            "ffmpeg", "-i", file_path, "-ss", str(start_time),
            "-t", str(part_duration), "-c", "copy", "-map", "0", part_name
        ])
        output_files.append(part_name)

    return output_files

async def download_video(url, name, message):
    """
    Updated: Ab ye download karne se pehle teri API se link update karega.
    """
    # Step 1: Link ko API se bypass karwana
    if "classplus" in url or "m3u8" in url:
        await message.edit(f"📥 **Bypassing Link via API...**\n`{name}`")
        url = await get_api_link(url)

    # Step 2: Download Logic (Example using yt-dlp as per your repo)
    await message.edit(f"📥 **Downloading:** `{name}`")
    
    # Yahan tumhara purana yt-dlp ya download logic continue hoga...
    # (Maine integration point set kar diya hai)
    
    # ... baki ka code jo tumne bheja tha wo same rahega
    
