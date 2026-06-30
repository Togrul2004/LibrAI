#!/usr/bin/env python3
"""Analytics Dashboard for Processed Videos"""

import json
import glob
from collections import Counter
from pathlib import Path

def analyze_all_videos():
    """Generate statistics from all processed videos"""
    
    json_files = glob.glob("output/*_metadata.json")
    
    if not json_files:
        print("❌ No processed videos found!")
        return
    
    print(f"\n📊 ANALYZING {len(json_files)} VIDEOS\n")
    
    all_buildings = []
    all_words = []
    total_duration = 0
    topics = Counter()
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Collect buildings
        all_buildings.extend(data.get("buildings", []))
        
        # Count words
        transcript = data.get("transcription", "")
        all_words.extend(transcript.lower().split())
        
        # Count segments (duration estimate)
        segments = data.get("segments", [])
        if segments:
            total_duration += segments[-1].get("end", 0)
    
    # Buildings
    print("🏛️  BUILDINGS MENTIONED:")
    building_counts = Counter(all_buildings)
    if building_counts:
        for building, count in building_counts.most_common(10):
            print(f"   {building}: {count} videos")
    else:
        print("   None detected (videos may not show campus)")
    
    # Top words
    print("\n📝 TOP WORDS:")
    # Filter out common words
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'it', 'that', 'this', 'with', 'was', 'as', 'be', 'are'}
    filtered_words = [w for w in all_words if len(w) > 3 and w not in stopwords]
    word_counts = Counter(filtered_words)
    
    for word, count in word_counts.most_common(20):
        print(f"   {word}: {count}")
    
    # Stats
    print(f"\n📈 STATISTICS:")
    print(f"   Total videos: {len(json_files)}")
    print(f"   Total duration: {total_duration/60:.1f} minutes")
    print(f"   Total words: {len(all_words):,}")
    print(f"   Avg words/video: {len(all_words)//len(json_files):,}")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    analyze_all_videos()