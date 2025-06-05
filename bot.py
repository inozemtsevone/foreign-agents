import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from docx import Document

TOKEN = os.getenv('BOT_TOKEN')
print("TOKEN =", TOKEN)  # временно для отладки

INOAGENTS = ["Иван Иванов", "Мария Петрова", "Алексей Смирнов"]

def strike(text):
    return ''.join(c + '\u0336' for c in text)

def replace_names(doc_path, output_path):
    doc = Document(doc_path)
    for p in doc.paragraphs:
        for name in INOAGENTS:
            if name in p.text:
                p.text = p.text.replace(name, strike(name))
    doc.save(output_path)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Пришли мне .docx-документ — я зачеркну имена иноагентов.")

def handle_doc(update: Update, context: CallbackContext):
    file = update.message.document.get_file()
    file.download("input.docx")
    replace_names("input.docx", "output.docx")
    update.message.reply_document(document=open("output.docx", "rb"))
    os.remove("input.docx")
    os.remove("output.docx")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document.mime_type("application/vnd.openxmlformats-officedocument.wordprocessingml.document"), handle_doc))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
