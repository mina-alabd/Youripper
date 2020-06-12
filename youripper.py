from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import MessageEntity
from chataction import send_typing_action,send_upload_action
from pytube import YouTube
from moviepy.editor import *
import time,os


@send_typing_action
def start(update, context):
    update.message.reply_text('Hi! My name is YouRipper')
    update.message.reply_text('I Can download videos for you')
    update.message.reply_text('And convert them to mp3')
    update.message.reply_text('Send me a youtube link and see my magic!!')


def download_url(update, context):

    url=update.message.text
    print(url)
    try:
        send = YouTube(url)
        m = update.message.reply_text("got the link")
        downloading(update, context, send,m)
    except Exception:
        update.message.reply_text("Please send youtube Link")


def downloading(update, context, send,m):
    try:
        m.edit_text("Downloading..")
        video = send.streams.get_audio_only().download(skip_existing=True)
        title = send.streams.get_audio_only().default_filename
        title = title.replace(".mp4", ".mp3")
        mp3conversion(update, context, title,video,m)

    except Exception:
        update.message.reply_text("Download Error")

def mp3conversion(update,context,title,video,m):
    try:
        m.edit_text('Download Successful')
        m.edit_text('Converting to mp3')
        mp3 = AudioFileClip(video)
        mp3.write_audiofile(title)
        os.remove(video)
        m.edit_text('Yay! it got converted')
        sending_mp3(update,context,title,m)
    except Exception:
        update.message.reply_text("Audio Conversion Error")

@send_upload_action
def sending_mp3(update,context,title,m):
    try:
        m.edit_text('Sending mp3 to you .. Please Wait')
        context.bot.send_audio(chat_id=update.effective_message.chat_id, audio=open(title, "rb"), timeout=50)
        m.delete()
        k=update.message.reply_text("You got the mp3...!!")
        time.sleep(1)
        k.edit_text("Hope I am fast")
        time.sleep(1)
        k.edit_text("Its all because of my Master Syed")
        time.sleep(1)
        k.edit_text("Send Me another youtube link and see my magic ..")
        time.sleep(1)
        k.edit_text("Until then bye.... !!")
        time.sleep(1)
        k.delete()


    except Exception:
        update.message.reply_text("Upload Error")

def main():

    updater = Updater("1107009022:AAHkOzKjK4pDf9D7i-C8-PH5x1NI-61iVe8",use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(MessageHandler(Filters.entity(MessageEntity.URL), download_url))

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
        main()
