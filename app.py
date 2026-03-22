import streamlit as st
import random
import json
import urllib.parse
import os

# הגדרות עמוד
st.set_page_config(page_title="גלגל הברזים: ליאור ואלה", page_icon="🚫", layout="centered")

# עיצוב RTL ומרכוז תמונה
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    .stImage > img { border-radius: 20px; box-shadow: 0px 10px 30px rgba(0,0,0,0.2); display: block; margin-left: auto; margin-right: auto; max-width: 100%; }
    
    /* עיצוב כפתור הסובב */
    .stButton>button { 
        width: 100%; 
        font-weight: bold; 
        height: 3.5em; 
        background-color: #FF4B4B; 
        color: white; 
        border-radius: 12px; 
        border: none; 
        font-size: 20px;
        margin-top: 20px;
    }
    .stButton>button:hover { background-color: #D43F3F; border: none; }
    
    /* עיצוב רדיו בוטנס (רמת עקיצה) */
    div[data-testid="stMarkdownContainer"] > p { font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# הצגת התמונה
image_name = "ELLA2.jpg" 
if os.path.exists(image_name):
    st.image(image_name, use_container_width=True)

# פונקציה לטעינת נתונים
def load_data():
    try:
        with open("data/excuses.json", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

excuses_data = load_data()

if not excuses_data:
    st.error("⚠️ לא נמצאו תירוצים בתיקיית data/excuses.json")
    st.stop()

st.title("🚫 גלגל הברזים")
st.subheader("כי לכל הברזה יש סיבה (או סתם תירוץ)")

# הממשק החדש
activities = ["להיפגש באמצע בראשון", "נסיעה לאליכין", "לרדת למשען", "קפה שנדחה", "סיור נכסים"]
activity = st.selectbox("ממה מבריזים היום?", activities)

col1, col2 = st.columns(2)
with col1:
    user = st.radio("מי הברזן?", ["אלה", "ליאור"], horizontal=True)

# תצוגה חדשה לרמת עקיצה - כפתורי רדיו מעוצבים
st.write("---")
level_map = {
    "😇 רגיל": "רגיל",
    "😏 עוקצני": "עוקצני",
    "💀 אכזרי": "אכזרי"
}
selected_level_label = st.radio("בחר רמת עקיצה:", list(level_map.keys()), horizontal=True)
level = level_map[selected_level_label]

if st.button("סובב את הגלגל 🎡"):
    excuse = random.choice(excuses_data[user][level])
    
    # שתילת הפעילות בתוך התירוץ אם יש מקום
    if "{activity}" in excuse:
        excuse = excuse.format(activity=activity)
        
    res = f"🎲 {user} מבריז/ה מ{activity}!\nהתירוץ: {excuse}"
    
    # הצגת התוצאה בצורה מודגשת לפי רמה
    if level == "אכזרי":
        st.error(res)
    elif level == "עוקצני":
        st.warning(res)
    else:
        st.success(res)

    # כפתור וואטסאפ
    whatsapp_msg = f"🚫 *חדשות הברזה דחופות!* \n\n{res}"
    encoded_msg = urllib.parse.quote(whatsapp_msg)
    st.markdown(f'''
        <a href="https://wa.me/?text={encoded_msg}" target="_blank">
            <button style="background-color:#25D366; color:white; padding:12px; border:none; border-radius:10px; cursor:pointer; width:100%; font-weight:bold; font-size:16px;">
                📲 שלח את העקיצה בוואטסאפ
            </button>
        </a>
    ''', unsafe_allow_html=True)
