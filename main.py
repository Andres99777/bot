import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    ChatJoinRequestHandler,
    filters
)

# =======================
# CONFIGURACIÓN
# =======================

TOKEN = "8278289735:AAFWAJRrwNXTcZF-5l3Q4sqkMDhpw-MO2rg"
ADMIN_URL = "https://t.me/KykePicks"
ARCHIVO = "users.json"

RECORDATORIO_1 = 3600      # 1 hora
RECORDATORIO_2 = 86400     # 24 horas

# =======================
# UTILIDADES
# =======================

def cargar_datos():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return {"joined": [], "contacted": []}

def guardar_datos(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=4)

# =======================
# RECORDATORIOS
# =======================

async def recordatorio_1(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data
    data = cargar_datos()

    if user_id in data["contacted"]:
        return

    texto = (
        "👋 <b>¿Sigues ahí?</b>\n\n"
        "Si quieres información personalizada, escríbeme 👇"
    )

    await context.bot.send_message(
        chat_id=user_id,
        text=texto,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Hablar con Kyke", url=ADMIN_URL)]
        ])
    )

async def recordatorio_2(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data
    data = cargar_datos()

    if user_id in data["contacted"]:
        return

    texto = (
        "⏰ <b>Último recordatorio</b>\n\n"
        "Estoy disponible para ayudarte 👇"
    )

    await context.bot.send_message(
        chat_id=user_id,
        text=texto,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Contactar ahora", url=ADMIN_URL)]
        ])
    )

# =======================
# APROBAR + BIENVENIDA
# =======================

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request = update.chat_join_request
    user_id = join_request.from_user.id

    await join_request.approve()

    data = cargar_datos()

    if user_id not in data["joined"]:
        data["joined"].append(user_id)
        guardar_datos(data)

        context.job_queue.run_once(recordatorio_1, when=RECORDATORIO_1, data=user_id)
        context.job_queue.run_once(recordatorio_2, when=RECORDATORIO_2, data=user_id)

    mensaje = (
        "👋 <b>Hola, ¿cómo estás?</b>\n\n"
        "Déjame darte la <b>bienvenida al mejor canal de apuestas deportivas</b> 🥇\n\n"
        "Mucho gusto, <b>soy Kyke</b>, analista deportivo con <b>7 años de experiencia</b> "
        "en apuestas y <b>5 años siendo consistentemente rentable</b> 🥳💰\n\n"
        "Mi trabajo es analizar todos los eventos deportivos con estrategias y herramientas "
        "de probabilidades para que <b>mi comunidad gane dinero extra todos los días</b> conmigo ✅🔥\n\n"
        "Si estás empezando y no sabes del tema, aquí vas a <b>aprender y ganar totalmente GRATIS</b>.\n\n"
        "Estás en el lugar correcto si quieres <b>resultados y no humo</b>.\n"
        "Déjate guiar por mí 🧠 y tendrás grandes resultados 🍾\n\n"
        "🤑 <b>POR OTRO LADO…</b>\n\n"
        "🎁 <b>¿LISTOS PARA EL RETO DE 400.000 MIL PESOS (150 USD) EN UNA SEMANA?</b>\n\n"
        "Este reto está disponible para cualquier país 🌍\n"
        "Es <b>totalmente GRATIS</b>.\n"
        "No tienes que saber de apuestas, yo te dejaré el <b>paso a paso para ganar</b> ✅\n\n"
        "🥳 Mantente súper pendiente al grupo donde estaré dejando toda la información.\n\n"
        "🎁 <b>Grupo gratuito:</b>\n"
        "<a href='https://t.me/+hgwy3ZBwOXFlODgx'>Unirme al grupo de apuestas</a>\n\n"
        "ℹ️ <b>Este es mi único contacto oficial.</b>\n"
        "Si tienes cualquier duda, pregúntame sin pena 😉 🔽\n\n"
        "📲 <a href='https://t.me/KykePicks'>Contactar a Kyke aquí</a>"
    )

    await context.bot.send_message(
        chat_id=user_id,
        text=mensaje,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Contactar a Kyke", url=ADMIN_URL)]
        ])
    )

# =======================
# DETECTAR MENSAJE
# =======================

async def detectar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = cargar_datos()

    if user_id not in data["contacted"]:
        data["contacted"].append(user_id)
        guardar_datos(data)

# =======================
# MAIN (BACKGROUND WORKER)
# =======================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(approve))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detectar_mensaje))

    print("🤖 Bot Kyke corriendo 24/7 como Background Worker")
    app.run_polling()

if __name__ == "__main__":
    main()











