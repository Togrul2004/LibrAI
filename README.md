# 🎓 LibrAI — University of Sheffield Video Intelligence Platform

**Empowering students and researchers with AI-driven video content extraction, accessibility, and discovery.**

---

## 🎯 The Vision
Modern education happens on video, but video content is traditionally "dark data"—unsearchable, inaccessible, and hard to navigate. **LibrAI** transforms the University of Sheffield's video library into a rich, searchable intelligence asset.

---

## 🚀 Core Features

### 📡 Intelligent Ingestion
- **URL Upload Support**: Directly paste YouTube URLs to ingest them into the library.
- **Automated Download**: Uses `yt-dlp` to fetch high-quality media for processing.
- **Native Caption Proxy**: Automatically fetches professional YouTube captions if available, falling back to AI transcription only when necessary.

### 🧠 Advanced AI Pipeline
- **OpenAI Whisper Transcription**: 95%+ accurate English transcription for even the noisest lecture halls.
- **Smart Summarization**: Generates real human-readable summaries (not just extracted sentences) tailored to the Sheffield academic context.
- **Entity Extraction**: Automatically detects campus buildings (The Diamond, Arts Tower, Information Commons, etc.) and academic subjects.
- **Topic & Theme Classification**: Categorizes videos into "Day in the Life," "Research Showcase," "Course Information," and more.

### 🔍 Discovery & Accessibility
- **High-Fidelity Search**: Fuzzy search through full transcripts and metadata.
- **Detail Panel**: Interactive side-panel featuring synced subtitles, AI summaries, and key metadata chips.
- **SRT Generation**: Automatically generates `.srt` subtitle files for every processed video to improve accessibility.

---

## 🛠️ Technical Stack
- **Backend**: Python 3.14+ / Flask
- **Processing**: OpenAI Whisper, FFmpeg, yt-dlp
- **Frontend**: Vanilla HTML5, CSS3 (Modern UI/UX), JavaScript (ES6+)
- **Storage**: JSON-based metadata lake (`output/` + `AI_ANALYSIS_MASTER.json`)

---

## 📂 Project Structure

| File | Purpose |
|------|---------|
| `api_server.py` | The main Flask backend managing video uploads and UI data. |
| `quick_fix.py` | The core processing engine for transcription and extraction. |
| `batch_all_videos.py` | Orchestrator that processes all videos in the `videos/` folder. |
| `ai_summarizer_v3.py` | The "Brain" that generates AI summaries and the master library JSON. |
| `index.html` | The high-fidelity platform frontend dashboard. |
| `videos/` | Storage for downloaded/local `.mp4` video files. |
| `output/` | The metadata repository containing `_metadata.json` and `.srt` files. |

---

## ⏱️ Quick Start

### 1. Requirements
Ensure you have Python 3.14 and FFmpeg installed.
```bash
# Mac
brew install ffmpeg
```

### 2. Install Dependencies
```bash
pip install flask flask_cors yt-dlp openai-whisper youtube-transcript-api
```

### 3. Start the Platform
Run the API server:
```bash
python api_server.py
```
Open **`http://localhost:5001`** in your browser to access the dashboard.

### 4. Batch Process Existing Videos
If you add videos directly to the `videos/` folder:
```bash
python batch_all_videos.py
python ai_summarizer_v3.py
```

---

## 📊 Analytics & Searching
- **Run Analytics**: `python analytics.py` to see common buildings, topics, and word clouds.
- **Terminal Search**: `python advanced_search.py "search term"` to find specific moments in transcripts.

---

**Built for the University of Sheffield**  
*Turning video collections into searchable knowledge.*
# video-content-extraction-ai
