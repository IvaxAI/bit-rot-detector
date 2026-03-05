import subprocess
import os
import sys
import argparse
import hashlib
import json
from datetime import datetime

def get_file_hash(filepath, block_size=65536):
    """Generates an MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def check_video_integrity(filepath):
    """
    Uses FFmpeg to decode the video and check for errors.
    Returns (status, error_message)
    """
    # -v error: only show errors
    # -i: input file
    # -f null -: decode but don't save output
    command = [
        'ffmpeg',
        '-v', 'error',
        '-i', filepath,
        '-f', 'null',
        '-'
    ]
    
    try:
        # Run ffmpeg and capture stderr
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stderr:
            return "Corrupt", result.stderr.strip()
        return "Healthy", ""
    except subprocess.CalledProcessError as e:
        return "Corrupt", e.stderr.strip() or "General processing error."
    except FileNotFoundError:
        return "Error", "FFmpeg not found. Please install it first."

def main():
    parser = argparse.ArgumentParser(description="Bit Rot Detector - Cross-platform video integrity checker.")
    parser.add_argument('files', nargs='+', help="Video files to check.")
    parser.add_argument('--save-hash', action='store_true', help="Save hashes for future comparison.")
    
    args = parser.parse_args()
    
    results = []
    
    print(f"--- Bit Rot Detector Scan Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    for file in args.files:
        if not os.path.isfile(file):
            print(f"Skipping: {file} (Not a file)")
            continue
            
        print(f"Scanning: {os.path.basename(file)}...", end="", flush=True)
        
        status, detail = check_video_integrity(file)
        file_hash = get_file_hash(file) if args.save_hash else None
        
        results.append({
            "file": file,
            "status": status,
            "hash": file_hash,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f" [{status}]")
        if status == "Corrupt":
            print(f"   ! Error Details: {detail[:200]}...")

    # For now, just a simple console output. 
    # Future iterations can include a GUI or JSON report generation.
    print("\n--- Scan Complete ---")

if __name__ == "__main__":
    main()
