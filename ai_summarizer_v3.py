#!/usr/bin/env python3
"""
TRUE AI Summarizer - Generates Real Summaries
Not just extracted sentences!
"""

import json
import glob
import re
from pathlib import Path
from collections import Counter

def generate_real_summary(text, video_file):
    """
    Generate an ACTUAL summary, not extracted sentences
    """
    if not text or len(text) < 50:
        return "Video content not available for analysis."
    
    text_lower = text.lower()
    
    # Detect video type and generate appropriate summary
    
    # Pattern 1: Day in the Life
    if any(phrase in text_lower for phrase in ['day in', 'typical day', 'morning', 'wake up', 'get ready']):
        # Extract student info
        subject = extract_subject(text)
        year = extract_year(text)
        
        summary = f"A day in the life video following a"
        if year:
            summary += f" {year} year"
        summary += " student"
        if subject:
            summary += f" studying {subject}"
        summary += " at the University of Sheffield."
        
        # Add what they do
        activities = []
        if any(word in text_lower for word in ['lecture', 'class', 'seminar']):
            activities.append("attending lectures")
        if any(word in text_lower for word in ['library', 'study', 'revision']):
            activities.append("studying")
        if any(word in text_lower for word in ['coffee', 'lunch', 'eat']):
            activities.append("socializing")
        
        if activities:
            summary += f" The video shows {', '.join(activities[:2])} and daily campus activities."
        
        return summary
    
    # Pattern 2: Student/Staff Interview
    elif any(phrase in text_lower for phrase in ['my name is', "i'm a student", "i study", "i'm studying"]):
        name = extract_name(text)
        subject = extract_subject(text)
        role = extract_role(text)
        
        if role and ('lecturer' in role.lower() or 'professor' in role.lower()):
            summary = f"Interview with a {role} at the University of Sheffield"
        else:
            summary = "Student interview featuring a"
            year = extract_year(text)
            if year:
                summary += f" {year} year"
            summary += " student"
        
        if subject:
            summary += f" studying {subject}"
        summary += " at the University of Sheffield."
        
        # Add what they talk about
        topics = []
        if any(word in text_lower for word in ['chose', 'decided', 'selected']):
            topics.append("their reasons for choosing Sheffield")
        if any(word in text_lower for word in ['experience', 'enjoy', 'love']):
            topics.append("their university experience")
        if any(word in text_lower for word in ['career', 'future', 'graduate']):
            topics.append("future career plans")
        
        if topics:
            summary += f" They discuss {' and '.join(topics[:2])}."
        
        return summary
    
    # Pattern 3: Research Showcase
    elif any(phrase in text_lower for phrase in ['research', 'my work', 'investigating', 'project']):
        summary = "Research showcase from the University of Sheffield"
        
        subject = extract_subject(text)
        if subject:
            summary += f" focusing on {subject}"
        
        if any(word in text_lower for word in ['phd', 'doctorate', 'doctoral']):
            summary += ". The video features PhD research"
        elif any(word in text_lower for word in ['masters', 'master\'s', 'postgraduate']):
            summary += ". The video highlights postgraduate research"
        
        summary += " and its real-world applications."
        
        return summary
    
    # Pattern 4: Course Information
    elif any(phrase in text_lower for phrase in ['course', 'degree', 'programme', 'modules']):
        subject = extract_subject(text)
        
        summary = "Course information video about"
        if subject:
            summary += f" {subject}"
        else:
            summary += " programs"
        summary += " at the University of Sheffield."
        
        if any(word in text_lower for word in ['undergraduate', 'bachelor']):
            summary += " The video covers undergraduate degree options"
        elif any(word in text_lower for word in ['postgraduate', 'masters', 'master\'s']):
            summary += " The video explores postgraduate opportunities"
        
        if any(word in text_lower for word in ['module', 'taught', 'learn']):
            summary += " and what students will learn."
        
        return summary
    
    # Pattern 5: Campus Tour
    elif any(phrase in text_lower for phrase in ['tour', 'campus', 'facilities', 'building', 'welcome to']):
        summary = "Campus tour of the University of Sheffield"
        
        # Check for specific buildings
        buildings = extract_buildings_from_text(text)
        if buildings:
            summary += f" featuring {buildings[0]}"
            if len(buildings) > 1:
                summary += f" and {buildings[1]}"
        
        summary += ". The video showcases university facilities and student spaces."
        
        return summary
    
    # Default: Generic summary
    else:
        subject = extract_subject(text)
        
        summary = "University of Sheffield video"
        if subject:
            summary += f" related to {subject}"
        
        if any(word in text_lower for word in ['student', 'study', 'learn']):
            summary += " featuring student experiences and campus life"
        
        summary += "."
        
        return summary

