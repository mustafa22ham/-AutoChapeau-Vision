import streamlit as st
import google.generativeai as genai
import time
from PIL import Image

# ==========================================
# 1. إعدادات الصفحة الأساسية
# ==========================================
st.set_page_config(page_title="AutoChapeau Vision", page_icon="🚗", layout="centered")

# ==========================================
# 2. إدارة حالة الجلسة
# ==========================================
if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'car_data' not in st.session_state:
    st.session_state.car_data = {}
if 'history' not in st.session_state:
    st.session_state.history = [] 
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = ""

def next_step():
    st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# ==========================================
# 3. القائمة الجانبية واللغة
# ==========================================
st.sidebar.title("🌍 Language / اللغة")
st.session_state.lang = st.sidebar.radio("", ["العربية", "English"], index=0 if st.session_state.lang == "العربية" else 1)

# قاموس الترجمة
translations = {
    "العربية": {
        "login_title": "تسجيل دخول المناديب",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "دخول",
        "login_success": "تم تسجيل الدخول بنجاح!",
        "login_error": "اسم المستخدم أو كلمة المرور غير صحيحة.",
        "step1_title": "الخطوة 1: معلومات السيارة الأساسية",
        "brand": "العلامة التجارية",
        "model": "فئة السيارة (مثال: S-Class)",
        "year": "سنة التصنيع",
        "next": "التالي",
        "logout": "تسجيل الخروج",
        "warn_model": "الرجاء إدخال فئة السيارة.",
        "step2_title": "الخطوة 2: تفاصيل التعديل",
        "mod_type": "نوع التعديل",
        "exterior": "خارجي (Exterior)",
        "interior": "داخلي (Interior)",
        "color": "اللون المطلوب",
        "extra_mods": "تعديلات إضافية",
        "prev_btn": "السابق",
        "generate_btn": "توليد الصورة المبدئية",
        "warn_color": "الرجاء إدخال اللون.",
        "step3_title": "نتيجة التعديل الحالية",
        "mod_num": "تعديل رقم",
        "any_more_mods": "### هل يوجد أي تعديل إضافي؟",
        "new_mod_input": "أدخل التعديل الإضافي:",
        "back_btn": "رجوع",
        "apply_mod_btn": "تطبيق التعديل",
        "warn_extra": "الرجاء كتابة التعديل.",
        "finish_btn": "عرض النتيجة النهائية",
        "final_title": "النتيجة النهائية",
        "design_success": "تم إنهاء التصميم بنجاح!",
        "history_title": "مراحل التعديل:",
        "version": "النسخة",
        "video_title": "فيديو 360 درجة",
        "new_project_btn": "مشروع جديد",
        "loading": "جاري تطبيق التعديلات..."
    },
    "English": {
        "login_title": "Agent Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Login",
        "login_success": "Logged in successfully!",
        "login_error": "Invalid credentials.",
        "step1_title": "Step 1: Car Info",
        "brand": "Brand",
        "model": "Model (e.g., S-Class)",
        "year": "Year",
        "next": "Next",
        "logout": "Logout",
        "warn_model": "Enter car model.",
        "step2_title": "Step 2: Modifications",
        "mod_type": "Type",
        "exterior": "Exterior",
        "interior": "Interior",
        "color": "Color",
        "extra_mods": "Extra mods",
        "prev_btn": "Previous",
        "generate_btn": "Generate Image",
        "warn_color": "Enter a color.",
        "step3_title": "Current Result",
        "mod_num": "Mod #",
        "any_more_mods": "### More modifications?",
        "new_mod_input": "Enter extra mod:",
        "back_btn": "Back",
        "apply_mod_btn": "Apply Mod",
        "warn_extra": "Type a mod.",
        "finish_btn": "Show Final Result",
        "final_title": "Final Result",
        "design_success": "Done!",
        "history_title": "History:",
        "version": "Version",
        "video_title": "360 Video",
        "new_project_btn": "New Project",
        "loading": "Applying mods..."
    }
}
t = translations[st.session_state.lang]

# ==========================================
# 4. إعدادات API
# ==========================================
GEMINI_API_KEY = "AIzaSyDEtiBHPv4jTSI7dde0ff-DpLI2bgZJUJ0" 
genai.configure(api_key=GEMINI_API_KEY)

