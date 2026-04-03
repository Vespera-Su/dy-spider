import json

def print_cpilt_info(level_one_path,is_print:bool=True):
        i = level_one_path
        card = {}
        author = i["author"]["nickname"]
        aweme_id = i["aweme_id"]
        desc = i["desc"]
        if i["images"] is None:
            is_video = True
            resolution = i["video"]["bit_rate"][0]["play_addr"]["width"]
            video_url = i["video"]["bit_rate"][0]["play_addr"]["url_list"][2]
            for j in i["video"]["bit_rate"]:
                if j["play_addr"]["width"] > resolution:
                    resolution = j["play_addr"]["width"]
                    video_url = j["play_addr"]["url_list"][2]
            card = {
                "author":author,
                "aweme_id":aweme_id,
                "desc":desc,
                "is_video":is_video,
                "resolution":resolution,
                "url":video_url
            }
            if is_print:
                print(f" Author: {author},\n Aweme ID: {aweme_id},\n Description: {desc},\n Resolution: {resolution},\n Video URL: {video_url},\n")
        else:
            is_video = False
            resolution_list = []
            image_url_list = []
            for j in i["images"]:
                resolution = j["width"]
                image_url = j["url_list"][0]
                resolution_list.append(resolution)
                image_url_list.append(image_url)
            card = {
                "author":author,
                "aweme_id":aweme_id,
                "desc":desc,
                "is_video":is_video,
                "resolutions":resolution_list,
                "url":image_url_list
            }
            if is_print:
                print(f" Author: {author},\n Aweme ID: {aweme_id},\n Description: {desc},\n Resolution: {resolution},\n Image URL: {image_url_list},\n")
        return card

def load_cpilt_data(file_path):
    datas = []
    level_two_path = file_path["aweme_list"]
    for i in level_two_path:
        datas.append(print_cpilt_info(i,is_print=False))
    return datas


if __name__ == "__main__":
    with open("./data/date.json", mode="r", encoding="utf-8") as fr:
        data = json.load(fr)
        print(load_cpilt_data(data))
