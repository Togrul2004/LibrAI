#!/usr/bin/env python3
"""
Batch Video Processor for Sheffield Hackathon
Processes all videos in the 'videos' folder
"""

import glob
import os
import json
from pathlib import Path
import time
from datetime import datetime
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import our processor
import quick_fix

def process_all_videos():
    """Process all MP4 files in the videos folder"""
    
    # Find all videos
    video_folder = Path("videos")
    if not video_folder.exists():
        print("ERROR: 'videos' folder not found!")
        print("Create it and put your MP4 files there")
        return
    
    videos = list(video_folder.glob("*.mp4"))
    
    if not videos:
        print("ERROR: No MP4 files found in 'videos' folder!")
        return
    
    print("\n" + "="*70)
    print("  BATCH VIDEO PROCESSOR - Sheffield Hackathon")
    print(f"  Found {len(videos)} videos to process")
    print("="*70 + "\n")
    
    results = {
        "processed": [],
        "skipped": [],
        "failed": []
    }
    
    start_time = time.time()
    
    for i, video_path in enumerate(videos, 1):
        print(f"\n{'='*70}")
        print(f"VIDEO {i}/{len(videos)}: {video_path.name}")
        print('='*70)
        
        # Check if already processed
        output_name = video_path.stem + "_metadata.json"
        output_path = Path("output") / output_name
        
        if output_path.exists():
            # If transcript is empty, re-process it (maybe FFmpeg was fixed)
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    if meta.get('transcription', '').strip():
                        print("Already processed - skipping...")
                        results["skipped"].append(video_path.name)
                        continue
                    else:
                        print("Found empty transcript - re-processing...")
            except:
                print("Failed to read existing metadata - re-processing...")
        
        try:
            # Process the video
            processor = quick_fix.VideoProcessor(str(video_path))
            processor.process()
            results["processed"].append(video_path.name)
            
        except KeyboardInterrupt:
            print("\nStopped by user")
            break
        except Exception as e:
            print(f"FAILED: {e}")
            results["failed"].append({
                "video": video_path.name,
                "error": str(e)
            })
    
    # Print summary
    elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print("BATCH PROCESSING SUMMARY")
    print('='*70)
    print(f"Processed:  {len(results['processed'])} videos")
    print(f"Skipped:    {len(results['skipped'])} videos (already done)")
    print(f"Failed:     {len(results['failed'])} videos")
    print(f"Total time: {elapsed/60:.1f} minutes")
    print(f"Avg time:   {elapsed/max(len(results['processed']), 1)/60:.1f} min/video")
    
    if results['failed']:
        print("\nFailed videos:")
        for fail in results['failed']:
            print(f"   - {fail['video']}: {fail['error']}")
    
    print(f"\nAll results saved to: output/")
    
    # Save batch summary
    summary_path = Path("output") / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            "total_videos": len(videos),
            "processed": results['processed'],
            "skipped": results['skipped'],
            "failed": results['failed'],
            "total_time_minutes": elapsed/60,
            "avg_time_per_video": elapsed/max(len(results['processed']), 1)/60
        }, f, indent=2)
    
    print(f"Summary saved: {summary_path}")
    
    return results

if __name__ == "__main__":
    print("Starting batch processing...")
    print("Press Ctrl+C to stop at any time\n")
    
    results = process_all_videos()
    
    print("\nDone! Check the 'output' folder for all results!")