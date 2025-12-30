import streamlit as st
from fer_pytorch import FER
import cv2
import numpy as np
from streamlit_lottie import st_lottie
import requests
from gtts import gTTS
import tempfile

# -------------------------------- UI SETUP --------------------------------
st.set_page_config(page_title="AI Healing Companion", layout="wide")

def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

robot = load_lottie("https://assets10.lottiefiles.com/packages/lf20_tll0j4bb.json")


# ------------------------------ MODERN CSS --------------------------------
st.markdown("""
<style>

body {
  background: linear-gradient(145deg, #020617 20%, #0f172a 50%, #020617 80%);
}

.main {
  padding-top:0;
}

/* Cinematic Ambient Spotlight */
body::before {
  content:'';
  position:fixed;
  top:-20%;
  left:-20%;
  width:140%;
  height:140%;
  background: radial-gradient(circle at center,
    rgba(255,255,255,0.08),
    rgba(0,0,0,0.8)
  );
  z-index:-1;
  filter:blur(40px);
}

/* Floating Robot */
.robot-box {
  position: fixed;
  right: 60px;
  top: 60px;
  animation: float 4s ease-in-out infinite, drift 8s infinite alternate;
}

@keyframes float {
  0% { transform: translatey(0px); }
  50% { transform: translatey(-18px); }
  100% { transform: translatey(0px); }
}

@keyframes drift {
  0% { right:40px; }
  100% { right:130px; }
}

/* Elegant Glass Card */
.card {
  background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.04));
  border-radius: 22px;
  padding: 28px;
  border: 1px solid rgba(255,255,255,0.28);
  box-shadow: 0 0 25px rgba(255,255,255,0.12);
  backdrop-filter: blur(15px);
}

/* Elegant Header Typography */
.heading {
  font-size: 52px;
  text-align:center;
  font-weight:900;
  letter-spacing:1px;
  background: linear-gradient(120deg,#8b5cf6,#38bdf8,#a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.tagline {
  text-align:center;
  color:#cbd5f5;
  margin-top:-10px;
  font-size:17px;
  letter-spacing:1px;
}

/* Emotion Title */
.emotion-title {
  color:#d9b4ff;
  font-size:32px;
}

/* Spotify Button */
.heal-btn {
  background:#14b8a6;
  padding:10px 18px;
  border-radius:10px;
  font-size:18px;
  text-decoration:none;
  color:white;
  font-weight:700;
  border: 1px solid rgba(255,255,255,0.5);
  transition: 0.3s;
}
.heal-btn:hover{
  background:#2dd4bf;
  box-shadow:0 0 25px #2dd4bf;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------- HEADER -----------------------------------
st.markdown("<h1 class='heading'>AI Emotional Healing Companion</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>A gentle futuristic friend who understands your feelings, comforts you & heals you 🎶</p>", unsafe_allow_html=True)

# ------------------------------- ROBOT ------------------------------------
if robot:
    st.markdown("<div class='robot-box'>", unsafe_allow_html=True)
    st_lottie(robot, height=240, key="robot")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------- LAYOUT -----------------------------------
left, right = st.columns([1.1,2])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📷 Capture Your Emotion")
    image = st.camera_input("")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------- EMOTION LOGIC ----------------------------------
emotion_music = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DWX83CujKHHOn",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DWSf2RDTDayIx"
}

healing_talk = {
    "happy": "You look radiant today! Your happiness lights the room ✨",
    "sad": "It’s okay to feel sad. I’m here… breathe slowly… you’re not alone 💙",
    "angry": "Anger is powerful… but you are stronger. Let's calm together 🤍",
    "fear": "You are safe now. Nothing can harm you while I’m here 🤖💚",
    "neutral": "Peaceful mind. Balanced heart. Perfect state 🕊️",
    "surprise": "Something unexpected… but you handled it beautifully 😄",
}

emotion_color = {
    "happy": "#2dd4bf",
    "sad": "#60a5fa",
    "angry": "#ef4444",
    "fear": "#facc15",
    "neutral": "#a78bfa",
    "surprise": "#f97316"
}

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧠 Emotion Reflection & Healing")

    if image:

        # Convert camera image to CV2 format
        file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        detector = FER()
        result = detector.detect_emotions(img)

        if result:
            emotions = result[0]["emotions"]
            emotion = max(emotions, key=emotions.get)

            st.markdown(
                f"""
                <style>
                .card {{
                    box-shadow: 0 0 40px {emotion_color.get(emotion,'#ffffff')};
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"<h2 class='emotion-title'>❤️ Emotion Detected: {emotion.upper()}</h2>",
                unsafe_allow_html=True
            )

            message = healing_talk.get(emotion, "I am here for you always 🤍")
            st.success(f"🤖 Companion says:  {message}")

            # ---------- SAFE VOICE ----------
            try:
                tts = gTTS(message, lang="en", tld="com")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as voice_file:
                    tts.save(voice_file.name)
                    st.audio(voice_file.name)
            except Exception:
                st.warning("⚠️ Voice could not be generated. Please check internet or try again.")

            # ---------- Spotify ----------
            if emotion in emotion_music:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    f"<a class='heal-btn' href='{emotion_music[emotion]}' target='_blank'>🎵 Open Healing Spotify Playlist</a>",
                    unsafe_allow_html=True
                )

        else:
            st.error("No face detected. Try again 🙂")

    else:
        st.info("Waiting for your photo… ✨")

    st.markdown("</div>", unsafe_allow_html=True)
  st.markdown("</div>", unsafe_allow_html=True)
