# ⚡ HACKATHON QUICK REFERENCE CARD
## Sheffield Video Metadata Extractor - FREE VERSION

---

## 🚀 SETUP (15 minutes)

```bash
# Install Whisper (FREE transcription)
pip install openai-whisper

# Install FFmpeg
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # Mac

# Optional extras
pip install pillow pytesseract spacy
```

---

## ▶️ RUN IT

```bash
python hackathon_extractor.py
```

**That's it!** It processes the video and creates:
- ✅ JSON metadata
- ✅ CSV for Excel/databases  
- ✅ SRT subtitles for YouTube

---

## 📊 WHAT IT DOES

1. **Extracts audio** from video
2. **Transcribes** with Whisper (95%+ accuracy)
3. **Samples frames** every 15 seconds
4. **Detects Sheffield buildings** (Octagon, Diamond, etc.)
5. **Extracts keywords** and topics
6. **Generates subtitles** (SRT format)
7. **Exports** JSON + CSV

---

## ⏱️ SPEED

- **1 video**: 3-4 minutes
- **10 videos**: 30-40 minutes
- **200 videos**: 10-14 hours (or 3-4 hours with parallel processing)

---

## 💰 COST

**£0** - Everything is free and open-source!

---

## 🎯 DEMO POINTS

### What to Show Judges

1. **Before/After**  
   - Before: "Video of campus" (no searchable info)
   - After: Full transcript + buildings + keywords + subtitles

2. **Search Demo**  
   - "Find all videos with the Octagon" → instant results
   - "Find mentions of engineering" → transcript search

3. **Accessibility Win**  
   - Auto-generated subtitles (SRT)
   - Improves access for deaf/hard-of-hearing

4. **Cost Savings**  
   - Manual: £5,000-10,000
   - This system: £0

---

## 🏆 WINNING ARGUMENTS

### Innovation
✅ Uses state-of-the-art Whisper AI  
✅ Fully automated  
✅ Zero manual work

### Impact
✅ Makes 200+ videos searchable  
✅ Saves £10,000+  
✅ Improves accessibility

### Technical Excellence
✅ Clean, documented code  
✅ Free/open-source only  
✅ Scales to thousands of videos

### Practical
✅ Works TODAY  
✅ No special hardware needed  
✅ Easy to maintain

---

## 📝 OUTPUT FILES

**For each video you get:**

1. **JSON** - Full metadata
2. **CSV** - For Excel/databases
3. **SRT** - YouTube subtitles

---

## 🔧 TROUBLESHOOTING

**Whisper slow?**  
→ Use "base" model (faster) or "large" (more accurate)

**Out of memory?**  
→ Process videos one at a time, or use smaller model

**Can't find buildings?**  
→ They're detected from transcription text

---

## 💡 BONUS IDEAS (If Time Allows)

### Easy Wins
- Search interface (Streamlit)
- Statistics dashboard
- Batch processing script

### Advanced
- Speaker identification
- Topic modeling
- Sentiment analysis
- Similar video recommendations

---

## 📞 HELP

**Whisper docs**: https://github.com/openai/whisper  
**FFmpeg docs**: https://ffmpeg.org/documentation.html  
**Python help**: Stack Overflow

---

## ✅ HACKATHON CHECKLIST

Day 1:
- [ ] Install tools
- [ ] Test on 1 video
- [ ] Process 5-10 samples
- [ ] Refine entity extraction

Day 2:
- [ ] Add batch processing
- [ ] Create demo interface
- [ ] Process full sample set
- [ ] Prepare presentation

---

## 🎉 SUCCESS CRITERIA

✅ Transcription working (95%+ accuracy)  
✅ Buildings detected (Octagon, Diamond, etc.)  
✅ Keywords extracted  
✅ SRT subtitles generated  
✅ JSON + CSV exported  
✅ Demo ready

---

## 🎬 DEMO SCRIPT (5 minutes)

**Minute 1**: Problem
- "Library has 200+ videos"
- "No transcriptions or metadata"
- "Can't search, poor accessibility"

**Minute 2**: Solution
- "We built a FREE system"
- "Uses Whisper AI for transcription"
- "Identifies buildings and topics"

**Minute 3**: Live Demo
- Show video processing
- Display transcript
- Search for "Octagon" → results!

**Minute 4**: Impact
- "Makes 200 videos searchable"
- "Saves £10,000 vs manual"
- "Auto-generates subtitles"

**Minute 5**: Q&A
- "It's all free and open-source"
- "Can process 200 videos in 1 day"
- "Easy to maintain and extend"

---

**REMEMBER**: You're not just building a tool—you're solving a real library problem with FREE technology that saves thousands of pounds!

**GO WIN THAT HACKATHON! 🏆**