def generate_car_image(prompt):
    with st.spinner(t["loading"]):
        time.sleep(3) 
        return "https://via.placeholder.com/800x400.png?text=AutoChapeau+Generated+Car+Image"

# ==========================================
# 5. واجهة المستخدم والتنقل
# ==========================================
try:
    logo = Image.open("AutoChapeau Logo.png")
    st.image(logo, use_container_width=True)
except:
    st.title("AutoChapeau Vision")

# --- الخطوة 0 ---
if st.session_state.step == 0:
    st.subheader(t["login_title"])
    users = {"agent1": "pass123", "admin": "admin2026"}
    username = st.text_input(t["username"])
    password = st.text_input(t["password"], type="password")
    if st.button(t["login_btn"]):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success(t["login_success"])
            next_step()
            st.rerun()
        else:
            st.error(t["login_error"])

# --- الخطوة 1 ---
elif st.session_state.step == 1 and st.session_state.logged_in:
    st.subheader(t["step1_title"])
    brand = st.selectbox(t["brand"], ["Mercedes", "BMW", "Range Rover", "Porsche", "Audi", "Other"])
    model = st.text_input(t["model"])
    year = st.selectbox(t["year"], list(range(2027, 2010, -1)))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["next"]):
            if model:
                st.session_state.car_data['brand'] = brand
                st.session_state.car_data['model'] = model
                st.session_state.car_data['year'] = str(year)
                next_step()
                st.rerun()
            else:
                st.warning(t["warn_model"])
    with col2:
        if st.button(t["logout"]):
            st.session_state.clear()
            st.rerun()

# --- الخطوة 2 ---
elif st.session_state.step == 2:
    st.subheader(t["step2_title"])
    mod_type = st.radio(t["mod_type"], [t["exterior"], t["interior"]])
    color = st.text_input(t["color"])
    extra_mods = st.text_area(t["extra_mods"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["generate_btn"]):
            if color:
                st.session_state.car_data['mod_type'] = mod_type
                st.session_state.car_data['color'] = color
                prompt = f"Car {st.session_state.car_data['brand']} {st.session_state.car_data['model']}. Color: {color}. Mods: {extra_mods}"
                st.session_state.current_prompt = prompt
                img_url = generate_car_image(prompt)
                st.session_state.history.append({"prompt": prompt, "image": img_url, "iteration": 1})
                next_step()
                st.rerun()
            else:
                st.warning(t["warn_color"])
    with col2:
        if st.button(t["prev_btn"]):
            prev_step()
            st.rerun()

# --- الخطوة 3 ---
elif st.session_state.step == 3:
    st.subheader(t["step3_title"])
    latest_gen = st.session_state.history[-1]
    st.image(latest_gen["image"], caption=f"{t['mod_num']} {latest_gen['iteration']}", use_container_width=True)
    
    st.markdown(t["any_more_mods"])
    new_mod = st.text_input(t["new_mod_input"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(t["finish_btn"]):
            next_step()
            st.rerun()
    with col2:
        if st.button(t["apply_mod_btn"]):
            if new_mod:
                updated_prompt = latest_gen["prompt"] + f" Add: {new_mod}"
                img_url = generate_car_image(updated_prompt)
                st.session_state.history.append({"prompt": updated_prompt, "image": img_url, "iteration": latest_gen['iteration'] + 1})
                st.rerun()
            else:
                st.warning(t["warn_extra"])
    with col3:
        if st.button(t["back_btn"]):
            st.session_state.history.pop()
            prev_step()
            st.rerun()

# --- الخطوة 4 ---
elif st.session_state.step == 4:
    st.title(t["final_title"])
    st.success(t["design_success"])
    
    st.subheader(t["history_title"])
    cols = st.columns(len(st.session_state.history))
    for idx, item in enumerate(st.session_state.history):
        with cols[idx]:
            st.image(item["image"], caption=f"{t['version']} {idx + 1}")
    
    st.divider()
    if st.button(t["new_project_btn"]):
        st.session_state.step = 1
        st.session_state.car_data = {}
        st.session_state.history = []
        st.rerun()
