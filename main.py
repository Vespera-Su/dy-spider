from dotenv import load_dotenv
import os
load_dotenv()
os.environ.pop('SSLKEYLOGFILE', None)
import requests
import json
import src.cpilt as cpilt
import src.tool as tool
from src.download import Downloader
import threading

class spider:
    def __init__(self, config):
        try:
            config = json.load(open("./config.json", encoding="utf-8", mode="r"))
            self.cookies = config["cookies"]
            self.save_path = config["save_path"]
            self.start_timestamp = config["start_timestamp"]
            self.step_hours = config["step_hours"]
            self.count_page = config["count_page"]
            self.lock_path = r"./data/lock.json"
            self.redownload = config["redownload"]
            self.lock = json.load(open(self.lock_path, encoding="utf-8", mode="r")) if os.path.exists(self.lock_path) else os.makedirs(os.path.dirname(self.lock_path), exist_ok=True) or {}
        
            m = tool.generate_timestamps(start_timestamp=self.start_timestamp, step_hours=self.step_hours, count=self.count_page)
            self.data_list = []
            print(f"生成的时间戳列表: {m}")
            print("正在初始化数据页...")
            for i in range(self.count_page):
                if i == 0:
                    self.data_list.append(self.get_params(max_cursor=0,min_cursor=m[0]))
                    continue
                self.data_list.append(self.get_params(max_cursor=m[i-1],min_cursor=m[i]))
            if not self.redownload:
                # 过滤已下载的项目：保留未在lock中或lock值为False的项
                self.data_list = [
                    [item for item in page if not self.lock.get(item.get("aweme_id"), False)]
                    for page in self.data_list
                ]
            print(f"过滤后数据页数: {len(self.data_list)}, 各页项数: {[len(page) for page in self.data_list]}")
            print("数据页初始化完成！")
        except Exception as e:
            print(f"请先补全配置文件: {self.cookies}，错误详情: {e}")
            exit(1)

    def get_params(self, max_cursor:str = 0, min_cursor:str = 0):
            cookies = {
                'bd_ticket_guard_client_web_domain': '2',
                'enter_pc_once': '1',
                'UIFID_TEMP': '29a1f63ec682dc0a0df227dd163e2b46e3a6390e403335fa4c2c6d1dc0ec5ffa1824585df90bc0bf098c74b7e51b5a0217703ccfff41d3091f75cedffabfd5aaacccf21442a5e64a8fcbb2f3ca97825cdb419e6ed234fcb751ef7291355242f458be6c6612ad3d0b273efb23c6a83547',
                'hevc_supported': 'true',
                'UIFID': '29a1f63ec682dc0a0df227dd163e2b46e3a6390e403335fa4c2c6d1dc0ec5ffa8e62aa317e2d99b2dda1d7c8feaa36b14086b74f09810650663230f04379486919d44330efdbcb86bf5cb7246440892966c9fd4e9fc406b748b567e55b03fd48cd37613bb93ca3ac88d7bf41592388f3e73a4c967a0490149d04fc9e4180253d2b894aa0008ce1f7ee97d2fd1496349d37cddf9728f1433aeda13c7c30c2374ea2ed760bf8da729f6066091156759d7e474ba8276f02267f6b68e91afe9f7625',
                'n_mh': 'zCC6yXAdU9_bG76UwqWdxY3m6zV98keT2xrdhxI1l2k',
                'enter_pc_first_on_day': '20251206',
                'my_rd': '2',
                'SEARCH_RESULT_LIST_TYPE': '%22single%22',
                'PhoneResumeUidCacheV1': '%7B%22111225245452%22%3A%7B%22time%22%3A1766899306398%2C%22noClick%22%3A0%7D%7D',
                'volume_info': '%7B%22isMute%22%3Afalse%2C%22isUserMute%22%3Afalse%2C%22volume%22%3A0.5%7D',
                'passport_csrf_token': 'dc1d88fd3cd48a8c799fca9e5e6503a2',
                'passport_csrf_token_default': 'dc1d88fd3cd48a8c799fca9e5e6503a2',
                'is_staff_user': 'false',
                'strategyABtestKey': '%221772905652.809%22',
                'is_dash_user': '1',
                'ttwid': self.cookies["ttwid"],
                'passporst_assist_user': 'Cj1s8ZaZYjL4zy4y2S6s6E2kMZ5uZj9crk2UMUDs8Dw5w9UGgM7Ap3JYUIwJN_aGrX7AHOQQj8ZzwADK-xD7GkoKPAAAAAAAAAAAAABQJ_YMpjENL5Yz2B3FqC7I8rIfK8hAOLWiJW_WZRmD0r0j9eGVe1f15WICn-F0r5G68BCEvYsOGImv1lQgASIBAwwHNA4%3D',
                'sid_guard': self.cookies["sid_guard"],
                'uid_tt': 'ef77311c993c9ab54457d6ea63b2acea',
                'uid_tt_ss': 'ef77311c993c9ab54457d6ea63b2acea',
                'sid_tt': 'd0557cab2625a65136e3daf7c4bc4f25',
                'sessionid': 'd0557cab2625a65136e3daf7c4bc4f25',
                'sessionid_ss': 'd0557cab2625a65136e3daf7c4bc4f25',
                'session_tlb_tag': 'sttt%7C4%7C0FV8qyYlplE249r3xLxPJf________-z4ZtXzhDHK3oq99mLT9-BQATf8QTeAk7-ynolGU5zaec%3D',
                'sid_ucp_v1': '1.0.0-KGQ3N2Y2NzgxYzI5YTcyMjk5MzA4MTRmYWRmYjRiZWYyNGUxOWI0M2QKHwiMnqqsngMQz8mxzQYY7zEgDDD8y-biBTgHQPQHSAQaAmxxIiBkMDU1N2NhYjI2MjVhNjUxMzZlM2RhZjdjNGJjNGYyNQ',
                'ssid_ucp_v1': '1.0.0-KGQ3N2Y2NzgxYzI5YTcyMjk5MzA4MTRmYWRmYjRiZWYyNGUxOWI0M2QKHwiMnqqsngMQz8mxzQYY7zEgDDD8y-biBTgHQPQHSAQaAmxxIiBkMDU1N2NhYjI2MjVhNjUxMzZlM2RhZjdjNGJjNGYyNQ',
                '_bd_ticket_crypt_cookie': 'ec62179870c3495e87cebbcf24a419fc',
                '__security_mc_1_s_sdk_sign_data_key_web_protect': '648ea257-4d2a-a54b',
                '__security_mc_1_s_sdk_cert_key': '83c92002-4903-949f',
                '__security_mc_1_s_sdk_crypt_sdk': '135a188f-48d5-a281',
                '__security_server_data_status': '1',
                'login_time': '1772905679927',
                'publish_badge_show_info': '%220%2C0%2C0%2C1772905680312%22',
                'DiscoverFeedExposedAd': '%7B%7D',
                'biz_trace_id': '839b2f00',
                'odin_tt': 'c67891480cb9a2eb648767e6fab34482e3ccd6a7a7b51204f42db4fabd8d03ea45976f496027aa8f4bfb03850cdee74d1224629e5282bd447cf475f6ca7faf54',
                'SelfTabRedDotControl': '%5B%7B%22id%22%3A%227315707654188304399%22%2C%22u%22%3A86%2C%22c%22%3A86%7D%2C%7B%22id%22%3A%227547968399289927720%22%2C%22u%22%3A75%2C%22c%22%3A75%7D%5D',
                'IsDouyinActive': 'true',
                'stream_recommend_feed_params': '%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A960%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A20%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22',
                'FOLLOW_LIVE_POINT_INFO': '%22MS4wLjABAAAASK-dh93CTln2R7NDctNK1TTpNraSMoCRqSX4kuEna_Y%2F1772985600000%2F0%2F0%2F1772906753405%22',
                'FOLLOW_NUMBER_YELLOW_POINT_INFO': '%22MS4wLjABAAAASK-dh93CTln2R7NDctNK1TTpNraSMoCRqSX4kuEna_Y%2F1772985600000%2F0%2F1772906153405%2F0%22',
                'home_can_add_dy_2_desktop': '%221%22',
                'bd_ticket_guard_client_data': 'eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTk9xMzFqWHl6K2h0dHZsMkZNZTBDMmFGamtaenhTQndZWCtyTXVyMUhRRHc1cnhGNTNYanU4NUdEYTEwaEhxTXVDUVFpc01UVXN0NndYSmV3K3psaFU9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D',
                'bd_ticket_guard_client_data_v2': 'eyJyZWVfcHVibGljX2tleSI6IkJOT3EzMWpYeXoraHR0dmwyRk1lMEMyYUZqa1p6eFNCd1lYK3JNdXIxSFFEdzVyeEY1M1hqdTg1R0RhMTBoSHFNdUNRUWlzTVRVc3Q2d1hKZXcremxoVT0iLCJ0c19zaWduIjoidHMuMi5hNTJkYWQ0ZGEzMDJkYWJkZjAxZTk0ZmYyYWM5YTA0ZTViOGM2Njg3NmFlZGYwNzEyOGQzYjNhNGE1NzliNzVkYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiIrYzRlYk8vYW50UEJCalZJdkFGdkNNVmpjN3ZncXlmZ0NmN3JObE14QmRBPSIsInNlY190cyI6IiNGTWRZdE1QYzR4YWRCM1IweVhRMTlSQmVqVk9zaVl5RzZtV1BIQjZZQzNNOVNaczhaQ0Vxb05vcTI1OUMifQ%3D%3D',
            }

            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'bd-ticket-guard-client-data': 'eyJ0c19zaWduIjoidHMuMi5hNTJkYWQ0ZGEzMDJkYWJkZjAxZTk0ZmYyYWM5YTA0ZTViOGM2Njg3NmFlZGYwNzEyOGQzYjNhNGE1NzliNzVkYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50IjoidGlja2V0LHBhdGgsdGltZXN0YW1wIiwicmVxX3NpZ24iOiIvcVFNdkZTLzBvRGRHUGlvMnBUVHpSMU9lVDEwRzdXcjUyUXFiMWQ4clc4PSIsInRpbWVzdGFtcCI6MTc3MjkwNjE1NH0=',
                'bd-ticket-guard-ree-public-key': 'BNOq31jXyz+httvl2FMe0C2aFjkZzxSBwYX+rMur1HQDw5rxF53Xju85GDa10hHqMuCQQisMTUst6wXJew+zlhU=',
                'bd-ticket-guard-version': '2',
                'bd-ticket-guard-web-sign-type': '1',
                'bd-ticket-guard-web-version': '2',
                'cache-control': 'no-cache',
                'origin': 'https://www.douyin.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://www.douyin.com/',
                'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'uifid': '29a1f63ec682dc0a0df227dd163e2b46e3a6390e403335fa4c2c6d1dc0ec5ffa8e62aa317e2d99b2dda1d7c8feaa36b14086b74f09810650663230f04379486919d44330efdbcb86bf5cb7246440892966c9fd4e9fc406b748b567e55b03fd48cd37613bb93ca3ac88d7bf41592388f3e73a4c967a0490149d04fc9e4180253d2b894aa0008ce1f7ee97d2fd1496349d37cddf9728f1433aeda13c7c30c2374ea2ed760bf8da729f6066091156759d7e474ba8276f02267f6b68e91afe9f7625',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
                'cookie': self.cookies["cookie"],
            }

            params = {
                'device_platform': 'webapp',
                'aid': '6383',
                'sec_user_id': 'MS4wLjABAAAASK-dh93CTln2R7NDctNK1TTpNraSMoCRqSX4kuEna_Y',
                'max_cursor': max_cursor,
                'min_cursor': min_cursor,
            }
            response = requests.get('https://www-hj.douyin.com/aweme/v1/web/aweme/favorite/', params=params, cookies=cookies, headers=headers)
            with open("./logs/date.txt", mode="w", encoding="utf-8") as f:
                f.write(response.text)
            t = cpilt.load_cpilt_data(response.json())
            return t
    
    def start_download(self):
        threads = []
        tap = 1
        downs = Downloader(save_path=self.save_path)
        download_results = {}

        def thread_worker(page_data, page_index):
            # 这里调用下载逻辑并收集返回值
            lock_result = downs.download_cpilt_data(page_data)
            download_results.update(lock_result)

        for j in self.data_list:
            if not j:
                print(f"第{tap}页数据为空，跳过下载...")
                tap += 1
                continue
            print(f"第{tap}页数据不为空，开始下载...")
            t = threading.Thread(target=thread_worker, args=(j, tap))
            threads.append(t)
            tap += 1
        
        # 启动所有下载线程
        for t in threads:
            t.start()
        # 等待所有下载线程完成
        for t in threads:
            t.join()

        self.download_results = download_results
        print("所有下载线程已完成")
        self.update_lock()

    def update_data(self):
        with open("./data/list.json", mode="w", encoding="utf-8") as f:
            json.dump(self.data_list, f, ensure_ascii=False, indent=4)
            print("数据更新完成！")

    def export_data(self):
        return self.data_list
    
    def update_lock(self):
        lock_data = {}
        if os.path.exists(self.lock_path):
            with open(self.lock_path, "r", encoding="utf-8") as f:
                lock_data = json.load(f)
        lock_data.update(self.download_results)
        with open(self.lock_path, "w", encoding="utf-8") as f:
            json.dump(lock_data, f, ensure_ascii=False, indent=4)
    
if __name__ == '__main__':
    #读取配置文件
    config = json.loads(open("./config.json", encoding="utf-8", mode="r").read())
    #初始化爬虫实例
    sp = spider(config = config)
    #存储数据
    sp.update_data()
    #开始爬虫并拿到每页下载结果
    sp.start_download()

    
    
        