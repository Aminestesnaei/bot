from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

# توکن ربات
TOKEN = "7059609395:AAEBtLxm_kjoxmkazYwbEdzgCiIToghOkPs"

# لیست کانال‌ها
CHANNELS = {
    "کانال عمومی ایران انجوی": "https://t.me/iranenjoys1",
    "تور گروهی قشم ایران اینجوی": "https://t.me/IranEnjoy11",
    "تور گروهی گیلان ایران اینجوی": "https://t.me/GilanIranEnjooy",
    "تور گروهی گلستان ایران اینجوی": "https://t.me/GolestanIranEnjoy",
    "تور گروهی کویر مصر ایران اینجوی": "https://t.me/KavirMesrIranEnjoy",
    "تور گروهی خالد نبی ایران اینجوی": "https://t.me/KhalednabiIranEnjoy",
    "تور گروهی مرداب کندو ایران اینجوی": "https://t.me/MordabKandooIranEnjoy"
}

# لینک پی‌وی ادمین
ADMIN_LINK = "https://t.me/SalehifarH"

async def check_membership(user_id, bot):
    """ بررسی می‌کند که کاربر در کدام کانال‌ها عضو نیست """
    not_joined_channels = []  # لیست کانال‌هایی که کاربر عضو نیست

    for name, url in CHANNELS.items():
        try:
            chat_id = url.replace("https://t.me/", "")  # تبدیل لینک به chat_id
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in ["left", "kicked"]:
                not_joined_channels.append((name, url))  # ذخیره کانال‌هایی که عضو نیست
        except Exception:
            not_joined_channels.append((name, url))  # در صورت خطا، فرض می‌کنیم عضو نیست

    return not_joined_channels  # فقط کانال‌هایی که عضو نیست

async def start(update: Update, context):
    user_id = update.message.from_user.id
    bot = context.bot

    not_joined_channels = await check_membership(user_id, bot)

    if not not_joined_channels:
        # اگر عضو تمام کانال‌ها بود، پیام تماس با ادمین ارسال شود
        buttons = [[InlineKeyboardButton("💬 تماس با ادمین", url=ADMIN_LINK)]]
        await update.message.reply_text(
            "✅ شما قبلاً در تمام کانال‌ها عضو شده‌اید! برای دریافت اطلاعات بیشتر با ادمین تماس بگیرید. 🎁",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        # نمایش فقط کانال‌هایی که کاربر عضو نیست
        buttons = [[InlineKeyboardButton(f"🔹 {name}", url=url)] for name, url in not_joined_channels]
        buttons.append([InlineKeyboardButton("🔄 بررسی دوباره عضویت", callback_data="check")])

        await update.message.reply_text(
            "❌ شما هنوز در **همه کانال‌های مورد نیاز** عضو نشده‌اید!\n\n"
            "🔹 لطفاً در **کانال‌های زیر** عضو شوید و سپس روی **بررسی دوباره عضویت** کلیک کنید:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

async def check_membership_callback(update: Update, context):
    """ بررسی دوباره عضویت کاربر در کانال‌ها هنگام کلیک روی دکمه بررسی """
    query = update.callback_query
    user_id = query.from_user.id
    bot = context.bot

    not_joined_channels = await check_membership(user_id, bot)

    if not not_joined_channels:
        # اگر حالا عضو شد، دکمه ادمین را ارسال کند
        buttons = [[InlineKeyboardButton("💬 تماس با ادمین", url=ADMIN_LINK)]]
        await query.message.edit_text(
            "✅ تبریک! شما اکنون در تمام کانال‌ها عضو هستید. برای ارتباط با ادمین، روی دکمه زیر کلیک کنید. 🎁",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        # نمایش فقط کانال‌هایی که هنوز عضو نشده است
        buttons = [[InlineKeyboardButton(f"🔹 {name}", url=url)] for name, url in not_joined_channels]
        buttons.append([InlineKeyboardButton("🔄 بررسی دوباره عضویت", callback_data="check")])

        await query.message.edit_text(
            "❌ شما هنوز در **برخی از کانال‌ها** عضو نشده‌اید!\n\n"
            "🔹 لطفاً در **کانال‌های زیر** عضو شوید و دوباره امتحان کنید:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_membership_callback, pattern="check"))
    app.run_polling()

if __name__ == "__main__":
    main()
