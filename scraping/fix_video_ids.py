#!/usr/bin/env python3
import json
import os

# Path to the videos.json file
VIDEOS_JSON_PATH = "/Users/eiffelcsy/Projects/dbtt-prototype/pohkim/public/videos.json"

def fix_video_ids():
    print(f"Fixing video IDs in {VIDEOS_JSON_PATH}")
    
    # Read the existing videos.json file
    with open(VIDEOS_JSON_PATH, 'r', encoding='utf-8') as f:
        videos = json.load(f)
    
    # Sort videos by their current ID
    videos.sort(key=lambda video: video['id'])
    
    # Get the total number of videos
    total_videos = len(videos)
    print(f"Found {total_videos} videos")
    
    # Create a backup of the original file
    backup_path = VIDEOS_JSON_PATH + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    print(f"Created backup at {backup_path}")
    
    # Reassign IDs sequentially starting from 1
    for i, video in enumerate(videos, 1):
        old_id = video['id']
        video['id'] = i
        print(f"Changed ID: {old_id} -> {i}")
    
    # Save the updated videos back to the file
    with open(VIDEOS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully updated {total_videos} videos with sequential IDs")

if __name__ == "__main__":
    fix_video_ids() 