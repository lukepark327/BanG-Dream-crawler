from requests import get
import requests
import eyed3
import os
import random
from time import sleep


def download(url, file_name):
    with open(file_name, "wb") as file:  # open in binary mode
        response = get(url)  # get request
        content = response.content
        file.write(content)  # write to file

    # if not decide(file_name):
    #     os.remove(file_name)


def decide(file_name):
    audiofile = eyed3.load(file_name)
    try:
        audiofile.tag
        return True
    except AttributeError:
        return False


def set_tag(file_name, image):
    audiofile = eyed3.load(file_name)

    with open(image, "rb") as file:  # open in binary mode
        audiofile.initTag()
        audiofile.tag.images.set(
            type_=3,
            img_data=file.read(),
            mime_type="image/png")
        audiofile.tag.save()


if __name__ == "__main__":
    ROOT_1 = "https://bestdori.com/assets/en/sound/"
    # https://bestdori.com/assets/jp/sound/bgm194_rip/bgm194.mp3
    # https://bestdori.com/assets/jp/sound/bgm001_rip/bgm001.mp3
    # https://bestdori.com/assets/en/sound/bgm1001_rip/bgm1001.mp3
    # et al.
    ROOT_2 = "https://bestdori.com/info/songs/"

    # 1~1001
    for id in range(1, 1002):
        PATH_2 = ROOT_2 + str(id)
        req = requests.get(PATH_2)
        html = req.text

        # Get title
        target = 'title content='
        idx_start = html.find(target)
        idx_end = html[idx_start:].find('>')
        title = html[idx_start + len(target):idx_start + idx_end]

        # Save MP3
        if title == "Bestdori!":
            print(id, ">>> !SKIP")
            continue
        else:
            PATH_1 = ROOT_1 + "bgm" + "%03d" % id + "_rip/bgm" + "%03d" % id + ".mp3"

            title = title[1:-1]
            download(PATH_1, "./songs/" + title + ".mp3")

        # Get art
        target = 'image content='
        idx_start = html.find(target)
        idx_end = html[idx_start:].find('>')
        image = html[idx_start + len(target):idx_start + idx_end]
        image = image[1:-1]
        download(image, "./images/" + title + ".png")

        set_tag(
            "./songs/" + title + ".mp3",
            "./images/" + title + ".png")

        print(id, ">>>", title)

        sleep(random.random())