def extract_name(text):
    """Extract person's name"""
    patterns = [
        r"my name is ([A-Z][a-z]+ [A-Z][a-z]+)",
        r"my name is ([A-Z][a-z]+)",
        r"i'm ([A-Z][a-z]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None

def extract_subject(text):
    """Extract subject/course being studied"""
    subjects = {
        'mathematics': ['mathematics', 'maths', 'math'],
        'engineering': ['engineering', 'engineer'],
        'medicine': ['medicine', 'medical', 'biomedical'],
        'law': ['law', 'legal'],
        'computer science': ['computer science', 'computing', 'software'],
        'business': ['business', 'management', 'finance'],
        'chemistry': ['chemistry', 'chemical'],
        'biology': ['biology', 'biological'],
        'physics': ['physics'],
        'psychology': ['psychology', 'psychological'],
        'architecture': ['architecture', 'architectural'],
        'journalism': ['journalism', 'journalist'],
        'history': ['history'],
        'english': ['english literature', 'english language'],
        'sociology': ['sociology', 'social'],
        'statistics': ['statistics', 'statistical']
    }
    
    text_lower = text.lower()
    
    # Look for "studying X" or "study X" patterns
    study_match = re.search(r'study(?:ing)?\s+([^,\.]+?)(?:\s+at|\s+with|\s+for|,|\.)', text_lower)
    if study_match:
        subject_text = study_match.group(1).strip()
        for subject, keywords in subjects.items():
            if any(kw in subject_text for kw in keywords):
                return subject
    
    # Look for degree mentions
    degree_match = re.search(r'degree in ([^,\.]+)', text_lower)
    if degree_match:
        subject_text = degree_match.group(1).strip()
        for subject, keywords in subjects.items():
            if any(kw in subject_text for kw in keywords):
                return subject
    
    # Look for "X student" or "student of X"
    student_match = re.search(r'([^,\.]+?)\s+student', text_lower)
    if student_match:
        subject_text = student_match.group(1).strip()
        for subject, keywords in subjects.items():
            if any(kw in subject_text for kw in keywords):
                return subject
                
    # Look for "course in X" or "student of X"
    course_match = re.search(r'(?:course in|student of)\s+([^,\.]+)', text_lower)
    if course_match:
        subject_text = course_match.group(1).strip()
        for subject, keywords in subjects.items():
            if any(kw in subject_text for kw in keywords):
                return subject
                
    # No more broad generic keyword search - we only want EXPLICIT subject declarations.
    return None

def extract_year(text):
    """Extract year of study"""
    patterns = [
        r'(first|second|third|final) year',
        r'year (one|two|three|four|1|2|3|4)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            year_map = {
                'first': 'first', 'one': 'first', '1': 'first',
                'second': 'second', 'two': 'second', '2': 'second',
                'third': 'third', 'three': 'third', '3': 'third',
                'final': 'final', 'four': 'final', '4': 'final'
            }
            year_str = match.group(1).lower()
            return year_map.get(year_str, year_str)
    
    return None

def extract_role(text):
    """Extract person's role (lecturer, professor, etc.)"""
    roles = ['lecturer', 'professor', 'researcher', 'teaching assistant', 'PhD student']
    
    for role in roles:
        if role in text.lower():
            return role
    
    return None

def extract_buildings_from_text(text):
    """Extract Sheffield building names"""
    buildings = [
        'Diamond', 'The Wave', 'Information Commons', 'Arts Tower',
        'Firth Court', 'Western Bank Library', 'Students Union',
        'Octagon', 'Alfred Denny Building', 'Jessop West',
        'Endcliffe', 'Ranmoor', 'Allen Court', 'Stephenson',
        'St Vincent', 'Broad Lane', 'Mappin'
    ]
    
    found = []
    for building in buildings:
        if building.lower() in text.lower():
            found.append(building)
    
    return found

def extract_topics(text, content_type="", explicit_subject=None):
    """Extract academic topics with rigorous thresholding to prevent false positives"""
    topics = []
    text_lower = text.lower()
    
    # Generic videos shouldn't be over-classified academically unless evidence is very strong
    is_generic = content_type in ["Campus Life", "Events", "Accommodation", "International", "Facilities"]
    
    # Map explicit string from extract_subject to main Academic Topic headers
    subject_to_topic = {
        'mathematics': 'Mathematics', 'engineering': 'Engineering', 'medicine': 'Medicine',
        'law': 'Law', 'computer science': 'Computer Science', 'business': 'Business',
        'chemistry': 'Science', 'biology': 'Biosciences', 'physics': 'Science', 'psychology': 'Psychology',
        'architecture': 'Architecture', 'journalism': 'Arts & Humanities', 
        'history': 'Arts & Humanities', 'english': 'Arts & Humanities', 'sociology': 'Arts & Humanities', 
        'statistics': 'Mathematics'
    }
    
    # Define signals: Strong (3pts) and Weak (1pt each)
    academic_signals = {
        'Engineering': {
            'strong': [r'engineering degree', r'faculty of engineering', r'civil engineering', r'mechanical engineering', r'software engineering', r'aerospace'],
            'weak': [r'\bengineering\b', r'\bengineer\b', r'\bmechanical\b', r'\bcivil\b', r'\bmechatronics\b']
        },
        'Medicine': {
            'strong': [r'medical school', r'medicine degree', r'school of medicine'],
            'weak': [r'\bmedicine\b', r'\bmedical\b', r'\bhealthcare\b', r'\bclinical\b']
        },
        'Science': {
            'strong': [r'science degree', r'faculty of science', r'chemistry lab', r'physics lab'],
            'weak': [r'\bscience\b', r'\bchemistry\b', r'\bphysics\b']
        },
        'Biosciences': {
            'strong': [r'bioscience', r'biomedical science', r'molecular biology', r'zoology degree'],
            'weak': [r'\bbiosciences\b', r'\bbiology\b', r'\bzoology\b', r'\bgenetics\b', r'\bbiomedical\b']
        },
        'Psychology': {
            'strong': [r'psychology degree', r'department of psychology', r'clinical psychology', r'cognitive psychology'],
            'weak': [r'\bpsychology\b', r'\bpsychological\b', r'\bneuroscience\b']
        },
        'Architecture': {
            'strong': [r'architecture degree', r'school of architecture', r'landscape architecture'],
            'weak': [r'\barchitecture\b', r'\barchitectural\b']
        },
        'Law': {
            'strong': [r'law degree', r'school of law', r'law school', r'legal practice'],
            'weak': [r'\blaw\b', r'\blegal\b', r'\bjurisprudence\b']
        },
        'Business': {
            'strong': [r'business school', r'management degree', r'finance degree', r'\bmba\b'],
            'weak': [r'\bbusiness\b', r'\bmanagement\b', r'\bfinance\b', r'\beconomics\b', r'\baccounting\b']
        },
        'Arts & Humanities': {
            'strong': [r'arts degree', r'humanities', r'literature degree', r'faculty of arts', r'fine art'],
            'weak': [r'\bart\b', r'\bliterature\b', r'\bphilosophy\b', r'\bhistory\b', r'\bjournalism\b']
        },
        'Computer Science': {
            'strong': [r'computer science', r'artificial intelligence', r'machine learning', r'software development'],
            'weak': [r'\bprogramming\b', r'\bsoftware\b', r'\bcomputing\b', r'\bcybersecurity\b']
        },
        'Mathematics': {
            'strong': [r'mathematics degree', r'maths department', r'school of mathematics', r'statistics degree'],
            'weak': [r'\bmathematics\b', r'\bmaths\b', r'\bmath\b', r'\bstatistics\b']
        }
    }
    
    for topic, signals in academic_signals.items():
        score = 0
        
        # Check strong context phrases
        for kw in signals['strong']:
            if re.search(kw, text_lower):
                score += 3
                
        # Check weak context phrases (cap at 2 points to avoid repetitive noise like "art, art, art")
        weak_score = 0
        for kw in signals['weak']:
            matches = len(re.findall(kw, text_lower))
            if matches > 0:
                weak_score += min(matches, 2)
        score += min(weak_score, 2)
        
        # Did another rigid extractor (which checks "I study X" phrases strictly) find this?
        if explicit_subject and subject_to_topic.get(explicit_subject) == topic:
            score += 4
            
        # generic vlog content needs far stronger signals to get tagged academically (4+ points)
        # instructional/academic content only needs moderate signals (3+ points)
        threshold = 4 if is_generic else 3
        
        if score >= threshold:
            topics.append(topic)
            
    # Safer fallbacks if confidence is weak or video is un-academic
    if not topics:
        if is_generic or "accommodation" in text_lower or "student union" in text_lower:
            topics.append("Campus & Student Life")
        else:
            topics.append("General University Content")
            
    return topics[:2]

def extract_themes(text):
    """Extract Sheffield student life themes and specific experience tags"""
    themes = []
    
    categories = {
        'Student Experience': ['student experience', 'student life', 'living in', 'community'],
        'Day in the Life': ['day in the life', 'typical day', 'my day', 'morning routine'],
        'Campus Tour': ['campus tour', 'show you around', 'showing you around', 'facilities tour'],
        'Study Spaces': ['study space', 'silent study', 'group study', 'studying at'],
        'Libraries': ['library', 'western bank', 'information commons', 'diamond library'],
        'Labs': ['lab', 'laboratory', 'practical session', 'workshop', 'experiments'],
        'Wellbeing': ['wellbeing', 'mental health', 'support', 'stress'],
        'Societies': ['society', 'club', 'sports team', 'varsity', 'extracurricular'],
        'Employability': ['employability', 'cv', 'careers service', 'placement', 'internship', 'job'],
        'Open Day': ['open day', 'visiting sheffield', 'applicant day'],
        'Applications': ['applying', 'ucas', 'personal statement', 'clearing', 'application'],
        'Postgraduate Study': ['postgraduate', 'masters', 'phd', 'researcher', 'dissertation'],
        'Undergraduate Study': ['undergraduate', 'bachelor', 'first year', 'second year', 'third year', 'final year'],
        'Facilities': ['facilities', 'equipment', 'maker space', 'investment fund', 'tools'],
        'Student Union': ['student union', 'students union', 'the su', 'foundry']
    }
    
    text_lower = text.lower()
    for category, keywords in categories.items():
        if any(re.search(rf'\b{kw}\b', text_lower) for kw in keywords):
            themes.append(category)
            
    return themes[:4]

def extract_primary_category(text):
    """Extract the primary video category using keyword term matching"""
    text_lower = text.lower()
    
    categories = {
        'Research': ['research', 'investigating', 'finding', 'postdoc', 'phd study', 'publishing', 'laboratories'],
        'Admissions': ['open day', 'applying', 'applicant', 'ucas', 'clearing', 'admission', 'entry requirements', 'personal statement'],
        'Careers': ['careers', 'employability', 'placement', 'internship', 'job', 'graduating', 'career service', 'alumni'],
        'Accommodation': ['accommodation', 'student village', 'halls', 'rent', 'living in sheffield', 'endcliffe', 'ranmoor'],
        'International': ['international student', 'visa', 'moving to the uk', 'studying abroad', 'overseas', 'culture shock'],
        'Student Support': ['wellbeing', 'support', 'mental health', 'student services', 'disability', 'counselling', 'financial support', 'scholarship'],
        'Events': ['event', 'varsity', 'graduation ceremony', 'freshers week', 'intro week', 'festival', 'concert'],
        'Facilities': ['facilities', 'equipment', 'labs', 'library', 'study spaces', 'maker space', 'investment fund', 'trading room'],
        'Academic': ['degree', 'module', 'assignment', 'lectures', 'seminars', 'tutor', 'coursework', 'exams'],
        'Campus Life': ['societies', 'campus tour', 'day in the life', 'typical day', 'student union', 'students union', 'su', 'going out', 'friends']
    }
    
    scores = {c: 0 for c in categories}
    for cat, keywords in categories.items():
        for kw in keywords:
            # Prevent substring traps ('rent' -> 'different', 'event' -> 'prevent')
            matches = len(re.findall(rf'\b{kw}\b', text_lower))
            scores[cat] += matches
            
    best_cat = "Campus Life"
    if any(re.search(rf'\b{m}\b', text_lower) for m in ['study', 'course']):
        best_cat = "Academic"
        
    highest_score = 0
    for cat, score in scores.items():
        if score > highest_score and score >= 2: # Require at least 2 mentions to override defaults
            highest_score = score
            best_cat = cat
            
    return best_cat

def evaluate_transcript_quality(text):
    """
    Quality control layer. 
    Returns False if the transcript appears to be highly noisy, repetitive (Whisper hallucination),
    or otherwise too low quality for a confident summary.
    """
    if not text:
        return False
        
    text_lower = text.lower()
    words = text_lower.split()
    
    # 1. Too short to be meaningful for full-video extraction
    if len(words) < 20:
        return False
        
    # 2. Whisper hallucination: Insane word length (e.g. broken spaces)
    longest_word = max(words, key=len) if words else ""
    if len(longest_word) > 40 and "http" not in longest_word:
        return False
        
    # 3. Whisper hallucination: Extreme repetition loop checking
    if len(words) > 30:
        from collections import Counter
        word_counts = Counter(words)
        most_common = word_counts.most_common(1)[0]
        # If a single word makes up >35% of a long transcript, it's highly likely a loop
        if most_common[1] / len(words) > 0.35:
            return False
            
    # 4. Specific known Whisper loop patterns (e.g. empty room static turning into "thank you")
    if text_lower.count("thank you") > max(10, len(words) * 0.1):  
        return False
        
    # 5. Non-English / Gibberish character ratio check (for foreign language leaks)
    non_ascii_count = sum(1 for char in text if ord(char) > 127)
    if (non_ascii_count / len(text)) > 0.15:
        return False
        
    return True

def analyze_video(json_path):
    """Analyze video and generate REAL summary"""
    
    import os
    processed_at = os.stat(json_path).st_mtime if os.path.exists(json_path) else 0
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    transcript = data.get('transcription', '')
    video_file = data['video_file']
    buildings = data.get('buildings', [])
    
    # Quality Control Check
    is_transcript_valid = evaluate_transcript_quality(transcript)
    
    if not is_transcript_valid:
        # Fallback for poor quality transcripts
        summary = "Limited transcript quality — summary may be incomplete or unavailable due to audio issues."
        topics = []
        themes = []
        content_type = "University Content"
        key_points = []
    else:
        # Generate REAL summary
        summary = generate_real_summary(transcript, video_file)
        
        # First extract confident signals
        content_type = extract_primary_category(transcript)
        subject = extract_subject(transcript)
        
        # Extract metadata
        topics = extract_topics(transcript, content_type=content_type, explicit_subject=subject)
        themes = extract_themes(transcript)
        
        # Extract key points
        key_points = []
        name = extract_name(transcript)
        year = extract_year(transcript)
        
        if name:
            key_points.append(f"Features: {name}")
        if subject:
            key_points.append(f"Subject: {subject}")
        if year:
            key_points.append(f"Year: {year.title()}")
            
        key_points = key_points[:3]
    
    analysis = {
        'video_file': video_file,
        'content_type': content_type,
        'ai_summary': summary,
        'topics': topics,
        'themes': themes,
        'key_points': key_points[:3],
        'buildings': buildings,
        'transcript_length': len(transcript.split()),
        'duration_estimate': len(data.get('segments', [])) * 6,
        'processed_at': processed_at
    }
    
    return analysis

def analyze_all_videos():
    """Generate REAL summaries for all videos"""
    
    json_files = glob.glob("output/*_metadata.json")
    
    if not json_files:
        print("No videos found")
        return
    
    print("\nTRUE AI SUMMARIZER - Generating Real Summaries")
    print("="*70)
    print(f"Processing {len(json_files)} videos...\n")
    
    analyses = []
    
    for i, json_file in enumerate(json_files, 1):
        print(f"Generating summary {i}/{len(json_files)}: {Path(json_file).stem[:30]}...", end='\r')
        
        analysis = analyze_video(json_file)
        analyses.append(analysis)
        
        # Save
        output_path = Path(json_file).parent / f"{analysis['video_file']}_AI_summary.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    
    # Show samples
    print("\n Sample Generated Summaries:\n")
    for i, analysis in enumerate(analyses[:5], 1):
        print(f"{i}. {analysis['video_file']}")
        print(f"    {analysis['content_type']}")
        print(f"    {analysis['ai_summary']}\n")
    
    # Save master
    master_path = Path("output") / "AI_ANALYSIS_MASTER.json"
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(analyses, f, indent=2, ensure_ascii=False)
    
    print("="*70)
    print(f" Complete! Generated {len(analyses)} REAL summaries")
    print(f" Saved to: {master_path}")

if __name__ == "__main__":
    analyze_all_videos()