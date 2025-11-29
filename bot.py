import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]  # ✅ 从环境变量读取

# ================== 主選單鍵盤 ==================
MENU_KEYBOARD = [
    ["禄鼎记餐厅菜单", "禄鼎记-4楼KTV包厢", "禄鼎记客房"],
    ["梦田-KTV包厢", "梦田-大厅卡座"],
    ["中国美女", "联系方式"]
]

MENU_MARKUP = ReplyKeyboardMarkup(
    MENU_KEYBOARD,
    resize_keyboard=True,
    one_time_keyboard=False
)

# 只有純文字回覆的按鈕（圖片 / 影片另外在程式裡特別處理）
MENU_ACTIONS = {
    "禄鼎记客房": "客房房间号\n-K01（二楼）\n-K02（三楼）\n-K03（三楼）\n-K05（三楼）\n-K06（四楼）\n-K08（四楼）\n联系方式，Cindy辛迪 \n@Cindyasdf",
}

# 工具函式：把 list 每 n 個切一組
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# ================== /start 指令 ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "嗨，歡迎使用本機器人！\n請從下面的菜單選擇功能 👇",
        reply_markup=MENU_MARKUP
    )

# ================== /help 指令 ==================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "指令說明：\n/start  顯示主菜單\n直接點下面的按鈕就能使用功能。",
        reply_markup=MENU_MARKUP
    )

# ================== 處理所有文字訊息 ==================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()

    # ---------- 1. 禄鼎记餐厅菜单：多張圖片相簿 ----------
    if text == "禄鼎记餐厅菜单":
        folder_path = "ludingji_menu"  # 放27張菜單圖的資料夾

        all_files = sorted(os.listdir(folder_path))
        image_files = [
            f for f in all_files
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]

        if not image_files:
            await update.message.reply_text("目前資料夾裡沒有找到圖片喔～", reply_markup=MENU_MARKUP)
            return

        # 每組 7 張發一個相簿
        groups = list(chunk_list(image_files, 7))

        for group in groups:
            media_group = []
            opened = []
            for filename in group:
                file_path = os.path.join(folder_path, filename)
                f = open(file_path, "rb")
                opened.append(f)
                media_group.append(InputMediaPhoto(media=f))

            await update.effective_chat.send_media_group(media_group)

            for f in opened:
                f.close()

            await asyncio.sleep(0.5)  # 稍微休息一下，避免太頻繁

        return

    # ---------- 2. 禄鼎记-4楼KTV包厢：單張圖片 + 文字 ----------
    if text == "禄鼎记-4楼KTV包厢":
        with open("ludingji_ktv.jpg", "rb") as img:
            caption = (
                "包厢消费：自己随意点酒，达到包厢低消即可！\n\n"
                "联系方式，Cindy辛迪 @Cindyasdf"
            )
            await update.message.reply_photo(
                photo=img,
                caption=caption,
                reply_markup=MENU_MARKUP
            )
        return

    # ---------- 3. 梦田-KTV包厢：單張圖片 + 文字 ----------
    if text == "梦田-KTV包厢":
        with open("mengtian_ktv.jpg", "rb") as img:
            caption = (
                "包厢消费：自己随意点酒，达到包厢低消即可！\n\n"
                "联系方式，Cindy辛迪 @Cindyasdf"
            )
            await update.message.reply_photo(
                photo=img,
                caption=caption,
                reply_markup=MENU_MARKUP
            )
        return

    # ---------- 4. 梦田-大厅卡座：單張圖片 + 文字 ----------
    if text == "梦田-大厅卡座":
        with open("mengtian_hall.jpg", "rb") as img:
            caption = "联系方式，Cindy辛迪 @Cindyasdf"
            await update.message.reply_photo(
                photo=img,
                caption=caption,
                reply_markup=MENU_MARKUP
            )
        return

    # ---------- 5. 中国美女：單張圖片 + 文字 ----------
    if text == "中国美女":
        with open("china_beauty.jpg", "rb") as img:
            caption = (
                "美女价格请看图\n\n"
                "美女频道请点链接\n\n"
                "https://t.me/BahaoYulechuanmei\n\n"
                "联系方式，Cindy辛迪 @Cindyasdf"
            )
            await update.message.reply_photo(
                photo=img,
                caption=caption,
                reply_markup=MENU_MARKUP
            )
        return

    # ---------- 6. 联系方式：多張圖片（資料夾） + 文案 ----------
    if text == "联系方式":

        # 6-1：多張圖片（從 contact_photos 資料夾）
        photo_folder = "contact_photos"
        if os.path.isdir(photo_folder):
            all_photos = sorted(os.listdir(photo_folder))
            photo_files = [
                f for f in all_photos
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            ]

            groups = list(chunk_list(photo_files, 10))

            for group in groups:
                media_group = []
                opened = []
                for filename in group:
                    p = os.path.join(photo_folder, filename)
                    f = open(p, "rb")
                    opened.append(f)
                    media_group.append(InputMediaPhoto(media=f))

                if media_group:
                    await update.effective_chat.send_media_group(media_group)

                for f in opened:
                    f.close()

                await asyncio.sleep(1)

        # 6-2：最後發一段長文字
        caption = (
            "禄鼎记-2楼海鲜姿造\n"
            "禄鼎记-3楼湖景客房\n"
            "禄鼎记-4楼KTV包厢\n"
            "梦田-KTV包厢\n"
            "梦田-大厅卡座\n\n"
            "小房888中房1288大房1588，这三种，自己点酒达到这个低消价格就行\n\n"
            "美女频道👇🏻\n"
            "https://t.me/BahaoYulechuanmei\n"
            "（有些妹妹没有笔记，推荐现场选）\n\n"
            "这两家KTV地址在：八号公馆一期二期\n"
            "（三期已打通）\n\n"
            "😍联系方式 😍@Cindyasdf"
        )

        await update.message.reply_text(
            caption,
            reply_markup=MENU_MARKUP
        )
        return

    # ---------- 7. 其他按鈕：用 MENU_ACTIONS ----------
    if text in MENU_ACTIONS:
        reply = MENU_ACTIONS[text]
        if reply:
            await update.message.reply_text(
                reply,
                reply_markup=MENU_MARKUP
            )
        else:
            await update.message.reply_text(
                "這個功能內容還在建置中～",
                reply_markup=MENU_MARKUP
            )
    else:
        await update.message.reply_text(
            "我看不懂這句～請用下面的按鈕選擇功能 😊",
            reply_markup=MENU_MARKUP
        )

# ================== 主程式入口 ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("Bot 已啟動，按 Ctrl+C 可停止。")
    app.run_polling()

if __name__ == "__main__":
    main()
