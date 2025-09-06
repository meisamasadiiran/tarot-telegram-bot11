import telebot
import random
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8333098744:AAG60huJyo0PRLpEvakrG4H2-YKQUCCVqGk"
bot = telebot.TeleBot(BOT_TOKEN)

# ذخیره زمان آخرین فال برای هر کاربر
last_usage = {}

# کارت های تاروت (۲۲ ماژور آرکانا)
tarot_cards = {
    "احمق": "شروع جدید، ماجراجویی، آزادی از ترس",
    "جادوگر": "قدرت اراده، خلاقیت، توانایی تحقق آرزوها",
    "کاهنه اعظم": "شهود، اسرار، دانایی پنهان",
    "امپراتریس": "مادری، عشق بی‌قید، حاصلخیزی",
    "امپراتور": "اقتدار، رهبری، نظم و قانون",
    "کشیش اعظم": "سنت، آموزش، راهنمایی معنوی",
    "عاشقان": "عشق، انتخاب سرنوشت‌ساز، رابطه عاطفی",
    "ارابه": "پیروزی، اراده قوی، حرکت به جلو",
    "قدرت": "شجاعت درونی، کنترل نفس، قدرت آرام",
    "زاهد": "جستجوی درونی، تنهایی، حکمت",
    "چرخ سرنوشت": "تغییر، چرخه زندگی، سرنوشت",
    "عدالت": "حقیقت، تعادل، نتیجه منصفانه",
    "معلق": "توقف، دیدگاه جدید، رها کردن",
    "مرگ": "پایان، دگرگونی، شروع دوباره",
    "اعتدال": "تعادل، هماهنگی، صبر",
    "شیطان": "وسوسه، قید و بند، ترس درونی",
    "برج": "شوک، فروپاشی ناگهانی، تغییر ناگزیر",
    "ستاره": "امید، الهام، ایمان",
    "ماه": "توهم، شهود، نااطمینانی",
    "خورشید": "شادی، موفقیت، روشنایی",
    "داوری": "بیداری، تصمیم مهم، رستاخیز",
    "جهان": "تکامل، موفقیت نهایی، کامل شدن"
}

# پیام انگیزشی
motivational = [
    "✨ هر پایانی شروع جدیدی است",
    "🌟 قدرت تغییر در دستان توست",
    "💫 به شهودت اعتماد کن",
    "🌙 صبر کن، زمان مناسب فرا میرسد"
]

# start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔮 سلام! برای انتخاب نوع فال دستور /tarot رو بزن 🌟")

# انتخاب نوع فال
@bot.message_handler(commands=['tarot'])
def choose_tarot(message):
    user_id = message.from_user.id
    now = time.time()

    # محدودیت 24 ساعت (86400 ثانیه)
    if user_id in last_usage and now - last_usage[user_id] < 86400:
        remaining = int(86400 - (now - last_usage[user_id])) // 3600
        bot.reply_to(message, f"⏳ شما روزی فقط یک بار می‌تونید فال بگیرید.\nلطفاً {remaining} ساعت دیگه دوباره امتحان کنید.")
        return

    # ذخیره زمان جدید
    last_usage[user_id] = now

    # ساخت کیبورد انتخاب
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("❤️ فال احساسی", callback_data="emotional"),
        InlineKeyboardButton("🕰 گذشته/حال/آینده", callback_data="timeline"),
        InlineKeyboardButton("💖 فال عشق", callback_data="love"),
        InlineKeyboardButton("⚖️ فال تصمیم‌گیری", callback_data="decision")
    )
    bot.send_message(message.chat.id, "کدوم فال رو میخوای؟ 🔮", reply_markup=markup)

# هندلر انتخاب فال
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in ["emotional", "timeline", "love", "decision"]:
        cards = random.sample(list(tarot_cards.items()), 3)  # انتخاب ۳ کارت تصادفی
        msg = random.choice(motivational)

        if call.data == "emotional":
            title = "❤️ فال احساسی"
            meaning_type = ["درون قلبت", "در احساساتت", "در آینده‌ی عشقی"]
        elif call.data == "timeline":
            title = "🕰 فال گذشته / حال / آینده"
            meaning_type = ["گذشته", "حال", "آینده"]
        elif call.data == "love":
            title = "💖 فال عشق"
            meaning_type = ["تو", "او", "رابطه"]
        elif call.data == "decision":
            title = "⚖️ فال تصمیم‌گیری"
            meaning_type = ["گزینه اول", "گزینه دوم", "نتیجه"]

        text = f"{title}\n\n"
        for i, (card, meaning) in enumerate(cards):
            text += f"🎴 {meaning_type[i]}:\n{card} → {meaning}\n\n"
        text += f"{msg}\n\n☕ برای فال کامل به همراه قهوه به تلگرام @falfalika پیام بدین"

        bot.send_message(call.message.chat.id, text)

# اجرای ربات
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"⚠️ خطا در polling: {e}")
        time.sleep(5)
