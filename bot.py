# import os
# import telebot
# from pytube import YouTube
# from moviepy.editor import VideoFileClip

# bot = telebot.TeleBot('7144449198:AAHoMTB8azWfEo1WvbQ4A_EBF-2lO-TsNxQ')

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, "Welcome to yotubebot!")

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     try:
#         download_video(message)
#     except Exception as e:
#         bot.reply_to(message, f"An error occurred: {e}")

# def download_video(message):
#     try:
#         url = message.text
#         yt = YouTube(url)
#         video = yt.streams.get_highest_resolution()

#         if not os.path.exists('downloads'):
#             os.makedirs('downloads')

#         file_path = os.path.join('downloads', video.default_filename)
#         video.download(output_path='downloads')

#         convert_to_audio(file_path, yt.title, message)
#     except Exception as e:
#         bot.reply_to(message, f"An error occurred: {e}")

# def convert_to_audio(video_path, title, message):
#     try:
#         audio_path = os.path.join('downloads', f"{title}.mp3")
#         video_clip = VideoFileClip(video_path)
#         audio_clip = video_clip.audio
#         audio_clip.write_audiofile(audio_path)

#         with open(audio_path, 'rb') as audio_file:
#             bot.send_audio(message.chat.id, audio_file, timeout=500)  # Increase timeout value

#         bot.reply_to(message, f"Converted '{title}' video to audio successfully")
#     except TimeoutError:
#         bot.reply_to(message, "Sending audio timed out. Please try again later.")
#     except Exception as e:
#         bot.reply_to(message, f"An error occurred: {e}")

# bot.polling()
import os
import telebot
from yt_dlp import YoutubeDL
from moviepy.editor import *

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the API token you obtained from BotFather
TOKEN = '7144449198:AAHoMTB8azWfEo1WvbQ4A_EBF-2lO-TsNxQ'

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = (
        "Send me a YouTube link and I will convert it to MP3 for you!\n\n"
        "Just send me the link, and I'll handle the rest."
    )
    bot.reply_to(message, instructions)

@bot.message_handler(content_types=['text'])
def handle_youtube_link(message):
    try:
        youtube_link = message.text.strip()

        # Download the YouTube video
        with YoutubeDL() as ydl:
            info_dict = ydl.extract_info(youtube_link, download=True)
            video_title = info_dict.get('title', 'video')

        # Find the downloaded file with the highest resolution (in MP4 format)
        mp4_files = [f for f in os.listdir('.') if f.endswith('.mp4')]
        if not mp4_files:
            bot.reply_to(message, "Failed to download the video.")
            return

        mp4_files.sort(key=lambda f: os.path.getsize(f), reverse=True)
        downloaded_mp4 = mp4_files[0]

        # Convert the MP4 to MP3 using moviepy
        mp3_file = f'{video_title}.mp3'
        video_clip = VideoFileClip(downloaded_mp4)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(mp3_file)

        # Send the MP3 file to the user
        with open(mp3_file, 'rb') as f:
            bot.send_audio(message.chat.id, f)

        # Clean up downloaded files
        os.remove(downloaded_mp4)
        os.remove(mp3_file)

    except Exception as e:
        bot.reply_to(message, "An error occurred. Please try again later.")

if __name__ == '__main__':
    bot.polling()