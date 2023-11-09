#! /bin/env python3

import argparse
import json
import os
import re
from functools import partial
from pathlib import Path
from typing import List, Optional

import cv2 as cv

Color = List[int]

ImageArray = List[List[Color]]

class URL(str):
    def __init__(self, s: str):
        super().__init__()
        self.s = s
        regex = re.compile(
                r'^(?:http)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(regex, s) is None:
            raise ValueError("Not a valid url")
        
    def __str__(self):
        return self.s


def get_frame_from_video(video_path: Path, frame_number) -> Optional[ImageArray]:
    vidcap = cv.VideoCapture(str(video_path))
    if vidcap.isOpened():
        vidcap.set(cv.CAP_PROP_POS_FRAMES, frame_number)
        _, image = vidcap.retrieve()
        vidcap.release()
        if _:
            return image
    return

def save_image(format: str, image: ImageArray, filename: Path) -> bool:
    _, encoded_image = cv.imencode(format, image)
    if _:
        return encoded_image.tofile(str(filename))
    else:
        return False 


def main(input_dir: Path, output_dir: Path, url: URL):
    if not (input_dir.is_dir() and output_dir.is_dir()):
        print("路径不是一个目录")
        exit(1)
        
    # glob returned an generator object only can be used once, so
    # need turn to list 

    # videos [Path("xxx/x.mp4"), Path("xxx/y.mp4"), ......]
    videos = list(input_dir.glob("*.mp4"))

    # map object only can be used once and then will be destroyed
    # generator object too. But we only use once so needn't turn 
    # to list
    covers = list(map(
        # fix function with 1. Get the first frame.
        lambda x: get_frame_from_video(x, 1),
        videos
    ))

    # print(videos)


    # ids [(0, Path(xxx/0.mp4)), (1, Path(xxx/1.mp4)), .....]
    ids = list(map(lambda x: (x[0], input_dir / (str(x[0]) + "." + str(x[1]).split(".")[-1])), enumerate(videos)))


    list(map(lambda x, y: os.rename(x, y[1]), videos, ids))

    covers_filename = list(map(
        # xxx/x.mp4 to xxx/x.jpg
        lambda x: output_dir / (str(x[0]) + '.jpg'),
        ids
    ))   # all covers filename

    

    list(map(partial(save_image, '.jpg'), covers, covers_filename))

    json_content = list(map(
        lambda x: {"video_id": x, "videoDownloadUrl": url+str(x)+".mp4", "coverImgUrl": url+str(x)+".jpg"},
        [x[0] for x in ids]
    ))

    with open(Path(".") / "mapping.json", "w") as json_file:
        json.dump(json_content, json_file, indent=2)

    # with open(Path(".") / "map.csv", 'w', encoding="utf-8") as f:
    #     f.write("\n".join(map(
    #         lambda a: "; ".join(a),
    #         map(lambda x, y: [str(x), str(y)], videos, covers_filename)
    #     )))

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path, help="input video directory")
    parser.add_argument("output_dir", type=Path, help="output cover directory")
    parser.add_argument("url", type=URL, help="url in json")
    argv = parser.parse_args()
    main(**argv.__dict__)
