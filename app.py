###### import streamlit as st

###### import google.generativeai as genai

###### import time

###### from PIL import Image

###### 

###### \# ==========================================

###### \# 1. إعدادات الصفحة

###### \# ==========================================

###### st.set\_page\_config(page\_title="AutoChapeau Vision", page\_icon="🚗", layout="centered")

###### 

###### \# ==========================================

###### \# 2. إدارة حالة الجلسة (البيانات، اللغة، الثيم)

###### \# ==========================================

###### if 'lang' not in st.session\_state:

###### &#x20;   st.session\_state.lang = "العربية"

###### if 'theme\_mode' not in st.session\_state:

###### &#x20;   st.session\_state.theme\_mode = "Light"

###### if 'step' not in st.session\_state:

###### &#x20;   st.session\_state.step = 0

###### if 'logged\_in' not in st.session\_state:

###### &#x20;   st.session\_state.logged\_in = False

###### if 'car\_data' not in st.session\_state:

###### &#x20;   st.session\_state.car\_data = {}

###### if 'history' not in st.session\_state:

###### &#x20;   st.session\_state.history = \[] 

###### if 'current\_prompt' not in st.session\_state:

###### &#x20;   st.session\_state.current\_prompt = ""

###### 

###### def next\_step():

###### &#x20;   st.session\_state.step += 1

###### 

###### def prev\_step():

###### &#x20;   if st.session\_state.step > 1:

###### &#x20;       st.session\_state.step -= 1

###### 

###### \# ==========================================

###### \# 3. القائمة الجانبية (اللغة والثيم)

###### \# ==========================================

###### st.sidebar.title("⚙️ الإعدادات / Settings")

###### 

###### \# مبدل اللغة

###### st.session\_state.lang = st.sidebar.radio("🌍 Language / اللغة", \["العربية", "English"], index=0 if st.session\_state.lang == "العربية" else 1)

###### 

###### st.sidebar.divider()

###### 

###### \# مبدل الثيم (Light/Dark)

###### theme\_choice = st.sidebar.radio("🌓 Theme / المظهر", \["Light / فاتح", "Dark / داكن"], index=0 if st.session\_state.theme\_mode == "Light" else 1)

###### st.session\_state.theme\_mode = "Light" if "Light" in theme\_choice else "Dark"

###### 

###### \# ==========================================

###### \# 4. إعدادات الألوان والثيم (CSS Injection)

###### \# ==========================================

###### PRIMARY\_COLOR = "#8A1538"

###### SECONDARY\_COLOR = "#58595B"

###### 

###### if st.session\_state.theme\_mode == "Dark":

###### &#x20;   BG\_COLOR = "#121212"

###### &#x20;   TEXT\_COLOR = "#F0F0F0"

###### &#x20;   INPUT\_BG = "#1E1E1E"

###### else:

###### &#x20;   BG\_COLOR = "#FFFFFF"

###### &#x20;   TEXT\_COLOR = "#121212"

###### &#x20;   INPUT\_BG = "#F9F9F9"

###### 

###### st.markdown(f"""

###### &#x20;   <style>

###### &#x20;   /\* تغيير ألوان الخلفية والنصوص الأساسية \*/

###### &#x20;   .stApp {{

###### &#x20;       background-color: {BG\_COLOR};

###### &#x20;       color: {TEXT\_COLOR};

###### &#x20;   }}

###### &#x20;   h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{

###### &#x20;       color: {TEXT\_COLOR} !important;

###### &#x20;   }}

###### &#x20;   /\* تخصيص نصوص العناوين بهوية الشركة \*/

###### &#x20;   .title-text {{

###### &#x20;       color: {PRIMARY\_COLOR} !important;

###### &#x20;       font-family: 'Arial', sans-serif;

###### &#x20;       text-align: center;

###### &#x20;   }}

###### &#x20;   .subtitle-text {{

###### &#x20;       color: {SECONDARY\_COLOR} !important;

###### &#x20;       text-align: center;

###### &#x20;       font-style: italic;

###### &#x20;   }}

###### &#x20;   /\* تخصيص الأزرار \*/

###### &#x20;   .stButton>button {{

###### &#x20;       background-color: {PRIMARY\_COLOR};

###### &#x20;       color: white !important;

###### &#x20;       border-radius: 8px;

###### &#x20;       border: none;

###### &#x20;       padding: 10px 24px;

###### &#x20;       font-weight: bold;

###### &#x20;   }}

###### &#x20;   .stButton>button:hover {{

###### &#x20;       background-color: {SECONDARY\_COLOR};

###### &#x20;       color: white !important;

###### &#x20;   }}

###### &#x20;   </style>

###### """, unsafe\_allow\_html=True)

###### 

###### 

