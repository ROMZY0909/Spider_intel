from flask import Flask, request
import telegram
import os
from dotenv import load_dotenv
from app.scanner.email_scanner import scan_email
from app.pdf.generator import generate_pdf

# Charger les variables d'environnement
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Initialiser Flask
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text.startswith("/start"):
        bot.send_message(
            chat_id=chat_id,
            text="🕷️ *Bienvenue sur SPIDER INTEL*\n\nEnvoyez `/scan email@example.com` pour lancer une analyse OSINT.",
            parse_mode=telegram.ParseMode.MARKDOWN
        )

    elif text.startswith("/scan"):
        try:
            target = text.split(" ")[1]
            bot.send_message(chat_id=chat_id, text=f"🔍 Analyse en cours pour : `{target}`...", parse_mode="Markdown")

            # Analyse
            result = scan_email(target)

            # Format du message
            msg = f"*Résumé :*\n{result.summary}\n\n*Sources :*\n"
            for source in result.sources:
                msg += f"\n🔹 *{source.source}*:\n"
                for d in source.data:
                    msg += f"  - {d}\n"

            bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

            # Génération du PDF et envoi
            filename = f"rapport_{target}.pdf"
            generate_pdf(result.dict(), output_path=filename)
            with open(filename, "rb") as f:
                bot.send_document(chat_id=chat_id, document=f, filename=filename)

        except IndexError:
            bot.send_message(chat_id=chat_id, text="❌ Utilisation : `/scan email@example.com`", parse_mode="Markdown")

    elif text.startswith("/getreport"):
        bot.send_message(chat_id=chat_id, text="📄 La commande /getreport sera bientôt active.")

    return "ok", 200

# Lancer Flask si fichier exécuté directement (utile pour Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
