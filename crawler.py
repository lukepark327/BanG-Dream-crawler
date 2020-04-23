from requests import get
import requests
import eyed3
import os
import random
from time import sleep

import arguments


def download(url, file_name, test=False):
    with open(file_name, "wb") as file:  # open in binary mode
        response = get(url)  # get request
        content = response.content
        file.write(content)  # write to file

    if test and not is_mp3(file_name):
        # os.remove(file_name)
        raise TypeError


def is_mp3(file_name):
    audiofile = eyed3.load(file_name)
    try:
        audiofile.tag
        return True
    except AttributeError:
        return False


def set_tag(file_name, image):
    try:
        audiofile = eyed3.load(file_name)

        with open(image, "rb") as file:  # open in binary mode
            audiofile.initTag()
            audiofile.tag.images.set(
                type_=3,
                img_data=file.read(),
                mime_type="image/png")
            audiofile.tag.save()
    except AttributeError:
        print("!NO SONG")


if __name__ == "__main__":
    # Initialization
    if not os.path.isdir("./songs/"):
        os.mkdir("./songs/")
    if not os.path.isdir("./images/"):
        os.mkdir("./images/")

    args = arguments.parser()
    start_num = args.start
    end_num = args.end
    print("Download songs: from", start_num, "to", end_num)

    # Example of each song's download links:
    # https://bestdori.com/assets/jp/sound/bgm194_rip/bgm194.mp3
    # https://bestdori.com/assets/jp/sound/bgm001_rip/bgm001.mp3
    # https://bestdori.com/assets/en/sound/bgm1001_rip/bgm1001.mp3
    # We only consider the below conturies: jp, en, tw.
    ROOT_1_1 = "https://bestdori.com/assets/"
    ROOT_1_2_jp = "jp"
    ROOT_1_2_en = "en"
    ROOT_1_2_tw = "tw"
    ROOT_1_3 = "/sound/"
    ROOT_2 = "https://bestdori.com/info/songs/"

    # Set range of songs' ID.
    # For example, ID of "God knows..." is 7.
    # https://bestdori.com/info/songs/7/God-knows
    for id in range(start_num, end_num + 1):
        PATH_2 = ROOT_2 + str(id)
        req = requests.get(PATH_2)
        req.encoding = req.apparent_encoding
        html = req.text

        # Get title.
        target = 'title content='
        idx_start = html.find(target)
        idx_end = html[idx_start:].find('>')
        title = html[idx_start + len(target):idx_start + idx_end]

        # Save MP3.
        if title == "Bestdori!":
            print(id, ">>> !SKIP")
            continue
        else:
            title = title[1:-1]  # remove quotes marks
            title = title.replace("/", "-")  # prevent wrong file name

            for ROOT_1_2 in [ROOT_1_2_jp, ROOT_1_2_en, ROOT_1_2_tw]:
                try:
                    PATH_1 = ROOT_1_1 + ROOT_1_2 + ROOT_1_3 + "bgm" + "%03d" % id + "_rip/bgm" + "%03d" % id + ".mp3"
                    download(PATH_1, "./songs/" + title + ".mp3", test=True)
                    break
                except TypeError:
                    # os.remove("./songs/" + title + ".mp3")
                    pass

        # Save album art.
        target = 'image content='
        idx_start = html.find(target)
        idx_end = html[idx_start:].find('>')
        image = html[idx_start + len(target):idx_start + idx_end]
        image = image[1:-1]
        download(image, "./images/" + title + ".png")

        # Set tag.
        set_tag(
            "./songs/" + title + ".mp3",
            "./images/" + title + ".png")

        print(id, ">>>", title)

        sleep(random.random())