###### \# ==========================================

###### \# 5. إعدادات الترجمة (Dictionary)

###### \# ==========================================

###### translations = {

###### &#x20;   "العربية": {

###### &#x20;       "login\_title": "تسجيل دخول المناديب",

###### &#x20;       "username": "اسم المستخدم",

###### &#x20;       "password": "كلمة المرور",

###### &#x20;       "login\_btn": "دخول",

###### &#x20;       "login\_success": "تم تسجيل الدخول بنجاح!",

###### &#x20;       "login\_error": "اسم المستخدم أو كلمة المرور غير صحيحة.",

###### &#x20;       "step1\_title": "الخطوة 1: معلومات السيارة الأساسية",

###### &#x20;       "brand": "العلامة التجارية",

###### &#x20;       "model": "فئة السيارة (مثال: S-Class, G-Wagon)",

###### &#x20;       "year": "سنة التصنيع",

###### &#x20;       "next": "التالي",

###### &#x20;       "logout": "تسجيل الخروج",

###### &#x20;       "warn\_model": "الرجاء إدخال فئة السيارة.",

###### &#x20;       "step2\_title": "الخطوة 2: تفاصيل التعديل",

###### &#x20;       "mod\_type": "نوع التعديل",

###### &#x20;       "exterior": "خارجي (Exterior)",

###### &#x20;       "interior": "داخلي (Interior)",

###### &#x20;       "color": "اللون المطلوب (اسم اللون أو كود Hex)",

###### &#x20;       "extra\_mods": "تعديلات إضافية (عربي أو إنجليزي)",

###### &#x20;       "prev\_btn": "السابق (تعديل بيانات السيارة)",

###### &#x20;       "generate\_btn": "توليد الصورة المبدئية",

###### &#x20;       "warn\_color": "الرجاء إدخال اللون.",

###### &#x20;       "step3\_title": "نتيجة التعديل الحالية",

###### &#x20;       "mod\_num": "تعديل رقم",

###### &#x20;       "any\_more\_mods": "### هل يوجد أي تعديل إضافي؟",

###### &#x20;       "new\_mod\_input": "أدخل التعديل الإضافي (أو اترك الحقل فارغاً):",

###### &#x20;       "back\_btn": "رجوع للخطوة السابقة",

###### &#x20;       "apply\_mod\_btn": "تطبيق التعديل الإضافي",

###### &#x20;       "warn\_extra": "الرجاء كتابة التعديل الإضافي.",

###### &#x20;       "finish\_btn": "لا يوجد تعديل، عرض النتيجة النهائية",

###### &#x20;       "final\_title": "النتيجة النهائية لمعرض AutoChapeau",

###### &#x20;       "design\_success": "تم إنهاء التصميم بنجاح!",

###### &#x20;       "history\_title": "مراحل التعديل (History):",

###### &#x20;       "version": "النسخة",

###### &#x20;       "video\_title": "فيديو 360 درجة للسيارة (بعد التعديل النهائي)",

###### &#x20;       "new\_project\_btn": "بدء مشروع جديد لعميل آخر",

###### &#x20;       "loading": "AutoChapeau AI يقوم بتطبيق التعديلات... الرجاء الانتظار"

###### &#x20;   },

###### &#x20;   "English": {

###### &#x20;       "login\_title": "Agent Login",

###### &#x20;       "username": "Username",

###### &#x20;       "password": "Password",

###### &#x20;       "login\_btn": "Login",

###### &#x20;       "login\_success": "Logged in successfully!",

###### &#x20;       "login\_error": "Invalid username or password.",

###### &#x20;       "step1\_title": "Step 1: Basic Car Information",

###### &#x20;       "brand": "Brand",

###### &#x20;       "model": "Car Model (e.g., S-Class, G-Wagon)",

###### &#x20;       "year": "Manufacture Year",

###### &#x20;       "next": "Next",

###### &#x20;       "logout": "Logout",

###### &#x20;       "warn\_model": "Please enter the car model.",

###### &#x20;       "step2\_title": "Step 2: Modification Details",

###### &#x20;       "mod\_type": "Modification Type",

###### &#x20;       "exterior": "Exterior",

###### &#x20;       "interior": "Interior",

###### &#x20;       "color": "Requested Color (Name or Hex Code)",

###### &#x20;       "extra\_mods": "Extra modifications (Arabic or English)",

###### &#x20;       "prev\_btn": "Previous (Edit Car Info)",

###### &#x20;       "generate\_btn": "Generate Initial Image",

###### &#x20;       "warn\_color": "Please enter a color.",

###### &#x20;       "step3\_title": "Current Modification Result",

###### &#x20;       "mod\_num": "Modification #",

###### &#x20;       "any\_more\_mods": "### Any additional modifications?",

