#!/usr/bin/env python3
"""Advanced Search for Video Library"""

import json
import glob
import sys

def search_videos(search_term, show_context=True):
    """Search all videos with context"""
    
    json_files = glob.glob("output/*_metadata.json")
    results = []
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        transcript = data.get("transcription", "")
        
        if search_term.lower() in transcript.lower():
            # Find context around the match
            idx = transcript.lower().find(search_term.lower())
            start = max(0, idx - 100)
            end = min(len(transcript), idx + 100)
            context = transcript[start:end]
            
            results.append({
                "video": data["video_file"],
                "buildings": data.get("buildings", []),
                "context": context,
                "full_transcript": transcript
            })
    
    return results

def main():
    if len(sys.argv) < 2:
        print("🔍 VIDEO SEARCH TOOL")
        print("\nUsage: python advanced_search.py <search_term>")
        print("\nExamples:")
        print("  python advanced_search.py Sheffield")
        print("  python advanced_search.py research")
        print("  python advanced_search.py criminology")
        return
    
    search_term = " ".join(sys.argv[1:])
    results = search_videos(search_term)
    
    print(f"\n🔍 Searching for: '{search_term}'")
    print(f"📊 Found {len(results)} videos\n")
    
    for i, result in enumerate(results, 1):
        print(f"\n{'='*70}")
        print(f"📹 {i}. {result['video']}")
        print('='*70)
        
        if result['buildings']:
            print(f"🏛️  Buildings: {', '.join(result['buildings'])}")
        
        print(f"\n💬 Context:")
        print(f"   ...{result['context']}...")
        
    if not results:
        print("❌ No matches found")
        print("\n💡 Try searching for:")
        print("   - Sheffield")
        print("   - student")
        print("   - research")
        print("   - campus")

if __name__ == "__main__":
    main()