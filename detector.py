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
    command = [
        'ffmpeg',
        '-v', 'error',
        '-i', filepath,
        '-f', 'null',
        '-'
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stderr:
            return "Corrupt", result.stderr.strip()
        return "Healthy", ""
    except subprocess.CalledProcessError as e:
        return "Corrupt", e.stderr.strip() or "General processing error."
    except FileNotFoundError:
        return "Error", "FFmpeg not found. Please install it first."

def scan_directory(directory, recursive=True):
    """Scans a directory for video files."""
    video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.m4v')
    files_to_scan = []
    
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(video_extensions):
                    files_to_scan.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if file.lower().endswith(video_extensions):
                files_to_scan.append(os.path.join(directory, file))
                
    return files_to_scan

def main():
    parser = argparse.ArgumentParser(description="Bit Rot Detector - Cross-platform video integrity checker.")
    parser.add_argument('targets', nargs='*', help="Video files or directories to check.")
    parser.add_argument('--recursive', action='store_true', help="Scan directories recursively.")
    parser.add_argument('--save-hash', action='store_true', help="Save hashes for future comparison.")
    parser.add_argument('--report', action='store_true', help="Generate a JSON report.")
    
    args = parser.parse_args()
    
    if not args.targets:
        return

    all_files = []
    for target in args.targets:
        if os.path.isdir(target):
            all_files.extend(scan_directory(target, args.recursive))
        elif os.path.isfile(target):
            all_files.append(target)
            
    results = []
    
    print(f"--- Bit Rot Detector Scan Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    print(f"Total files found: {len(all_files)}")

    for file in all_files:
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

    if args.report:
        report_filename = f"bit_rot_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"\nReport saved to: {report_filename}")

    print("\n--- Scan Complete ---")

if __name__ == "__main__":
    main()
