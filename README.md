# 🤖 Telegram FAQ Bot

بوت تليجرام ذكي للرد على الأسئلة الشائعة مع دعم البحث الذكي والصور.

---

## ✨ المميزات

- ✅ بحث بالكلمات المفتاحية (فوري ودقيق)
- ✅ بحث Fuzzy للكلمات المكتوبة بشكل غير دقيق
- ✅ إرسال صور مع الردود
- ✅ دعم اللغة العربية بالكامل
- ✅ سهل التوسعة وإضافة أسئلة جديدة

---

## 📁 هيكل المشروع

```
telegram-bot/
├── bot.py              # الكود الرئيسي للبوت
├── requirements.txt    # المكتبات المطلوبة
├── Procfile            # ملف تشغيل على السيرفر
├── runtime.txt         # إصدار Python
├── .env.example        # مثال على متغيرات البيئة
├── .gitignore          # الملفات المستثناة من GitHub
├── images/             # مجلد الصور (ضع صورك هنا)
│   ├── خصم بنك اهلى.jpg
│   ├── خصم بابلو.jpg
│   └── خصم مهندسين.jpg
└── README.md
```

---

## 🚀 طريقة التشغيل المحلي

### 1. استنساخ المشروع
```bash
git clone https://github.com/username/telegram-bot.git
cd telegram-bot
```

### 2. إنشاء بيئة افتراضية
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 4. إعداد التوكن
```bash
# انسخ ملف المثال
cp .env.example .env

# افتح .env وضع التوكن الخاص بك
BOT_TOKEN=your_token_here
```

### 5. تشغيل البوت
```bash
python bot.py
```

---

## ☁️ الاستضافة المجانية على Railway

1. سجّل على [railway.app](https://railway.app) بحساب GitHub
2. اضغط **New Project** → **Deploy from GitHub repo**
3. اختر الريبو بتاعك
4. اضغط على المشروع → **Variables** → أضف:
   - `BOT_TOKEN` = توكن البوت
5. اضغط **Deploy** ✅

---

## ➕ إضافة سؤال جديد

افتح `bot.py` وأضف في قاموس `QUESTIONS`:

```python
"اسم السؤال": {
    "keywords": ["كلمة1", "كلمة2"],
    "answer": "الرد هنا",
    "photo": "images/اسم_الصورة.jpg"  # أو None لو مفيش صورة
},
```

---

## 🔑 الحصول على توكن البوت

1. افتح تليجرام وابحث عن `@BotFather`
2. ابعت `/newbot`
3. اتبع التعليمات واحصل على التوكن
4. ضع التوكن في متغير البيئة `BOT_TOKEN`

---

## 📦 المكتبات المستخدمة

| المكتبة | الغرض |
|---------|--------|
| `python-telegram-bot` | التواصل مع Telegram API |
| `rapidfuzz` | البحث الذكي في النصوص |
