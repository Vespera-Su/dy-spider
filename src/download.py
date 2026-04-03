from dotenv import load_dotenv
load_dotenv()
import requests
import os
import re
from src.tool import now_timestamp

class Downloader:
    def __init__(self,save_path=None):
        self.save_path = save_path
        if self.save_path is None:
            save_dir = "./downloads"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            self.save_path = os.path.abspath(save_dir)
        else:
            self.save_path = os.path.abspath(self.save_path)
        if os.path.exists(self.save_path) is False:
            os.mkdir(self.save_path)
            print(f"文件夹{self.save_path}已创建")
        print(f"文件夹存在性:{os.path.exists(self.save_path)}")

    def clean_windows_filename(self, filename, replace_char="_"):
        # 移除非法字符
        illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'
        cleaned = re.sub(illegal_chars, replace_char, filename)
        
        # 移除Windows保留文件名（可选）
        windows_reserved = [
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
        ]
        
        # 检查是否为保留文件名
        base_name = cleaned.rsplit('.', 1)[0] if '.' in cleaned else cleaned
        if base_name.upper() in windows_reserved:
            cleaned = f"_{cleaned}"
        
        # 移除开头和结尾的点及空格（Windows不允许）
        cleaned = cleaned.strip('. ')
        
        # 限制长度（Windows路径最长260字符，文件名最长255字符）
        if len(cleaned) > 255:
            cleaned = cleaned[:255]
        
        return cleaned

    def download_cpilt_data(self, cpilt_data):
        lock = {}
        for u in cpilt_data:
            try:
                author = self.clean_windows_filename(u["author"])
                if u["is_video"]:
                    video_response = requests.get(u["url"])
                    file_name = f"{author} {u['aweme_id']}.mp4"
                    with open(os.path.join(self.save_path, file_name), mode="wb") as fv:
                        fv.write(video_response.content)
                        print(f"{now_timestamp()} Downloaded video: {author} {u['aweme_id']}.mp4")
                else:
                    for i in u["url"]:
                        image_response = requests.get(i)
                        file_name = f"{author} {u['aweme_id']} {u['url'].index(i)}.webp"
                        with open(os.path.join(self.save_path, file_name), mode="wb") as fi:
                            fi.write(image_response.content)
                            print(f"{now_timestamp()} Downloaded image: {author} {u['aweme_id']} {u['url'].index(i)}.webp")
                lock.update({u['aweme_id']:True})
            except Exception as e:
                # print(f"{e}")
                print(f"{now_timestamp()} Download failed: {author} {u['aweme_id']}")
                lock.update({u['aweme_id']:False})      
                continue
        return lock