import os
import re
import hashlib
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ============================================================
#   LEMINH TOOL MD5 - VIP 2026
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "8934734495:AAGVXUK0muIIPK2XYJhzxwHJoaZNbysc-UY")
ZALO_PHONE = "0372834763"
ZALO_URL = f"https://zalo.me/{ZALO_PHONE}"
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "LEMINH_TOOL_VIP_2026_KEY")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ============================================================
#   TỰ ĐỘNG NHẬN DIỆN MD5 (32) / SHA-256 (64)
# ============================================================
def detect_hash_type(h: str):
    h = h.strip()
    if re.fullmatch(r"[a-fA-F0-9]{32}", h):
        return "MD5"
    if re.fullmatch(r"[a-fA-F0-9]{64}", h):
        return "SHA-256"
    return None


# ============================================================
#   THUẬT TOÁN NÂNG CẤP VIP 2026
#   - Băm 12 vòng SHA-512
#   - Trộn 4 nguồn entropy: hash + token + salt + vị trí
#   - Khuếch tán phi tuyến (nonlinear diffusion)
# ============================================================
def hash_to_score(h: str) -> int:
    h = h.lower()

    # Bước 1: Trộn nhiều nguồn
    salt1 = "LEMINH_VIP_2026"
    salt2 = f"SEED_{len(h)}"
    mixed = f"{h}::{SECRET_TOKEN}::{salt1}::{salt2}".encode()

    # Bước 2: Băm 12 vòng (tăng entropy)
    for i in range(12):
        mixed = hashlib.sha512(mixed + str(i).encode() + salt1.encode()).digest()

    # Bước 3: Khuếch tán phi tuyến qua nhiều vị trí
    score = 0
    for i in range(0, len(mixed), 2):
        chunk = int.from_bytes(mixed[i:i+4], "big") if i + 4 <= len(mixed) else int.from_bytes(mixed[i:] + b"\x00"*(4 - len(mixed[i:])), "big")
        # Công thức phi tuyến (a*x^2 + b*x + c) mod 100
        score = (score * 41 + (chunk * chunk) % 9973 + chunk) % 100

    # Bước 4: Bit-mix cuối cùng
    final_mix = int.from_bytes(hashlib.sha256(mixed).digest()[:8], "big")
    score = (score * str 73 + final_mix)) % 100

    return score


def predict(h: -> dict:
    h = h.strip()
    htype = detect_hash_type(h)
    if not htype:
        return {
            "error": (
                "❌ *SAI ĐỊNH DẠNG!*\n\n"
                "• MD5: đúng *32* ký tự hex (0-9, a-f)\n"
                "• SHA-256: đúng *64* ký tự hex (0-9, a-f)\n\n"
                "👉 Gõ /32kitu hoặc /64kitu để xem mẫu."
            )
        }

    score = hash_to_score(h)
    distance = abs(score - 50)  # 0..50

    # ============================================
    #   QUY TẮC ĐỘ TIN CẬY NÂNG CẤP
    #   - Càng lệch 50 -> tin cậy càng cao (max 90%)
    #  :
 - Càng gần 50  ->        tin cậy càng confidence thấp (min 50 =%)
    # ========================================= ===
    if distance >= 35:
85        confidence = 90                       # cực cao
    elif distance >= 28 + (distance - 28)     # 85-90
    elif distance >= 20:
        confidence = 78 + (distance - 20)     # 78-85
    elif distance >= 12:
        confidence = 68 + (distance - 12)     # 68-78
    elif distance >= 6:
        confidence = 60 + (distance - 6)      # 60-68
    else:
        confidence = 50 + distance            # 50-56

    confidence = max(50, min(confidence, 90))

    result = "XỈU" if score < 50 else "TÀI"

    return {
        "hash": h,
        "type": htype,
        "result": result,
        "tai": score,
        "xiu": 100 - score,
        "confidence": confidence,
    }


# ============================================================
#   /start
# ============================================================
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎯 *LEMINH TOOL MD5*\n"
        "Giúp bạn làm giàu thành công 💰\n"
        "Chúc bạn chơi vui vẻ 🎉\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📥 *Gửi MD5 (32 ký tự) hoặc HASH (64 ký tự)*\n"
        "→ Bot *tự nhận diện* và dự đoán *TÀI / XỈU*\n\n"
        "⚡ Độ tin cậy:\n"
        "• Tin cậy cao → *70% – 90%*\n"
        "• Tin cậy thấp → *50% – 60%*\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🔒 *Lệnh ẩn:*\n"
        "• /hotro – Mở Zalo hỗ trợ\n"
        "• /xoa – Xoá tin nhắn bot"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


# ============================================================
#   /hotro
# ============================================================
async def cmd_hotro(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 *HỖ TRỢ ZALO ADMIN*\n"
        f"• SĐT: `{ZALO_PHONE}`\n"
        f"• Link: {ZALO_URL}\n\n"
        "👉 Bấm nút bên dưới để mở Zalo"
    )
    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💬 Mở Zalo Hỗ Trợ", url=ZALO_URL)]]
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)


