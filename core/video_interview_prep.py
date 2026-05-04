"""
Video Interview Preparation System
Comprehensive guide for video interviews with body language and camera tips
"""

from typing import Dict, List, Any

class VideoInterviewPrep:
    """Video interview preparation and coaching"""
    
    def __init__(self):
        self.setup_checklist = [
            "✅ Test your internet connection (minimum 5 Mbps)",
            "✅ Check camera quality and positioning",
            "✅ Test microphone and audio levels",
            "✅ Ensure good lighting (face the light source)",
            "✅ Choose a clean, professional background",
            "✅ Close unnecessary applications",
            "✅ Silence phone and notifications",
            "✅ Have a glass of water nearby",
            "✅ Keep resume and notes handy",
            "✅ Test the video platform beforehand"
        ]
        
        self.camera_tips = {
            "positioning": [
                "📹 Place camera at eye level",
                "📹 Sit 2-3 feet away from camera",
                "📹 Center yourself in the frame",
                "📹 Leave some space above your head",
                "📹 Ensure your shoulders are visible"
            ],
            "lighting": [
                "💡 Face a window or light source",
                "💡 Avoid backlighting (light behind you)",
                "💡 Use soft, diffused lighting",
                "💡 Avoid harsh shadows on face",
                "💡 Test lighting before interview"
            ],
            "background": [
                "🖼️ Use a clean, uncluttered background",
                "🖼️ Avoid distracting items",
                "🖼️ Neutral colors work best",
                "🖼️ Virtual backgrounds: use sparingly",
                "🖼️ Ensure background is professional"
            ]
        }
        
        self.body_language_tips = {
            "posture": [
                "🧍 Sit up straight with shoulders back",
                "🧍 Lean slightly forward to show engagement",
                "🧍 Keep both feet flat on the floor",
                "🧍 Avoid slouching or leaning back",
                "🧍 Maintain good posture throughout"
            ],
            "eye_contact": [
                "👁️ Look at the camera, not the screen",
                "👁️ Imagine talking to a friend",
                "👁️ Avoid looking away frequently",
                "👁️ Don't stare - blink naturally",
                "👁️ Practice looking at camera lens"
            ],
            "facial_expressions": [
                "😊 Smile naturally and genuinely",
                "😊 Show enthusiasm and interest",
                "😊 Nod to show understanding",
                "😊 Avoid blank or bored expressions",
                "😊 Let your personality shine"
            ],
            "hand_gestures": [
                "🤲 Use natural hand gestures",
                "🤲 Keep hands visible in frame",
                "🤲 Avoid excessive movements",
                "🤲 Don't fidget or play with objects",
                "🤲 Use gestures to emphasize points"
            ],
            "voice": [
                "🎤 Speak clearly and at moderate pace",
                "🎤 Project your voice confidently",
                "🎤 Vary your tone to show enthusiasm",
                "🎤 Pause before answering questions",
                "🎤 Avoid filler words (um, uh, like)"
            ]
        }
        
        self.common_mistakes = [
            "❌ Poor lighting making you hard to see",
            "❌ Looking at screen instead of camera",
            "❌ Sitting too close or too far",
            "❌ Distracting background",
            "❌ Poor audio quality",
            "❌ Wearing distracting clothing/jewelry",
            "❌ Fidgeting or excessive movement",
            "❌ Not testing technology beforehand",
            "❌ Interrupting due to audio delay",
            "❌ Not having backup plan for tech issues"
        ]
        
        self.dress_code = {
            "men": [
                "👔 Solid color shirt (blue, white, gray)",
                "👔 Avoid busy patterns or stripes",
                "👔 Business casual or formal",
                "👔 Well-groomed appearance",
                "👔 Minimal accessories"
            ],
            "women": [
                "👗 Solid color top (professional colors)",
                "👗 Avoid low-cut or revealing clothing",
                "👗 Business casual or formal",
                "👗 Natural makeup",
                "👗 Minimal jewelry"
            ],
            "general": [
                "👕 Dress as you would for in-person interview",
                "👕 Avoid white (can cause glare)",
                "👕 Avoid all black (can look harsh)",
                "👕 Test outfit on camera beforehand",
                "👕 Ensure clothes are clean and pressed"
            ]
        }
    
    def generate_video_prep_guide(self, job: Dict[str, Any]) -> str:
        """Generate comprehensive video interview prep guide"""
        
        guide = f"""
# 🎥 Video Interview Preparation Guide

## Position: {job.get('title', 'N/A')}
## Company: {job.get('company', 'N/A')}

---

## 📋 Pre-Interview Setup Checklist

"""
        for item in self.setup_checklist:
            guide += f"{item}\n"
        
        guide += "\n---\n\n## 📹 Camera Setup\n\n"
        for category, tips in self.camera_tips.items():
            guide += f"### {category.title()}\n"
            for tip in tips:
                guide += f"{tip}\n"
            guide += "\n"
        
        guide += "---\n\n## 🎭 Body Language Mastery\n\n"
        for category, tips in self.body_language_tips.items():
            guide += f"### {category.title()}\n"
            for tip in tips:
                guide += f"{tip}\n"
            guide += "\n"
        
        guide += "---\n\n## 👔 Dress Code\n\n"
        for category, tips in self.dress_code.items():
            guide += f"### {category.title()}\n"
            for tip in tips:
                guide += f"{tip}\n"
            guide += "\n"
        
        guide += "---\n\n## ❌ Common Mistakes to Avoid\n\n"
        for mistake in self.common_mistakes:
            guide += f"{mistake}\n"
        
        guide += """

---

## 🎯 During the Interview

### Opening (First 30 seconds):
1. **Smile and greet warmly**
2. **Thank them for the opportunity**
3. **Show enthusiasm and energy**
4. **Make strong "eye contact" (look at camera)**

### During Questions:
1. **Listen carefully to the full question**
2. **Pause 1-2 seconds before answering**
3. **Structure answers using STAR method**
4. **Maintain eye contact with camera**
5. **Use natural hand gestures**
6. **Show enthusiasm in voice and face**

### Closing:
1. **Thank them for their time**
2. **Reiterate your interest**
3. **Ask about next steps**
4. **End with a smile**

---

## 🚨 Technical Issues - Backup Plan

### If Video Freezes:
- "I apologize, I think my video froze. Can you hear me?"
- Restart camera if needed
- Offer to switch to phone call

### If Audio Cuts Out:
- Have phone number ready as backup
- "I'm having audio issues, may I call you?"

### If Internet Drops:
- Rejoin immediately
- Apologize briefly and continue
- Don't dwell on the issue

---

## 🎬 Practice Exercises

### Exercise 1: Camera Test (5 minutes)
1. Record yourself answering a question
2. Watch the recording
3. Note: posture, eye contact, gestures
4. Adjust and re-record

### Exercise 2: Mock Interview (30 minutes)
1. Set up as if real interview
2. Have friend/family ask questions
3. Practice looking at camera
4. Get feedback on body language

### Exercise 3: Technical Check (10 minutes)
1. Test all equipment
2. Join test meeting
3. Check audio and video quality
4. Ensure backup plan ready

---

## 💡 Pro Tips

### Energy Level:
- **Increase energy by 20%** on video
- Video can make you appear less energetic
- Smile more than you think necessary
- Show enthusiasm in voice and face

### Pacing:
- **Speak slightly slower** than normal
- Account for potential audio delay
- Pause between sentences
- Don't rush your answers

### Engagement:
- **Nod to show understanding**
- Use verbal affirmations ("I see", "That's interesting")
- Ask clarifying questions if needed
- Show active listening

### Professionalism:
- **Treat it like in-person interview**
- Same level of formality
- Same preparation
- Same follow-up

---

## 📝 Final Checklist (Day Before)

- [ ] Test all technology
- [ ] Prepare and test outfit
- [ ] Set up interview space
- [ ] Review company research
- [ ] Prepare questions to ask
- [ ] Print resume and notes
- [ ] Set up good lighting
- [ ] Charge devices
- [ ] Have water ready
- [ ] Plan to log in 5 minutes early

---

## 🎯 Day of Interview

### 30 Minutes Before:
- [ ] Final tech check
- [ ] Use restroom
- [ ] Check appearance
- [ ] Review key points
- [ ] Take deep breaths

### 10 Minutes Before:
- [ ] Close all other applications
- [ ] Silence phone
- [ ] Have notes ready
- [ ] Get comfortable
- [ ] Smile and relax

### 5 Minutes Before:
- [ ] Join meeting
- [ ] Check audio/video one last time
- [ ] Take final deep breath
- [ ] Get ready to shine! ✨

---

## 🌟 Remember

**You've got this!**

- You're qualified for this role
- You've prepared thoroughly
- Technology is just a tool
- Your skills and personality will shine through
- Be yourself and be confident

**Good luck! 🍀**

---

**Pro Tip:** Record yourself practicing and watch it back. 
You'll be surprised what you notice!
"""
        
        return guide


def generate_video_interview_guide(job: Dict[str, Any]) -> str:
    """Quick helper to generate video interview guide"""
    prep = VideoInterviewPrep()
    return prep.generate_video_prep_guide(job)


async def save_video_interview_guide(job: Dict[str, Any], filename: str = None):
    """Generate and save video interview guide"""
    prep = VideoInterviewPrep()
    guide = prep.generate_video_prep_guide(job)
    
    if not filename:
        company = job.get("company", "Company").replace(" ", "_")
        filename = f"video_interview_prep_{company}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(guide)
    
    return filename
