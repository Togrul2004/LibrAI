#!/usr/bin/env python3
"""
API Server for Sheffield Video Library
Allows adding videos through web interface
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import sys
import shutil
import os
import json
import re
from pathlib import Path
import threading

app = Flask(__name__)
CORS(app)  # Allow requests from web dashboard

# Directory configuration
OUTPUT_DIR = 'output'
VIDEO_DIR = 'videos'

# Store processing status
processing_status = {}

# Serve Dashboard static files
@app.route('/api/delete-video/<video_file>', methods=['DELETE'])
def delete_video(video_file):
    """Delete a video and its metadata"""
    try:
        # Delete physical files
        metadata_file = os.path.join(OUTPUT_DIR, f"{video_file}_metadata.json")
        csv_file = os.path.join(OUTPUT_DIR, f"{video_file}_metadata.csv")
        srt_file = os.path.join(OUTPUT_DIR, f"{video_file}_subtitles.srt")
        summary_file = os.path.join(OUTPUT_DIR, f"{video_file}_AI_summary.json")
        video_path = os.path.join(VIDEO_DIR, f"{video_file}.mp4")
        
        deleted_files = []
        for filepath in [metadata_file, csv_file, srt_file, summary_file, video_path]:
            if os.path.exists(filepath):
                os.remove(filepath)
                deleted_files.append(os.path.basename(filepath))
        
        # UPDATE MASTER JSON - This is the critical part!
        master_path = os.path.join(OUTPUT_DIR, 'AI_ANALYSIS_MASTER.json')
        if os.path.exists(master_path):
            with open(master_path, 'r', encoding='utf-8') as f:
                videos = json.load(f)
            
            # Remove this video from the list
            videos = [v for v in videos if v.get('video_file') != video_file]
            
            # Write back to file
            with open(master_path, 'w', encoding='utf-8') as f:
                json.dump(videos, f, indent=2, ensure_ascii=False)
        
        return jsonify({"success": True, "message": f"Deleted {video_file}", "deleted_files": deleted_files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/')
def serve_dashboard():
    """Serve the main dashboard page from the root folder"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static assets from root or website folder"""
    if os.path.exists(path):
        return send_from_directory('.', path)
    if os.path.exists(os.path.join('website', path)):
        return send_from_directory('website', path)
    return jsonify({'error': 'File not found'}), 404