###### &#x20;       "new\_mod\_input": "Enter extra modification (or leave empty):",

###### &#x20;       "back\_btn": "Go Back",

###### &#x20;       "apply\_mod\_btn": "Apply Extra Modification",

###### &#x20;       "warn\_extra": "Please type the extra modification.",

###### &#x20;       "finish\_btn": "No more mods, Show Final Result",

###### &#x20;       "final\_title": "AutoChapeau Showroom Final Result",

###### &#x20;       "design\_success": "Design completed successfully!",

###### &#x20;       "history\_title": "Modification Stages (History):",

###### &#x20;       "version": "Version",

###### &#x20;       "video\_title": "360 Degree Car Video (Final)",

###### &#x20;       "new\_project\_btn": "Start new project for another client",

###### &#x20;       "loading": "AutoChapeau AI is applying modifications... Please wait"

###### &#x20;   }

###### }

###### t = translations\[st.session\_state.lang] 

###### 

###### \# ==========================================

###### \# 6. إعدادات Google Gemini API

###### \# ==========================================

###### GEMINI\_API\_KEY = "AIzaSyDEtiBHPv4jTSI7dde0ff-DpLI2bgZJUJ0" 

###### genai.configure(api\_key=GEMINI\_API\_KEY)

###### 

###### def generate\_car\_image(prompt):

###### &#x20;   with st.spinner(t\["loading"]):

###### &#x20;       time.sleep(3) 

###### &#x20;       # ملاحظة: تم وضع صورة مؤقتة هنا كعينة.

###### &#x20;       return "https://via.placeholder.com/800x400.png?text=AutoChapeau+Generated+Car+Image"

###### 

###### \# ==========================================

###### \# 7. واجهة المستخدم والتنقل

###### \# ==========================================

###### try:

###### &#x20;   # محاولة عرض الشعار، في حال كان الثيم داكناً يمكن استخدام شعار معدل إذا توفر

###### &#x20;   logo = Image.open("AutoChapeau Logo.png")

###### &#x20;   st.image(logo, use\_container\_width=True)

###### except:

###### &#x20;   st.markdown("<h1 class='title-text'>AutoChapeau Vision</h1>", unsafe\_allow\_html=True)

###### &#x20;   st.markdown("<h4 class='subtitle-text'>World of luxury</h4>", unsafe\_allow\_html=True)

###### 

###### 

###### \# --- الخطوة 0 ---

###### if st.session\_state.step == 0:

###### &#x20;   st.subheader(t\["login\_title"])

###### &#x20;   users = {"agent1": "pass123", "admin": "admin2026"}

###### &#x20;   username = st.text\_input(t\["username"])

###### &#x20;   password = st.text\_input(t\["password"], type="password")

###### &#x20;   if st.button(t\["login\_btn"]):

###### &#x20;       if username in users and users\[username] == password:

###### &#x20;           st.session\_state.logged\_in = True

###### &#x20;           st.success(t\["login\_success"])

###### &#x20;           next\_step()

###### &#x20;           st.rerun()

###### &#x20;       else:

###### &#x20;           st.error(t\["login\_error"])

###### 

###### \# --- الخطوة 1 ---

###### elif st.session\_state.step == 1 and st.session\_state.logged\_in:

###### &#x20;   st.subheader(t\["step1\_title"])

###### &#x20;   brand\_options = \["مرسيدس / Mercedes", "بي إم دبليو / BMW", "رينج روفر / Range Rover", "بورش / Porsche", "أودي / Audi", "أخرى / Other"]

###### &#x20;   brand = st.selectbox(t\["brand"], brand\_options)

###### &#x20;   model = st.text\_input(t\["model"])

###### &#x20;   year = st.selectbox(t\["year"], list(range(2027, 2010, -1)))

###### &#x20;   

###### &#x20;   col1, col2 = st.columns(2)

###### &#x20;   with col1:

###### &#x20;       if st.button(t\["next"]):

###### &#x20;           if model:

###### &#x20;               st.session\_state.car\_data\['brand'] = brand

###### &#x20;               st.session\_state.car\_data\['model'] = model

###### &#x20;               st.session\_state.car\_data\['year'] = str(year)

###### &#x20;               next\_step()

###### &#x20;               st.rerun()

###### &#x20;           else:

###### &#x20;               st.warning(t\["warn\_model"])

###### &#x20;   with col2:

###### &#x20;       if st.button(t\["logout"]):

###### &#x20;           st.session\_state.clear()

###### &#x20;           st.rerun()

###### 

###### \# --- الخطوة 2 ---

###### elif st.session\_state.step == 2:

###### &#x20;   st.subheader(t\["step2\_title"])

