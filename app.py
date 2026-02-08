import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import base64
import os
import json
import requests
import time
import random

# Try importing canvas, handle if missing
try:
    from streamlit_drawable_canvas import st_canvas
except ImportError:
    st_canvas = None

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Our Love Story", layout="centered", page_icon="💖")

# ---------------- HELPER FUNCTIONS ----------------
@st.cache_data
def get_audio_html(file_path, _mtime=None):
    try:
        ext = os.path.splitext(file_path)[1].lower().replace(".", "")
        mime_type = f"audio/{ext}"
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"""
        <audio id="love-audio" loop>
            <source src="data:{mime_type};base64,{b64}" type="{mime_type}">
        </audio>
        <script>
            var audio = document.getElementById("love-audio");
            audio.volume = 0.3; 
            function playAudio() {{
                audio.play().catch(function(e){{ console.log(e); }});
            }}
            playAudio();
            window.parent.document.addEventListener('click', playAudio, {{ once: true }});
        </script>
        """
    except Exception as e:
        return ""

@st.cache_data
def get_file_b64(file_path, _mtime=None):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

def render_voice_note(day_key):
    st.markdown("---")
    st.markdown("### 💌 A Voice Note For You")
    
    # Check for mp3, aac, m4a, wav and pick the NEWEST one
    candidates = [
        (f"{day_key}_note.mp3", "audio/mp3"),
        (f"{day_key}_note.aac", "audio/mp4"), # Try mp4 mime for aac
        (f"{day_key}_note.m4a", "audio/mp4"),
        (f"{day_key}_note.wav", "audio/wav")
    ]
    
    # Filter for existing files and sort by modification time (newest first)
    existing_files = []
    for fname, mime in candidates:
        if os.path.exists(fname):
            existing_files.append((fname, mime, os.path.getmtime(fname)))
            
    existing_files.sort(key=lambda x: x[2], reverse=True)
    
    if existing_files:
        best_file, fmt, _ = existing_files[0]
        
        # TRANSCODING LOGIC: Convert everything to MP3 for maximum compatibility
        # This solves the "browser doesn't support this specific AAC codec" issue
        final_mp3_path = best_file + ".converted.mp3"
        
        # Only convert if mp3 doesn't exist or is older than source
        should_convert = True
        if os.path.exists(final_mp3_path):
            if os.path.getmtime(final_mp3_path) > os.path.getmtime(best_file):
                should_convert = False
        
        if should_convert:
            try:
                # TRANSCODING: Use direct ffmpeg call (bypasses pydub/ffprobe issues)
                import imageio_ffmpeg
                import subprocess
                
                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                
                # Command: ffmpeg -y -i input -vn -ar 44100 -ac 2 -b:a 192k output.mp3
                # -y: overwrite
                # -vn: disable video
                # -ar: audio rate
                # -ac: audio channels
                cmd = [
                    ffmpeg_exe, "-y", 
                    "-i", best_file,
                    "-vn",
                    "-ar", "44100",
                    "-ac", "2",
                    "-b:a", "192k",
                    final_mp3_path
                ]
                
                # Run conversion (suppress output unless error)
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                best_file = final_mp3_path
                fmt = "audio/mp3"
                st.toast("✅ Voice note converted successfully!")
            except Exception as e:
                # Fallback
                print(f"Conversion failed: {e}")
                st.error(f"Could not convert audio: {e}")
                pass
        else:
             best_file = final_mp3_path
             fmt = "audio/mp3"

        # Debug info removed as per user request
        # size_mb = os.path.getsize(best_file) / (1024 * 1024)
        # st.caption(f"Playing: {os.path.basename(best_file)} ({size_mb:.2f} MB)") 

        # Read as bytes and use Base64 to force browser to play it natively
        # Read as bytes and use Base64 to force browser to play it natively
        # Use cached function with mtime for invalidation
        b64 = get_file_b64(best_file, os.path.getmtime(best_file))
            
        # Custom HTML Audio Player
        audio_html = f"""
            <audio controls style="width: 100%; border-radius: 10px;">
                <source src="data:{fmt};base64,{b64}" type="{fmt}">
                Your browser does not support the audio element.
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='glass-card' style='padding:15px; text-align:center; font-style:italic;'>
            (Voice note for {day_key} not found. <br>Imagine me saying: "I love you more than words can say!" 💖)
        </div>
        """, unsafe_allow_html=True)

