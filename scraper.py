from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common import by
import time
from pytube import YouTube
import moviepy.editor as mp
import os
from selenium.webdriver.chrome.options import Options
import pygame
from tkinter import messagebox

chrome_options = Options()
chrome_options.add_argument("--headless")


base_working_dir = "E:\\musicScraper\\"

if not os.path.isdir(f"{base_working_dir}\\musics"):
    os.mkdir(f"{base_working_dir}\\musics")
if not os.path.isdir(f"{base_working_dir}\\videos"):
    os.mkdir(f"{base_working_dir}\\videos")


def search_youtube(query):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + query)
    time.sleep(3)
    video_elements = driver.find_elements(by.By.ID, "dismissible")
    url_link = (
        video_elements[0]
        .find_element(by.By.TAG_NAME, "ytd-thumbnail")
        .find_element(by.By.TAG_NAME, "a")
    )
    print("[URL SUCCESSFULLY FOUND]")

    file_name = (
        video_elements[0]
        .find_element(by.By.CLASS_NAME, "text-wrapper")
        .find_element(by.By.ID, "meta")
        .find_element(by.By.ID, "title-wrapper")
        .find_element(by.By.TAG_NAME, "h3")
        .find_element(by.By.TAG_NAME, "a")
        .get_attribute("title")
    )

    print("[DOWNLOADING VIDEO]")
    YoutubeAudioDownload(query, url_link.get_attribute("href"), file_name)


def YoutubeAudioDownload(query, video_url, file_name):
    video = YouTube(video_url)
    file_name = file_name.split("|")[0]
    video.streams.first().download(
        filename=f"{file_name}.mp4", output_path=f"{base_working_dir}videos\\"
    )
    print("[AUDIO DOWNLOADED SUCCESSFULLY]")
    print("[CONVERTING TO MP3]")
    # convert_video_to_audio(file_name)
    print("[PLAYING AUDIO]")
    play_audio(query, file_name)


def play_audio(query, file_name):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(f"{base_working_dir}musics\\{file_name}.mp3")
    pygame.mixer.music.play()
    time.sleep(15)
    pygame.quit()
    answer = messagebox.askyesno("Play Again", "Is music correct ?")
    if answer:
        convert_video_to_audio(file_name)
    else:
        search_youtube(query)


def convert_video_to_audio(file_name):
    clip = mp.VideoFileClip(f"{base_working_dir}videos\\{file_name}.mp4")
    clip.audio.write_audiofile(f"{base_working_dir}musics\\{file_name}.mp3")
    print("[CONVERTED SUCCESSFULLY]")


with open(f"{base_working_dir}music_names.txt", "r") as file:
    music_names = file.read()
music_names = music_names.split("\n")
for music in music_names:
    search_youtube(music)