###### &#x20;   mod\_type = st.radio(t\["mod\_type"], \[t\["exterior"], t\["interior"]])

###### &#x20;   color = st.text\_input(t\["color"])

###### &#x20;   extra\_mods = st.text\_area(t\["extra\_mods"])

###### &#x20;   

###### &#x20;   col1, col2 = st.columns(2)

###### &#x20;   with col2:

###### &#x20;       if st.button(t\["prev\_btn"]):

###### &#x20;           prev\_step()

###### &#x20;           st.rerun()

###### &#x20;   with col1:

###### &#x20;       if st.button(t\["generate\_btn"]):

###### &#x20;           if color:

###### &#x20;               st.session\_state.car\_data\['mod\_type'] = mod\_type

###### &#x20;               st.session\_state.car\_data\['color'] = color

###### &#x20;               st.session\_state.car\_data\['extra\_mods'] = extra\_mods

###### &#x20;               

###### &#x20;               prompt = f"Realistic high-quality photo of a {st.session\_state.car\_data\['year']} {st.session\_state.car\_data\['brand']} {st.session\_state.car\_data\['model']}. View: {mod\_type}. The main color is {color}. Additional modifications to apply exactly as requested: {extra\_mods}. Cinematic lighting, luxury automotive photography style."

###### &#x20;               

###### &#x20;               st.session\_state.current\_prompt = prompt

###### &#x20;               img\_url = generate\_car\_image(prompt)

###### &#x20;               st.session\_state.history.append({"prompt": prompt, "image": img\_url, "iteration": 1})

###### &#x20;               next\_step()

###### &#x20;               st.rerun()

###### &#x20;           else:

###### &#x20;               st.warning(t\["warn\_color"])

###### 

###### \# --- الخطوة 3 ---

###### elif st.session\_state.step == 3:

###### &#x20;   st.subheader(t\["step3\_title"])

###### &#x20;   latest\_generation = st.session\_state.history\[-1]

###### &#x20;   st.image(latest\_generation\["image"], caption=f"{t\['mod\_num']} {latest\_generation\['iteration']}", use\_container\_width=True)

###### &#x20;   

###### &#x20;   st.divider()

###### &#x20;   st.markdown(t\["any\_more\_mods"])

###### &#x20;   new\_mod = st.text\_input(t\["new\_mod\_input"], key="new\_mod\_input")

###### &#x20;   

###### &#x20;   col1, col2, col3 = st.columns(3)

###### &#x20;   with col3:

###### &#x20;       if st.button(t\["back\_btn"]):

###### &#x20;           st.session\_state.history.pop()

###### &#x20;           prev\_step()

###### &#x20;           st.rerun()

###### &#x20;   with col2:

###### &#x20;       if st.button(t\["apply\_mod\_btn"]):

###### &#x20;           if new\_mod:

###### &#x20;               updated\_prompt = latest\_generation\["prompt"] + f" Now apply this new change to the vehicle: {new\_mod}. Keep previous realistic luxury style."

###### &#x20;               img\_url = generate\_car\_image(updated\_prompt)

###### &#x20;               st.session\_state.history.append({"prompt": updated\_prompt, "image": img\_url, "iteration": latest\_generation\['iteration'] + 1})

###### &#x20;               st.rerun()

###### &#x20;           else:

###### &#x20;               st.warning(t\["warn\_extra"])

###### &#x20;   with col1:

###### &#x20;       if st.button(t\["finish\_btn"], type="primary"):

###### &#x20;           next\_step()

###### &#x20;           st.rerun()

###### 

###### \# --- الخطوة 4 ---

###### elif st.session\_state.step == 4:

###### &#x20;   st.markdown(f"<h2 class='title-text'>{t\['final\_title']}</h2>", unsafe\_allow\_html=True)

###### &#x20;   st.success(t\["design\_success"])

###### &#x20;   

###### &#x20;   st.subheader(t\["history\_title"])

###### &#x20;   cols = st.columns(len(st.session\_state.history))

###### &#x20;   for idx, item in enumerate(st.session\_state.history):

###### &#x20;       with cols\[idx]:

###### &#x20;           st.image(item\["image"], caption=f"{t\['version']} {idx + 1}")

###### &#x20;   

###### &#x20;   st.divider()

###### &#x20;   st.subheader(t\["video\_title"])

###### &#x20;   st.video("https://www.w3schools.com/html/mov\_bbb.mp4") 

###### &#x20;   

###### &#x20;   if st.button(t\["new\_project\_btn"]):

###### &#x20;       st.session\_state.step = 1

###### &#x20;       st.session\_state.car\_data = {}

###### &#x20;       st.session\_state.history = \[]

###### &#x20;       st.session\_state.current\_prompt = ""

###### &#x20;       st.rerun()

