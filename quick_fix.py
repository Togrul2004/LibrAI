#!/usr/bin/env python3
"""Quick Hackathon Video Processor - Windows Compatible"""

import json
import os
import subprocess
from pathlib import Path
from typing import List, Dict
import csv
from datetime import datetime

class VideoProcessor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.work_dir = Path(os.getcwd()) / "output"
        self.work_dir.mkdir(exist_ok=True, parents=True)
        self.video_name = Path(video_path).stem
        
        self.sheffield_landmarks = [
            "Octagon", "Diamond", "Western Bank Library", "Information Commons",
            "Arts Tower", "Firth Court", "Alfred Denny Building", "The Wave",
            "Engineering Heartspace", "Students Union", "Jessop West"
        ]
    
    def process(self):
        print("\n" + "="*60)
        print("🎓 PROCESSING VIDEO")
        print("="*60 + "\n")
        
        # 1. Extract audio
        print("📹 Extracting audio...")
        audio_path = self.work_dir / "audio.wav"
        
        try:
            subprocess.run([
                "ffmpeg", "-i", self.video_path,
                "-vn", "-acodec", "pcm_s16le",
                "-ar", "16000", "-ac", "1",
                str(audio_path), "-y"
            ], capture_output=True, check=True)
            print("   ✅ Audio extracted")
        except:
            print("   ⚠️  FFmpeg error - continuing anyway...")
            audio_path = None
        
        # 2. Transcribe
        transcription = {"full_text": "", "segments": []}
        
        # 2a. Fast-Path: Try native YouTube API bypassing local computation
        print("\n🎤 Attempting YouTube Transcript API bypass...")
        video_id = self.video_name.split("_")[-1]
        
        if len(video_id) == 11:
            try:
                from youtube_transcript_api import YouTubeTranscriptApi
                transcript_list = YouTubeTranscriptApi().list(video_id)
                
                t_obj = None
                for t in transcript_list:
                    if 'en' in t.language_code:
                        t_obj = t
                        break
                        
                if t_obj:
                    t_data = t_obj.fetch()
                    transcription["segments"] = [
                        {"start": seg.start, "end": seg.start + seg.duration, "text": seg.text.replace("\n", " ").strip()}
                        for seg in t_data
                    ]
                    transcription["full_text"] = " ".join([seg.text.replace("\n", " ").strip() for seg in t_data])
                    print(f"   ✅ Success! Fetched exact match transcript from YouTube servers ({len(transcription['segments'])} segments)")
                else:
                    print("   ⚠️  No English transcript found on YouTube.")
            except ImportError:
                 print("   ⚠️  youtube_transcript_api library missing. Falling back...")
            except Exception as e:
                print(f"   ⚠️  YouTube Transcript API failed ({e}). Falling back...")
        
        # 2b. Fallback: Run local Whisper AI if Youtube native transcription failed
        if not transcription["full_text"].strip() and audio_path and audio_path.exists():
            print("\n🎤 Transcribing with local Whisper...")
            try:
                import whisper
                import ssl
                ssl._create_default_https_context = ssl._create_unverified_context
                model = whisper.load_model("base")
                print("   Transcribing (2-3 minutes)...")
                result = model.transcribe(str(audio_path), language="en")
                
                transcription["full_text"] = result["text"]
                transcription["segments"] = [
                    {"start": s["start"], "end": s["end"], "text": s["text"]}
                    for s in result.get("segments", [])
                ]
                print(f"   ✅ Whisper Done! ({len(transcription['segments'])} segments)")
            except Exception as e:
                print(f"   ⚠️  Whisper Error: {e}")
                
        # Minimal explicit fallback if transcription is empty (Whisper missing/FFmpeg missing)
        if not transcription["full_text"].strip():
            print("   ⚠️  Transcription failed completely. Initializing blank placeholder.")
            # Do NOT inject misleading testing strings—this poisoned the UI.
            transcription["full_text"] = ""
            transcription["segments"] = []
        
        # 3. Extract entities
        print("\n🔍 Extracting entities...")
        buildings = []
        text_lower = transcription["full_text"].lower()
        
        for landmark in self.sheffield_landmarks:
            if landmark.lower() in text_lower:
                buildings.append(landmark)
        
        print(f"   ✅ Found buildings: {', '.join(buildings) if buildings else 'None'}")
        
        # 4. Save results
        metadata = {
            "video_file": self.video_name,
            "transcription": transcription["full_text"],
            "buildings": buildings,
            "segments": transcription["segments"]
        }
        
        json_path = self.work_dir / f"{self.video_name}_metadata.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        print(f"\n✅ Saved: {json_path}")
        
        # 5. Generate SRT
        if transcription["segments"]:
            srt_path = self.work_dir / f"{self.video_name}.srt"
            with open(srt_path, 'w', encoding='utf-8') as f:
                for i, seg in enumerate(transcription["segments"], 1):
                    f.write(f"{i}\n")
                    f.write(f"{self._fmt(seg['start'])} --> {self._fmt(seg['end'])}\n")
                    f.write(f"{seg['text']}\n\n")
            print(f"✅ Saved: {srt_path}")
        
        print("\n" + "="*60)
        print("✅ DONE! Check the 'output' folder")
        print("="*60)
    
    def _fmt(self, seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

if __name__ == "__main__":
    import glob
    
    videos = glob.glob("*.mp4")
    if not videos:
        print("❌ No MP4 files found!")
        exit()
    
    print(f"📹 Found: {videos[0]}")
    processor = VideoProcessor(videos[0])
    processor.process()