def is_valid_youtube_url(url):
    """Validate YouTube URL for security"""
    youtube_patterns = [
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+',
        r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(https?://)?(www\.)?youtu\.be/[\w-]+'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False

def process_video_background(video_url, task_id):
    """Process video in background thread"""
    try:
        processing_status[task_id] = {
            'status': 'downloading',
            'message': 'Downloading video from YouTube...',
            'progress': 10
        }
        
        # Download video
        videos_dir = Path('videos')
        videos_dir.mkdir(exist_ok=True)
        
        ytdlp_bin = shutil.which('yt-dlp') or '/Library/Frameworks/Python.framework/Versions/3.14/bin/yt-dlp'
        download_cmd = [
            ytdlp_bin,
            '-f', 'best[height<=720]',
            '--output', str(videos_dir / '%(upload_date)s_%(id)s.mp4'),
            video_url
        ]
        
        result = subprocess.run(download_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result.returncode != 0:
            processing_status[task_id] = {
                'status': 'error',
                'message': f'Download failed: {result.stderr}',
                'progress': 0
            }
            return
            
        # Dynamically determine the video ID extracted by yt-dlp
        downloaded_file = None
        video_id = None
        file_match = re.search(r'videos[/\\]([\w-]+)\.mp4', result.stdout)
        if file_match:
            video_id = file_match.group(1)
        else:
            print(f"Warning: Could not parse video ID from output: {result.stdout}")
        
        processing_status[task_id] = {
            'status': 'transcribing',
            'message': 'Transcribing video with Whisper AI...',
            'progress': 40
        }
        
        # Process the video
        process_cmd = [sys.executable, 'batch_all_videos.py']
        result = subprocess.run(process_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result.returncode != 0:
            processing_status[task_id] = {
                'status': 'error',
                'message': f'Processing failed: {result.stderr}',
                'progress': 0
            }
            return
        
        processing_status[task_id] = {
            'status': 'analyzing',
            'message': 'Generating AI summary...',
            'progress': 70
        }
        
        # Generate AI summary
        summary_cmd = [sys.executable, 'ai_summarizer_v3.py']
        result = subprocess.run(summary_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result.returncode != 0:
            processing_status[task_id] = {
                'status': 'error',
                'message': f'AI analysis failed: {result.stderr}',
                'progress': 0
            }
            return
        
        # Final Validation Layer
        # Block 'complete' status if the final transcription genuinely failed
        is_success = True
        error_msg = 'Video successfully added to library!'
        
        if video_id:
            metadata_path = Path('output') / f'{video_id}_metadata.json'
            if not metadata_path.exists():
                is_success = False
                error_msg = 'Transcription missing. Process aborted due to audio extraction failure.'
            else:
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        test_data = json.load(f)
                        if not test_data.get('transcription', '').strip():
                            is_success = False
                            error_msg = 'Transcription engine returned an empty transcript.'
                except Exception as e:
                    is_success = False
                    error_msg = f'Transcription validation failed: {str(e)}'
        
        if is_success:
            processing_status[task_id] = {
                'status': 'complete',
                'message': error_msg,
                'progress': 100
            }
        else:
            processing_status[task_id] = {
                'status': 'failed',
                'message': error_msg,
                'progress': 0
            }
        
    except Exception as e:
        processing_status[task_id] = {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'progress': 0
        }

@app.route('/api/add-video', methods=['POST'])
def add_video():
    """Add a new YouTube video"""
    data = request.json
    video_url = data.get('url', '').strip()
    
    # Validate URL
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    if not is_valid_youtube_url(video_url):
        return jsonify({'error': 'Invalid YouTube URL. Only YouTube links are allowed.'}), 400
    
    # Generate task ID
    import time
    task_id = f"task_{int(time.time())}"
    
    # Start processing in background
    processing_status[task_id] = {
        'status': 'queued',
        'message': 'Video added to processing queue...',
        'progress': 0
    }
    
    thread = threading.Thread(target=process_video_background, args=(video_url, task_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'task_id': task_id,
        'message': 'Video processing started'
    })

@app.route('/api/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """Get processing status"""
    status = processing_status.get(task_id, {
        'status': 'unknown',
        'message': 'Task not found',
        'progress': 0
    })
    return jsonify(status)

@app.route('/api/videos', methods=['GET'])
def get_videos():
    """Get all processed videos"""
    try:
        with open('output/AI_ANALYSIS_MASTER.json', 'r', encoding='utf-8') as f:
            videos = json.load(f)
        return jsonify(videos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transcript/<video_id>', methods=['GET'])
def get_transcript(video_id):
    """
    Return transcript text for a specific video.
    Reads from the existing individual _metadata.json file.
    No processing logic is touched — pure read-only data retrieval.
    """
    # Sanitise the video_id to prevent path traversal
    safe_id = re.sub(r'[^a-zA-Z0-9_\-]', '', video_id)
    metadata_path = Path('output') / f'{safe_id}_metadata.json'

    if not metadata_path.exists():
        return jsonify({'error': 'Transcript not found', 'video_id': safe_id}), 404

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return jsonify({
            'video_id': safe_id,
            'transcription': metadata.get('transcription', ''),
            'segments': metadata.get('segments', [])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get library statistics"""
    try:
        with open('output/AI_ANALYSIS_MASTER.json', 'r', encoding='utf-8') as f:
            videos = json.load(f)
        
        buildings = set()
        topics = set()
        
        for video in videos:
            buildings.update(video.get('buildings', []))
            topics.update(video.get('topics', []))
        
        return jsonify({
            'total_videos': len(videos),
            'total_buildings': len(buildings),
            'total_topics': len(topics)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 Sheffield Video Library API Server")
    print("="*70)
    print("📡 Backend API: http://localhost:5001/api")
    print("🌐 Dashboard:   http://localhost:5001/")
    print("="*70)
    print("\nDocumentation:")
    print("  /              - Access the LibrAI Web Dashboard")
    print("  /api/videos    - Get processed video metadata")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)