@st.cache_data
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

@st.cache_data
def get_image_b64(file_path, _mtime=None):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# ---------------- PREMIUM THEME MANAGER ----------------
def inject_css(theme):
    # Base CSS Keyframes
    animations = """
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 40px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4); }
        70% { box-shadow: 0 0 0 20px rgba(255, 255, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    """
    
    # Base Styles (Glassmorphism & Typography)
    base_style = """
    body { font-family: 'Lato', sans-serif; }
    
    /* GLASS CARD SYSTEM */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border-radius: 20px;
        padding: 40px;
        margin: 20px 0;
        animation: fadeInUp 1s ease-out;
        color: white;
    }
    
    /* BUTTON STYLING */
    .stButton button {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 15px 40px !important;
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.4s ease !important;
        backdrop-filter: blur(5px);
    }
    .stButton button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        background: rgba(255, 255, 255, 0.25) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
        border-color: white !important;
    }
    
    /* HEADERS */
    h1 {
        font-family: 'Great Vibes', cursive;
        font-weight: 400;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 20px;
        animation: float 6s ease-in-out infinite;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    h2, h3 {
        font-family: 'Cinzel', serif;
        text-align: center;
        font-weight: 300;
        letter-spacing: 4px;
    }
    """

    # Theme Specific Overrides
    theme_css = ""
    if theme == "rose":
        theme_css = """
        .stApp { background: linear-gradient(135deg, #a80038 0%, #fb93ac 100%); }
        h1 { color: #fff0f5; text-shadow: 0 0 20px #ff1493; }
        .glass-card { background: rgba(50, 0, 10, 0.3); border: 1px solid rgba(255, 192, 203, 0.3); }
        """
    elif theme == "propose":
        theme_css = """
        .stApp { background: radial-gradient(circle at 60% 50%, #2b0c16 0%, #100000 100%); }
        h1 { color: #ffd700; text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
        .glass-card { background: rgba(20, 0, 0, 0.5); border: 1px solid rgba(255, 215, 0, 0.2); }
        .stButton button { border-color: #ffd700 !important; color: #ffd700 !important; }
        """
    elif theme == "chocolate":
        theme_css = """
        .stApp { background: linear-gradient(135deg, #3e2723 0%, #5d4037 100%); }
        h1 { color: #ffe0b2; }
        .glass-card { background: rgba(62, 39, 35, 0.6); border: 1px solid rgba(255, 215, 0, 0.3); }
        """
    elif theme == "teddy":
        theme_css = """
        .stApp { background: linear-gradient(135deg, #d7ccc8 0%, #efebe9 100%); }
        h1 { color: #5d4037; text-shadow: none; font-family:'Cinzel'; font-weight:700;}
        .glass-card { 
            background: #fffbf0; 
            color: #5d4037; 
            box-shadow: 5px 5px 15px rgba(0,0,0,0.1); 
            border: none;
            background-image: linear-gradient(#efebe9 1px, transparent 1px);
            background-size: 100% 30px;
        }
        .stButton button { background: #8d6e63 !important; color: white !important; }
        """
    elif theme == "promise":
        theme_css = """
        .stApp { background: linear-gradient(135deg, #0d47a1 0%, #42a5f5 100%); }
        h1 { color: #e3f2fd; }
        .glass-card { background: rgba(13, 71, 161, 0.8); border: 1px solid rgba(187, 222, 251, 0.3); }
        """
    elif theme == "hug":
        theme_css = """
        .stApp { background: linear-gradient(135deg, #ff6f00 0%, #ffca28 100%); }
        h1 { color: #fff3e0; }
        .glass-card { background: rgba(255, 111, 0, 0.3); }
        """
    elif theme == "kiss":
        theme_css = """
        .stApp { background: linear-gradient(135deg, #4a148c 0%, #8e24aa 100%); }
        h1 { color: #f3e5f5; }
        .glass-card { background: rgba(74, 20, 140, 0.4); border: 1px solid rgba(225, 190, 231, 0.3); }
        """
    elif theme == "valentine":
        theme_css = """
        .stApp { background: radial-gradient(circle at 50% 50%, #b71c1c 0%, #5c0000 100%); }
        h1 { font-size: 80px; color: #ffcdd2; text-shadow: 0 0 30px #d50000; animation: pulse-glow 3s infinite; }
        .glass-card { background: rgba(80, 0, 0, 0.6); border: 1px solid rgba(255, 215, 0, 0.4); }
        
        /* TIMELINE STYLES */
        .timeline-item {
            position: relative;
            padding-left: 50px;
            margin-bottom: 40px;
        }
        .timeline-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 2px;
            height: 100%;
            background: rgba(255,255,255,0.3);
        }
        .timeline-dot {
            position: absolute;
            left: -9px;
            top: 0;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #ffd700;
            box-shadow: 0 0 10px #ffd700;
            animation: pulse-glow 2s infinite;
        }
        .timeline-year {
            font-family: 'Cinzel', serif;
            font-size: 24px;
            color: #ffd700;
            margin-bottom: 5px;
        }
        .timeline-content {
            font-family: 'Lato', sans-serif;
            font-size: 18px;
            color: rgba(255,255,255,0.9);
        }
        """
    else:
        theme_css = ".stApp { background: #121212; }"

    full_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;700&family=Dancing+Script:wght@400;700&family=Lato:wght@300;400;700&display=swap');
    {animations}
    {base_style}
    {theme_css}
    </style>
    """
    st.markdown(full_css, unsafe_allow_html=True)

    # MAGIC CURSOR (Global)
    components.html("""
    <script>
    document.addEventListener('mousemove', function(e) {
        if (Math.random() > 0.8) {
            let heart = document.createElement('div');
            heart.innerHTML = '💖';
            heart.style.position = 'fixed';
            heart.style.left = e.clientX + 'px';
            heart.style.top = e.clientY + 'px';
            heart.style.fontSize = Math.random() * 20 + 10 + 'px';
            heart.style.pointerEvents = 'none';
            heart.style.opacity = '0.8';
            document.body.appendChild(heart);
            let y = e.clientY;
            let opacity = 0.8;
            let anim = setInterval(function() {
                y -= 2;
                opacity -= 0.02;
                heart.style.top = y + 'px';
                heart.style.opacity = opacity;
                if (opacity <= 0) {
                    clearInterval(anim);
                    heart.remove();
                }
            }, 50);
        }
    });
    </script>
    """, height=0)

# ---------------- PAGES ----------------

def page_locked(day_name, unlock_date):
    inject_css("locked")
    st.markdown(f"<div style='height:20vh'></div>", unsafe_allow_html=True)
    st.markdown(f"<h1>🔒 {day_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3>Unlocks on {unlock_date}</h3>", unsafe_allow_html=True)

def page_rose():
    inject_css("rose")
    st.markdown("<h1>Grow Your Love 🌹</h1>", unsafe_allow_html=True)
    
    # State for Rose Game
    if "rose_stage" not in st.session_state:
        st.session_state.rose_stage = 0 # 0=Seed, 1=Sprout, 2=Bud, 3=Bloom

    stages = [
        {"icon": "🌱", "msg": "A tiny seed of love...", "btn": "Water Me 💧"},
        {"icon": "🌿", "msg": "It's growing stronger!", "btn": "Give Sunlight ☀️"},
        {"icon": "🌷", "msg": "Almost there...", "btn": "Give Love 💖"},
        {"icon": "🌹", "msg": "A Beautiful Rose for You!", "btn": "Reset"}
    ]
    
    current = stages[st.session_state.rose_stage]
    
    st.markdown(f"""
    <div class='glass-card' style='text-align:center'>
        <div style='font-size:120px; animation:float 3s infinite;'>{current['icon']}</div>
        <p style='font-size:24px; margin-top:20px;'>{current['msg']}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.rose_stage < 3:
        if st.button(current['btn']):
            st.session_state.rose_stage += 1
            st.rerun()
    else:
        st.balloons()
        if st.button("Replay 🔄"):
            st.session_state.rose_stage = 0
            st.rerun()

    render_voice_note("rose")

    # Falling Petals
    components.html("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script>
    function createPetal() {
        const p = document.createElement('div');
        p.innerText = '🌹';
        p.style.position = 'fixed'; p.style.left = Math.random()*100+'vw'; p.style.top = '-50px';
        p.style.fontSize = Math.random()*20+15+'px'; p.style.opacity = Math.random();
        document.body.appendChild(p);
        gsap.to(p, {y: window.innerHeight+100, rotation: 360, duration: Math.random()*5+5, ease:'none', onComplete:()=>p.remove()});
    }
    setInterval(createPetal, 400);
    </script>
    """, height=0)

def page_propose():
    inject_css("propose")
    st.markdown("<h1>Propose Day</h1>", unsafe_allow_html=True)
    
    if "no_clicks" not in st.session_state:
        st.session_state.no_clicks = 0
    if "rose_accepted" not in st.session_state:
        st.session_state.rose_accepted = False

    st.markdown("""
    <div class='glass-card'>
        <h3>My Forever Question</h3>
        <p style='text-align:center; font-size:18px; margin-top:20px; opacity:0.9;'>
        They say you only fall in love once, but that can't be true...<br>
        Because every time I look at you, I fall in love all over again.
        </p>
        <p style='text-align:center; font-size:24px; margin-top:30px; font-weight:bold; color:#ffd700;'>
        Will You Be Mine?
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.rose_accepted:
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
             pass # padding
        with col2:
            if st.button("YES, I WILL! 💍"):
                st.session_state.rose_accepted = True
                st.balloons()
                st.rerun()
        
        with col3:
            # THE IMPOSSIBLE NO
            no_texts = ["No", "Are you sure?", "Really?", "Think again!", "Last chance!", "Please?", "Okay, YES!"]
            current_no_text = no_texts[min(st.session_state.no_clicks, len(no_texts)-1)]
            
            if st.button(current_no_text):
                if current_no_text == "Okay, YES!":
                    st.session_state.rose_accepted = True
                    st.balloons()
                    st.rerun()
                else:
                    st.session_state.no_clicks += 1
                    st.rerun()

    else:
        st.markdown("<div class='glass-card' style='text-align:center; background:rgba(0,100,0,0.3); border-color:#00ff00;'><h3>SHE SAID YES! 💍💖</h3></div>", unsafe_allow_html=True)
        if os.path.exists("celebration.mp4"):
            st.video("celebration.mp4", autoplay=True)

    render_voice_note("propose")

def page_chocolate():
    inject_css("chocolate")
    st.markdown("<h1>Chocolate Day</h1>", unsafe_allow_html=True)
    
    if "opened_chocolates" not in st.session_state:
        st.session_state.opened_chocolates = set()

    prizes = {
        0: "Sweeter than candy! 🍬", 1: "Melts my heart 💖", 2: "Perfect Mix 🍩",
        3: "Love you a choco-lot! 🍫", 4: "My favorite flavor is YOU 💋", 5: "Sweetest soul! 🍭",
        6: "Hugs & Kisses 🤗", 7: "You are the milk to my dark world 🥛", 8: "Be my KitKat? ❤️"
    }

    st.markdown("<div style='text-align:center; margin-bottom:20px; font-family:Cinzel; letter-spacing:2px;'>TAP TO UNWRAP</div>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            st.write("")
            if i in st.session_state.opened_chocolates:
                 st.markdown(f"<div style='background:rgba(0,0,0,0.3); padding:20px; border-radius:10px; text-align:center; border:1px solid #d7ccc8;'>{prizes[i]}</div>", unsafe_allow_html=True)
            else:
                if st.button("🍫", key=f"choco_{i}"):
                    st.session_state.opened_chocolates.add(i)
                    st.rerun()
    
    render_voice_note("chocolate")

def page_teddy():
    inject_css("teddy")
    st.markdown("<h1>Teddy Day</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Build Your Custom Bear 🧸</h3>", unsafe_allow_html=True)

    # Initialize Session State
    if "bear_created" not in st.session_state:
        st.session_state.bear_created = False
        st.session_state.bear_color = "🧸" 
        st.session_state.bear_accessory = ""

    # Teddy Bear Image Mapping
    bear_map = {
        ("🧸", "🎀"): "teddy_brown_bow.png",
        ("🧸", "🕶️"): "teddy_brown_shades.png",
        ("🧸", "💌"): "teddy_brown_letter.png",
        ("🐻‍❄️", "🎀"): "teddy_white_bow.png",
        ("🐻‍❄️", "🕶️"): "teddy_white_shades.png",
        ("🐻‍❄️", "💌"): "teddy_white_letter.png",
        ("🐼", "🎀"): "teddy_panda_bow.png",
        ("🐼", "🕶️"): "teddy_panda_shades.png",
        ("🐼", "💌"): "teddy_panda_letter.png",
    }

    if not st.session_state.bear_created:
        col1, col2 = st.columns(2)
        with col1:
             st.markdown("<div class='glass-card'><h4>1. Choose Bear</h4></div>", unsafe_allow_html=True)
             if st.button("Classic Brown 🧸"): st.session_state.bear_color = "🧸"
             if st.button("Polar White 🐻‍❄️"): st.session_state.bear_color = "🐻‍❄️"
             if st.button("Panda 🐼"): st.session_state.bear_color = "🐼"
        
        with col2:
             st.markdown("<div class='glass-card'><h4>2. Add Accessory</h4></div>", unsafe_allow_html=True)
             if st.button("Red Bow 🎀"): st.session_state.bear_accessory = "🎀"
             if st.button("Cool Shades 🕶️"): st.session_state.bear_accessory = "🕶️"
             if st.button("Love Letter 💌"): st.session_state.bear_accessory = "💌"
        
        st.markdown("---")
        # Show preview of selection if creating
        st.markdown(f"<div style='text-align:center; font-size:40px; margin-bottom:20px;'>{st.session_state.bear_color} + {st.session_state.bear_accessory}</div>", unsafe_allow_html=True)

        if st.button("CREATE MY BEAR ✨"):
             st.session_state.bear_created = True
             st.rerun()
    else:
        st.balloons()
        
        # Determine image file
        selected_img = bear_map.get((st.session_state.bear_color, st.session_state.bear_accessory))
        
        st.markdown(f"""
        <div class='glass-card' style='text-align:center'>
            <h2>Your Special Delivery!</h2>
        </div>
        """, unsafe_allow_html=True)

        if selected_img and os.path.exists(selected_img):
            st.image(selected_img, caption="Made with love, just for you.", use_container_width=True)
        else:
            # Fallback if image missing
            st.markdown(f"""
            <div style='text-align:center; font-size:100px;'>{st.session_state.bear_color} + {st.session_state.bear_accessory}</div>
            <p style='text-align:center'>(Image not found: {selected_img})</p>
            """, unsafe_allow_html=True)

        if st.button("Make Another Bear"):
            st.session_state.bear_created = False
            st.rerun()

    render_voice_note("teddy")

def page_promise():
    inject_css("promise")
    st.markdown("<h1>Promise Day</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom:20px;'>The Digital Contract</h3>", unsafe_allow_html=True)
    
    if "contract_signed" not in st.session_state:
        st.markdown("""
        <div class='glass-card' style='color:#e3f2fd'>
            <h2 style='border-bottom:1px solid rgba(255,255,255,0.3); padding-bottom:10px;'>Official Relationship Contract</h2>
            <ul>
                <li>I promise to always listen to you.</li>
                <li>I promise to never go to bed angry.</li>
                <li>I promise to share my food (mostly).</li>
                <li>I promise to love you more every single day.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='text-align:center;'>Sign Below to Seal the Deal:</div>", unsafe_allow_html=True)
        
        if st_canvas:
            canvas_result = st_canvas(
                stroke_width=2,
                stroke_color="#fff",
                background_color="#1976D2",
                height=150,
                width=300,
                drawing_mode="freedraw",
                key="canvas",
            )
            
            if st.button("Seal the Deal ✍️"):
                 st.session_state.contract_signed = True
                 st.rerun()
        else:
             if st.button("I Promise! (Canvas Error)"):
                 st.session_state.contract_signed = True
                 st.rerun()
    else:
        st.balloons()
        st.markdown("""
        <div class='glass-card' style='text-align:center; border:2px solid #FFD700;'>
            <div style='font-size:80px;'>✅</div>
            <h2>CONTRACT OFFICIAL</h2>
            <p>Signed & Sealed with Love.</p>
        </div>
        """, unsafe_allow_html=True)

    render_voice_note("promise")

def page_hug():
    inject_css("hug")
    st.markdown("<h1>Hug Day</h1>", unsafe_allow_html=True)
    
    if "hug_score" not in st.session_state:
        st.session_state.hug_score = 0
    
    st.markdown(f"""
    <div class='glass-card' style='text-align:center'>
        <h3>Hug-O-Meter 🤗</h3>
        <div style='width:100%; background:rgba(0,0,0,0.2); height:30px; border-radius:15px; overflow:hidden; margin-bottom:20px;'>
            <div style='width:{min(st.session_state.hug_score, 100)}%; background:#fff; height:100%; transition:width 0.2s;'></div>
        </div>
        <p>Hug Energy: {st.session_state.hug_score}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.hug_score < 100:
        if st.button("SEND HUG 🤗 (Click Fast!)"):
            st.session_state.hug_score += 10
            if st.session_state.hug_score >= 100:
                st.balloons()
            st.rerun()
    else:
         st.markdown("<div style='text-align:center; font-size:40px; animation:pulse-glow 1s infinite;'>🥰 MAXIMUM COMFORT ACHIEVED!</div>", unsafe_allow_html=True)
         if st.button("Reset Hugs"):
             st.session_state.hug_score = 0
             st.rerun()
             
    render_voice_note("hug")

def page_kiss():
    inject_css("kiss")
    st.markdown("<h1>Kiss Day</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Click anywhere to send a kiss! 💋</h3>", unsafe_allow_html=True)
    
    # Click-to-Kiss JS
    components.html("""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; height: 100vh; background: transparent; }
    </style>
    <div id="click-area" style="width:100vw; height:100vh; cursor:pointer;"></div>
    <script>
    document.addEventListener('click', (e) => {
        const kiss = document.createElement('div');
        kiss.innerText = '💋';
        kiss.style.position = 'fixed';
        kiss.style.left = e.clientX + 'px';
        kiss.style.top = e.clientY + 'px';
        kiss.style.fontSize = '40px';
        kiss.style.pointerEvents = 'none';
        kiss.style.transform = 'translate(-50%, -50%)';
        document.body.appendChild(kiss);
        
        gsap.to(kiss, {
            scale: 2,
            opacity: 0,
            duration: 1,
            onComplete: () => kiss.remove()
        });
    });
    </script>
    """, height=600)
    
    render_voice_note("kiss")

def page_valentine():
    inject_css("valentine")
    st.markdown("<h1>Happy Valentine's Day</h1>", unsafe_allow_html=True)
    
    # THE TIMELINE - Vertical CSS
    st.markdown("""
<div style='max-width: 600px; margin: 0 auto;'>
<div class='glass-card'>
<h2 style='margin-bottom:40px; border-bottom:1px solid rgba(255,255,255,0.3); padding-bottom:10px;'>Our Love Journey</h2>
<div class='timeline-item'>
<div class='timeline-dot'></div>
<div class='timeline-year'>2024</div>
<div class='timeline-content'>The Day We Met 💖<br>And my life changed forever.</div>
</div>
<div class='timeline-item'>
<div class='timeline-dot'></div>
<div class='timeline-year'>2024</div>
<div class='timeline-content'>Falling in Love 🌹<br>Every moment became a memory.</div>
</div>
<div class='timeline-item' style='margin-bottom:0;'>
<div class='timeline-dot' style='background:#ff1493; box-shadow:0 0 20px #ff1493;'></div>
<div class='timeline-year' style='color:#ff1493;'>2026</div>
<div class='timeline-content'>Forever & Always ♾️<br>Just you and me.</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    st.balloons()
    
    if os.path.exists("photo1.jpg"):
        st.markdown("<div class='glass-card' style='padding:10px;'><img src='data:image/jpeg;base64,"+get_image_b64("photo1.jpg", os.path.getmtime("photo1.jpg"))+"' style='width:100%; border-radius:10px;'></div>", unsafe_allow_html=True)
        
    render_voice_note("valentine")

# ---------------- MAIN APP LOGIC ----------------
def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # LOCK SCREEN
    if not st.session_state.authenticated:
        st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle, #2b0c16 0%, #000000 100%); color: #ffd700; }
        .stTextInput input { text-align: center; border: 1px solid #ffd700; color: #ffd700; background: transparent; }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:30vh'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-family:Cinzel; text-align:center; color:#E0BFB8;'>Our Love Story</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            pwd = st.text_input("Enter Key", type="password", label_visibility="collapsed", placeholder="Birthday (DDMMYYYY)")
            if st.button("Enter ❤️"):
                if pwd == "15122004":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect Key")
        return

    # MUSIC PLAYER
    # Dynamic music based on the selected page (if accessible)
    # Since Streamlit re-runs the whole script, we can check the selected page from sidebar
    # However, 'selection' is defined later. We can move the sidebar definition up or handle logic after.
    # Let's handle it after 'selection' is made.

    # SIDEBAR
    st.sidebar.markdown("<h2 style='text-align:center; font-family:Great Vibes; color:#ff1493;'>Timeline</h2>", unsafe_allow_html=True)
    
    # Developer Controls Hidden
    # dev_mode = st.sidebar.checkbox("Dev Mode (Time Travel)", value=False)
    dev_mode = False
    
    today = datetime.now().day
    month = datetime.now().month
    current_day = today if month == 2 else 0 # Standard Time Logic
    # if dev_mode: current_day = 30
        
    days = {
        "🌹 Rose Day": {"date": 7, "func": page_rose, "key": "rose"},
        "💍 Propose Day": {"date": 8, "func": page_propose, "key": "propose"},
        "🍫 Chocolate Day": {"date": 9, "func": page_chocolate, "key": "chocolate"},
        "🧸 Teddy Day": {"date": 10, "func": page_teddy, "key": "teddy"},
        "🤝 Promise Day": {"date": 11, "func": page_promise, "key": "promise"},
        "🤗 Hug Day": {"date": 12, "func": page_hug, "key": "hug"},
        "💋 Kiss Day": {"date": 13, "func": page_kiss, "key": "kiss"},
        "💖 Valentine's Day": {"date": 14, "func": page_valentine, "key": "valentine"},
    }

    days_list = list(days.keys())
    default_index = 0
    
    # Calculate default index based on current date
    # Rose Day is index 0 (Feb 7). Valentine is index 7 (Feb 14).
    if month == 2:
        if 7 <= current_day <= 14:
            default_index = current_day - 7
        elif current_day > 14:
            default_index = 7 # Stay on Valentine's if past date
    
    selection = st.sidebar.radio("Go to:", days_list, index=default_index)
    day_info = days[selection]
    key = day_info["key"]
    
    # PLAY BACKGROUND MUSIC
    # Only try to find the DAY'S specific song if the day is UNLOCKED
    music_file = None
    if current_day >= day_info["date"]:
        for ext in ["mp3", "ogg", "wav"]:
            candidate = f"{key}_song.{ext}"
            if os.path.exists(candidate):
                music_file = candidate
                break
                
    # Fallback to default love.mp3 if no specific song found OR if day is locked
    if not music_file:
        music_file = "love.mp3"
    
    if os.path.exists(music_file):
        components.html(get_audio_html(music_file, os.path.getmtime(music_file)), height=0)

    # RENDER PAGE
    if dev_mode:
        current_day = 30
        st.sidebar.markdown("---")
        st.sidebar.subheader("🎙️ Upload Your Voice")
        st.sidebar.info("Upload .mp3/.aac/.m4a to replace the current day's voice note.")
        
        uploaded_voice = st.sidebar.file_uploader(f"Voice for {selection}", type=["mp3", "wav", "aac", "m4a"], key=f"uploader_{key}")
        
        if uploaded_voice:
            # Determine extension
            ext = uploaded_voice.name.split(".")[-1].lower()
            if ext not in ["mp3", "wav", "aac", "m4a"]: ext = "mp3" 
            
            # Save the file
            target_filename = f"{key}_note.{ext}"
            with open(target_filename, "wb") as f:
                f.write(uploaded_voice.getbuffer())
            st.sidebar.success(f"Saved to {target_filename}!")
            
            # Remove conflicting files (optional, but good)
            for other_ext in ["mp3", "wav", "aac", "m4a"]:
                if other_ext != ext:
                    other_name = f"{key}_note.{other_ext}"
                    if os.path.exists(other_name):
                        try: os.remove(other_name)
                        except: pass

    if current_day >= day_info["date"]:
        day_info["func"]()
    else:
        page_locked(selection, f"Feb {day_info['date']}")

if __name__ == "__main__":
    main()