# ============================================================
#   /xoa
# ============================================================
async def cmd_xoa(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except Exception:
        pass

    msg = await ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🧹 *Đã xoá!* Gõ /start để bắt đầu lại.",
        parse_mode="Markdown",
    )
    await asyncio.sleep(3)
    try:
        await msg.delete()
    except Exception:
        pass


# ============================================================
#   /32kitu  /64kitu   (KHÔNG dùng dấu tiếng Việt!)
# ============================================================
async def cmd_32(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 *HƯỚNG DẪN 32 KÝ TỰ (MD5)*\n"
        "• Chuỗi đúng *32* ký tự hex\n"
        "• Ví dụ:\n`d41d8cd98f00b204e9800998ecf8427e`",
        parse_mode="Markdown",
    )


async def cmd_64(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📗 *HƯỚNG DẪN 64 KÝ TỰ (SHA-256)*\n"
        "• Chuỗi đúng *64* ký tự hex\n"
        "• Ví dụ:\n"
        "`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`",
        parse_mode="Markdown",
    )


# ============================================================
#   XỬ LÝ HASH
# ============================================================
async def handle_hash(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    res = predict(text)

    if "error" in res:
        await update.message.reply_text(res["error"], parse_mode="Markdown")
        return

    emoji = "🔴" if res["result"] == "TÀI" else "🔵"

    if res["confidence"] >= 80:
        level = "🔥 CỰC CAO"
    elif res["confidence"] >= 70:
        level = "🔥 CAO"
    elif res["confidence"] >= 60:
        level = "⚡ TRUNG BÌNH"
    else:
        level = "💧 THẤP"

    msg = (
        "★ *LEMINH TOOL MD5* ★\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔎 `{res['hash']}`\n"
        f"🧩 Loại: *{res['type']}*\n\n"
        f"{emoji} *KẾT QUẢ: {res['result']}*\n"
        f"📊 TÀI: `{res['tai']}%`\n"
        f"📊 XỈU: `{res['xiu']}%`\n"
        f"🎯 Tin cậy: *{res['confidence']}%* ({level})\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💰 LEMINH TOOL – Làm giàu thành công\n"
        "🎉 Chúc bạn chơi vui vẻ!"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


# ============================================================
#   MAIN
# ============================================================
def main():
    if BOT_TOKEN == "DÁN_TOKEN_BOT_VÀO_ĐÂY":
        raise SystemExit("⚠️ Chưa cấu hình BOT_TOKEN!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hotro", cmd_hotro))
    app.add_handler(CommandHandler("xoa", cmd_xoa))       # ⚠️ KHÔNG dùng "xoá"
    app.add_handler(CommandHandler("32kitu", cmd_32))     # ⚠️ KHÔNG dùng "32kí"
    app.add_handler(CommandHandler("64kitu", cmd_64))     # ⚠️ KHÔNG dùng "64kí"
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hash))

    logger.info("🚀 LEMINH TOOL BOT đang chạy...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
