import streamlit as st
import random
import json
import urllib.parse
import os

# הגדרות עמוד
st.set_page_config(page_title="גלגל הברזים: ליאור ואלה", page_icon="🚫", layout="centered")

# עיצוב RTL (יישור לימין)
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[data-testid="stSelectbox"] label, div[data-testid="stSlider"] label { text-align: right; width: 100%; }
    .stButton>button { width: 100%; font-weight: bold; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
""", unsafe_allow_html=True)

# פונקציה לטעינת נתונים
def load_data():
    try:
        with open("data/excuses.json", encoding="utf-8") as f:
            excuses = json.load(f)
        with open("data/real_quotes.json", encoding="utf-8") as f:
            quotes = json.load(f)
        return excuses, quotes
    except FileNotFoundError:
        return None, None

excuses_data, real_quotes = load_data()

if excuses_data is None:
    st.error("⚠️ חסרה תיקיית data או הקבצים בתוכה. וודא שהמבנה ב-GitHub תקין!")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = {"אלה": 0, "ליאור": 0}

st.title("🚫 גלגל הברזים: ליאור ואלה")
st.subheader("מנוע התירוצים המשרדי - גרסת הריפו החדש")

# הגלגל
activities = ["להיפגש באמצע בראשון", "נסיעה לאליכין", "לרדת למשען", "קפה שנדחה", "סיור נכסים"]
activity = st.selectbox("ממה מבריזים היום?", activities)
user = st.selectbox("מי הברזן?", ["אלה", "ליאור"])
level = st.select_slider("רמת עקיצה", options=["רגיל", "עוקצני", "אכזרי"])

if st.button("סובב את הגלגל 🎡"):
    excuse = random.choice(excuses_data[user][level])
    res = f"🎲 {user} מבריז/ה מ{activity}!\nהתירוץ: {excuse}"
    st.session_state.history[user] += 1
    
    if level == "אכזרי": st.error(res)
    elif level == "עוקצני": st.warning(res)
    else: st.success(res)

    # כפתור וואטסאפ
    whatsapp_msg = f"🚫 *חדשות הברזה דחופות!* \n\n{res}"
    encoded_msg = urllib.parse.quote(whatsapp_msg)
    st.markdown(f'''
        <a href="https://wa.me/?text={encoded_msg}" target="_blank">
            <button style="background-color:#25D366; color:white; padding:10px; border:none; border-radius:8px; cursor:pointer; width:100%; font-weight:bold;">
                📲 שלח את העקיצה בוואטסאפ
            </button>
        </a>
    ''', unsafe_allow_html=True)

# סטטיסטיקה
st.divider()
c1, c2 = st.columns(2)
c1.metric("הברזות אלה", st.session_state.history["אלה"])
c2.metric("הברזות ליאור", st.session_state.history["ליאור"])
