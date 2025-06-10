from django.shortcuts import render
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from deepface import DeepFace
import cv2
import tempfile
import os
import time
QUOTES = [
    "Learning never exhausts the mind. – Leonardo da Vinci",
    "Education is the most powerful weapon to change the world. – Mandela",
    "Success is not the key to happiness. Happiness is the key to success.",
    "The expert in anything was once a beginner.",
    "Dream big. Start small. Act now."
]

def home(request):
    user = request.user
    quote = random.choice(QUOTES)
    return render(request, 'home.html', {'user': user, 'quote': quote})
# views.py


# student/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import os
import tempfile
import cv2
from deepface import DeepFace

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import random
import cv2
import os
import tempfile
from deepface import DeepFace

QUOTES = [
    "Learning never exhausts the mind. – Leonardo da Vinci",
    "Education is the most powerful weapon to change the world. – Mandela",
    "Success is not the key to happiness. Happiness is the key to success.",
    "The expert in anything was once a beginner.",
    "Dream big. Start small. Act now."
]

# 🎯 Home Page View
def home(request):
    quote = random.choice(QUOTES)
    return render(request, 'home.html', {'user': request.user, 'quote': quote})
from django.http import JsonResponse
import cv2
import time
import tempfile
import os
from deepface import DeepFace

def detect_face_emotion(request):
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return JsonResponse({'error': 'Webcam could not be opened'}, status=500)

        time.sleep(2)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return JsonResponse({'error': 'Failed to capture frame'}, status=500)

        # Save frame
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        temp_filename = temp_file.name
        cv2.imwrite(temp_filename, frame)
        temp_file.close()

        print(f"📷 Image saved at: {temp_filename}")

        # Analyze
        result = DeepFace.analyze(img_path=temp_filename, actions=['emotion'], enforce_detection=False)
        print(f"🔍 DeepFace result: {result}")
        emotion = result[0]['dominant_emotion']

        return JsonResponse({'emotion': emotion})

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)



import requests
#face emotions view
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import json


def face_emotion_view(request):
    """View for the face emotion detection page."""
    return render(request, 'face.html')


def get_content_by_emotion(request):
    """API endpoint to get appropriate content based on emotion and topic."""
    emotion = request.GET.get('emotion', 'neutral')
    topic = request.GET.get('topic', 'dsa')
    
    try:
        # Call Ollama API for content recommendation
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama3",
                "prompt": f"""
                Given a student learning about {topic} who is currently feeling {emotion},
                recommend the most appropriate type of content (blog, video, or game)
                and provide a specific URL for that content that is publicly available online.
                The content should help them learn {topic} effectively given their emotional state.
                Format your response as JSON with the following structure:
                {{
                    "content_type": "blog|video|game",
                    "url": "https://example.com/content",
                    "reason": "Brief explanation of why this content is appropriate"
                }}
                """
            },
            timeout=10
        )
        
        # Parse Ollama response
        ollama_data = response.json()
        content_data = json.loads(ollama_data.get('response', '{}'))
        
        return JsonResponse(content_data)
        
    except Exception as e:
        # Fallback content map if Ollama fails
        content_map = {
            "dsa": {
                "neutral": {"content_type": "blog", "url": "https://www.geeksforgeeks.org/data-structures/"},
                "happy": {"content_type": "blog", "url": "https://www.geeksforgeeks.org/data-structures/"},
                "sad": {"content_type": "video", "url": "https://www.youtube.com/embed/8hly31xKli0"},
                "bored": {"content_type": "game", "url": "https://www.codingame.com/playgrounds/explore"}
            },
            "python": {
                "neutral": {"content_type": "blog", "url": "https://realpython.com/python-beginners-guide/"},
                "happy": {"content_type": "blog", "url": "https://realpython.com/python-beginners-guide/"},
                "sad": {"content_type": "video", "url": "https://www.youtube.com/embed/rfscVS0vtbw"},
                "bored": {"content_type": "game", "url": "https://www.codingame.com/playgrounds/52377/python-course-for-beginners"}
            },
            # Add other topics as needed
        }
        
        # Get content from fallback map
        topic_map = content_map.get(topic, content_map["dsa"])
        content = topic_map.get(emotion, topic_map["neutral"])
        content["reason"] = "Fallback content selection (Ollama unavailable)"
        
        return JsonResponse(content)
# dashboard/views.py
from nrclex import NRCLex
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json

# 🎨 Emoji map for emotion labels
EMOJI_MAP = {
    "joy": "😄",
    "sadness": "😢",
    "anger": "😡",
    "fear": "😨",
    "disgust": "🤢",
    "surprise": "😲",
    "neutral": "😐",
    "love": "❤️"
}

@csrf_exempt
def detect_emotion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        if not text:
            return JsonResponse({'error': 'No text provided.'})

        # 🎯 Emotion detection using NRCLex
        emotion_label = get_emotion_from_nrclex(text)
        emoji = EMOJI_MAP.get(emotion_label, "😐")

        # 🤖 Ollama response
        ollama_reply = query_ollama(text)

        return JsonResponse({
            'response': ollama_reply,
            'emotion': f"Detected Emotion: {emotion_label.capitalize()} {emoji}"
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_emotion_from_nrclex(text):
    try:
        emotion_obj = NRCLex(text)
        emotions = emotion_obj.raw_emotion_scores

        if not emotions:
            return "neutral"

        # Return the emotion with the highest score
        top_emotion = max(emotions, key=emotions.get)
        return top_emotion if top_emotion in EMOJI_MAP else "neutral"
    except Exception as e:
        print(f"NRC error: {e}")
        return "neutral"

def query_ollama(text):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"The user said: '{text}'. Respond empathetically.",
                "stream": False
            }
        )
        return response.json().get("response", "Sorry, I couldn't think of a reply.")
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

def text_chat(request):
    return render(request, 'text.html')
