import streamlit as st
from datetime import datetime, time
from gtts import gTTS
import json
import os
import uuid

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="DoseGuard Smart Care",
    page_icon="💊",
    layout="wide"
)

# =====================================================
# 🎨 PREMIUM CSS
# =====================================================
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: bold;
    color: #1f77b4;
}
.card {
    padding: 18px;
    border-radius: 14px;
    background: #f7fbff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 14px;
}
.big-btn button {
    height: 60px !important;
    font-size: 18px !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 🌐 LANGUAGE PACK
# =====================================================
LANG = {
    "English": {
        "title": "DoseGuard Smart Care",
        "mode": "Select Mode",
        "member": "Member Mode",
        "caregiver": "Caregiver Mode",
        "profiles": "Member Profiles",
        "add_member": "Add New Member",
        "member_name": "Member Name",
        "today": "Today's Medicines",
        "taken": "Taken",
        "remind": "Remind",
        "health": "Health %",
        "streak": "Adherence Streak",
        "risk_low": "Risk Level: LOW",
        "risk_med": "Risk Level: MEDIUM",
        "risk_high": "HIGH RISK",
        "call_log": "Call Activity Log",
        "no_calls": "No calls yet",
        "food": "Food",
        "before": "Before Food",
        "after": "After Food",
        "when": "When"
    },

    "Tamil": {
        "title": "டோஸ் கார்ட்",
        "mode": "முறை தேர்வு",
        "member": "உறுப்பினர்",
        "caregiver": "பராமரிப்பாளர்",
        "profiles": "உறுப்பினர் பட்டியல்",
        "add_member": "புதிய உறுப்பினர்",
        "member_name": "உறுப்பினர் பெயர்",
        "today": "இன்றைய மருந்துகள்",
        "taken": "எடுத்தேன்",
        "remind": "நினைவூட்டு",
        "health": "ஆரோக்கியம் %",
        "streak": "தொடர்",
        "risk_low": "ஆபத்து: குறைவு",
        "risk_med": "ஆபத்து: நடுத்தரம்",
        "risk_high": "உயர் ஆபத்து",
        "call_log": "அழைப்பு பதிவு",
        "no_calls": "அழைப்புகள் இல்லை",
        "food": "உணவு",
        "before": "உணவுக்கு முன்",
        "after": "உணவுக்கு பின்",
        "when": "எப்போது"
    },

    "Hindi": {
        "title": "डोजगार्ड",
        "mode": "मोड चुनें",
        "member": "सदस्य मोड",
        "caregiver": "केयरगिवर मोड",
        "profiles": "सदस्य प्रोफाइल",
        "add_member": "नया सदस्य",
        "member_name": "सदस्य नाम",
        "today": "आज की दवाएं",
        "taken": "ले लिया",
        "remind": "याद दिलाएं",
        "health": "स्वास्थ्य %",
        "streak": "स्ट्रीक",
        "risk_low": "जोखिम: कम",
        "risk_med": "जोखिम: मध्यम",
        "risk_high": "उच्च जोखिम",
        "call_log": "कॉल लॉग",
        "no_calls": "कोई कॉल नहीं",
        "food": "भोजन",
        "before": "भोजन से पहले",
        "after": "भोजन के बाद",
        "when": "कब"
    }
}

# =====================================================
# 🌐 LANGUAGE SELECTOR (WORKING)
# =====================================================
language_choice = st.sidebar.selectbox(
    "🌐 Language / மொழி / भाषा",
    ["English", "Tamil", "Hindi"],
    key="language_selector"
)

T = LANG[language_choice]

# =====================================================
# STORAGE
# =====================================================
DATA_FILE = "members.json"

def load_members():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_members(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_member(member):
    data = load_members()
    member["id"] = str(uuid.uuid4())
    data.append(member)
    save_members(data)

# =====================================================
# SESSION STATE
# =====================================================
if "acknowledged" not in st.session_state:
    st.session_state.acknowledged = {}

if "call_logs" not in st.session_state:
    st.session_state.call_logs = []

# =====================================================
# VOICE
# =====================================================
def play_voice(text):
    try:
        lang_code = {"English": "en", "Tamil": "ta", "Hindi": "hi"}[language_choice]
        tts = gTTS(text, lang=lang_code)
        tts.save("reminder.mp3")
        st.audio("reminder.mp3")
    except:
        pass

# =====================================================
# AI CALL SIMULATION
# =====================================================
def make_call(phone, message):
    st.info(f"📞 Calling {phone}...")
    play_voice(message)

    st.session_state.call_logs.append({
        "time": datetime.now().strftime("%I:%M %p"),
        "phone": phone,
        "status": "Simulated Call"
    })

# =====================================================
# 🧭 MODE SWITCH
# =====================================================
mode = st.sidebar.radio(
    T["mode"],
    [T["member"], T["caregiver"]]
)

members = load_members()
member_names = [m.get("name", "Unknown") for m in members]

# =====================================================
# 👴 MEMBER MODE
# =====================================================
if mode == T["member"]:

    st.markdown(f"<div class='main-title'>💊 {T['title']}</div>", unsafe_allow_html=True)

    if not members:
        st.warning("No members available.")
        st.stop()

    selected_name = st.sidebar.selectbox(T["profiles"], member_names)
    member = next(m for m in members if m["name"] == selected_name)

    st.subheader(f"👋 Hello, {member['name']}")
    st.header(T["today"])

    dose_times = {
        "Morning": time(8, 0),
        "Afternoon": time(14, 0),
        "Night": time(20, 0)
    }

    now = datetime.now().time()
    missed_today = 0

    for med in member.get("medicines", []):
        for period in med.get("periods", []):

            key = f"{member['id']}_{med['name']}_{period}"

            if key not in st.session_state.acknowledged:
                st.session_state.acknowledged[key] = False

            scheduled_time = dose_times.get(period, time(8, 0))

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"### 💊 {med['name']} ({period})")
            st.write(f"⏰ {scheduled_time.strftime('%I:%M %p')}")
            st.write(f"🍽 {med['food']}")

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
                if st.button(f"🔔 {T['remind']}", key=f"r{key}"):
                    play_voice("Time to take your medicine")
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown("<div class='big-btn'>", unsafe_allow_html=True)
                if st.button(f"✅ {T['taken']}", key=f"t{key}"):
                    st.session_state.acknowledged[key] = True
                    st.success("Recorded")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            if now > scheduled_time and not st.session_state.acknowledged[key]:
                missed_today += 1

# =====================================================
# 👩‍⚕️ CAREGIVER MODE
# =====================================================
else:

    st.markdown(f"<div class='main-title'>👩‍⚕️ {T['caregiver']}</div>", unsafe_allow_html=True)

    selected_name = st.sidebar.selectbox(
        T["profiles"],
        ["➕ " + T["add_member"]] + member_names
    )

    # ADD MEMBER
    if selected_name.startswith("➕"):

        st.title(T["add_member"])

        name = st.text_input(T["member_name"])
        age = st.number_input("Age", 1, 120)
        phone = st.text_input("Phone")

        medicines = []
        med_count = st.number_input("Number of medicines", 1, 10, 1)

        for i in range(med_count):
            med_name = st.text_input(f"Medicine {i}", key=f"med{i}")
            periods = st.multiselect(
                T["when"],
                ["Morning", "Afternoon", "Night"],
                key=f"time{i}"
            )
            food = st.selectbox(
                T["food"],
                [T["before"], T["after"]],
                key=f"food{i}"
            )

            medicines.append({
                "name": med_name,
                "periods": periods,
                "food": food
            })

        if st.button("Save"):
            add_member({
                "name": name,
                "age": age,
                "phone": phone,
                "medicines": medicines,
                "streak": 0,
                "health": 100
            })
            st.success("Member added!")

        st.stop()

    # CAREGIVER DASHBOARD
    member = next(m for m in members if m["name"] == selected_name)

    st.metric(T["health"], member.get("health", 100))
    st.metric(T["streak"], member.get("streak", 0))

    st.header(T["call_log"])

    if st.session_state.call_logs:
        for log in reversed(st.session_state.call_logs[-5:]):
            st.write(f"🕒 {log['time']} — {log['phone']} — {log['status']}")
    else:
        st.write(T["no_calls"])

# =====================================================
# RISK DISPLAY
# =====================================================
if 'missed_today' in locals():
    if missed_today == 0:
        st.success(T["risk_low"])
    elif missed_today == 1:
        st.warning(T["risk_med"])
    else:
        st.error(T["risk_high"])
