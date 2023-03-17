import re, os
import json
import requests
import time, glob
from concurrent.futures import ThreadPoolExecutor
import csv
import random
import traceback


class BaiduStreetDownload():

    def __init__(self):
        self.root = r'.\dir'
        self.read_fn = r'all_wuhan_point.csv'
        self.error_fn = r'error_road_intersection.csv'
        self.dir = r'images'
        self.filenames_exist = glob.glob1(os.path.join(self.root, self.dir), "*.png")
        self.num = 200

        self.proxy_url = "https://proxy.qg.net/allocate?Key=青果代理%s"%(self.num)
        self.proxy_resp = requests.get(self.proxy_url).json()["Data"]
        self.proxyAddr_list = [self.proxy_resp[i]["host"] for i in range(len(self.proxy_resp))]

        self.session = requests.Session()
        self.session.proxies = random.choice(self.proxyAddr_list)

        # 读取 csv 文件
        self.data = self.read_csv(os.path.join(self.root, self.read_fn))
        # 记录 header
        self.header = self.data[0]
        # 去掉 header
        self.data = self.data[5000:]
        # 记录爬取失败的图片
        self.error_img = []
        # 记录没有svid的位置
        self.svid_none = []
        self.pitchs = '0'
        self.count = 1

    # read csv
    def write_csv(self, filepath, data, head=None):
        if head:
            data = [head] + data
        with open(filepath, mode='w', encoding='UTF-8-sig', newline='') as f:
            writer = csv.writer(f)
            for i in data:
                writer.writerow(i)

    # write csv
    def read_csv(self, filepath):
        data = []
        if os.path.exists(filepath):
            with open(filepath, mode='r', encoding='utf-8') as f:
                lines = csv.reader(f)  # #此处读取到的数据是将每行数据当做列表返回的
                for line in lines:
                    data.append(line)
            return data
        else:
            print('filepath is wrong：{}'.format(filepath))
            return []

    def grab_img_baidu(self, _url, _headers=None):
        if _headers == None:
            # 设置请求头 request header
            headers = {
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                "Referer": "https://map.baidu.com/",
                "sec-ch-ua-mobile": "?0",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
            }
        else:
            headers = _headers
        response = self.session.get(_url, headers=headers)

        if response.status_code == 200:# and response.headers.get('Content-Type') == 'image/jpeg':
            return response.content
        else:
            return None


    def openUrl(self, _url):
        # 设置请求头 request header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        response = self.session.get(_url, headers=headers)
        if response.status_code == 200:  # 如果状态码为200，寿命服务器已成功处理了请求，则继续处理数据
            return response.content
        else:
            return None


    def getPanoId(self, _lng, _lat):
        # 获取百度街景中的svid get svid of baidu streetview
        url = "https://mapsv0.bdimg.com/?&qt=qsdata&x=%s&y=%s&mode=day" % (
            str(_lng), str(_lat))
        
        response = self.openUrl(url).decode("utf8")
        # print(response)
        if (response == None):
            return None
        reg = r'"id":"(.+?)",'
        pat = re.compile(reg)
        try:
            svid = re.findall(pat, response)[0]
            return svid
        except:
            return None


    # 官方转换函数
    # 因为百度街景获取时采用的是经过二次加密的百度墨卡托投影bd09mc (Change wgs84 to baidu09)
    def wgs2bd09mc(self, wgs_x, wgs_y):
        # to:5是转为bd0911，6是转为百度墨卡托
        url = 'http://api.map.baidu.com/geoconv/v1/?coords={}+&from=1&to=6&output=json&ak={}'.format(
            wgs_x + ',' + wgs_y,
            'mYL7zDrHfcb0ziXBqhBOcqFefrbRUnuq'
        )
        res = self.openUrl(url).decode()
        temp = json.loads(res)
        bd09mc_x = 0
        bd09mc_y = 0
        if temp['status'] == 0:
            bd09mc_x = temp['result'][0]['x']
            bd09mc_y = temp['result'][0]['y']

        return bd09mc_x, bd09mc_y

    def downloadpic(self, i):
        self.count += 1
        print('Processing No. {} point...'.format(i + 1))
        # gcj_x, gcj_y, wgs_x, wgs_y = data[i][0], data[i][1], data[i][2], data[i][3]
        wgs_x, wgs_y = self.data[i][15], self.data[i][16]

        try:
            bd09mc_x, bd09mc_y = self.wgs2bd09mc(wgs_x, wgs_y)
        except Exception as e:
            print(str(e))  # 抛出异常的原因
            return None
        flag = True

        flag = flag and "%s_%s.png" % (wgs_x, wgs_y) in self.filenames_exist

        # If all four files exist, skip
        if (flag):
            return None
        svid = self.getPanoId(bd09mc_x, bd09mc_y)
        if svid is None:
            return None
        # for h in range(len(self.headings)):
        save_fn = os.path.join(self.root, self.dir) + r'\%s_%s.png' % (str(wgs_x).strip(), str(wgs_y).strip())

        url = 'https://mapsv0.bdimg.com/?qt=pdata&sid={}&pos=0_0&z=1'.format(
            svid #, self.headings[h]
        )
        img = self.grab_img_baidu(url)


        if img == None:
            # self.data[i].append(self.headings[h])
            self.error_img.append(self.data[i])

        if img != None:
            with open(save_fn, "wb") as f:
                f.write(img)


        # 保存失败的图片
        if len(self.error_img) > 0:
            self.write_csv(os.path.join(self.root, self.error_fn), self.error_img, self.header)

        
        self.change_proxy()

    def change_proxy(self):
        self.session = requests.Session()
        self.session.proxies = self.proxyAddr_list[self.count % self.num]

    def download(self):
        pool = ThreadPoolExecutor(max_workers = 50)
        for i in range(len(self.data)):
        # for i in range(100):
            pool.submit(self.downloadpic, i)
            # break

if __name__ == "__main__":

    # while count < 210:
    D = BaiduStreetDownload()
    D.download()