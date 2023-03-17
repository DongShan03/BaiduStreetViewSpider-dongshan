import requests, random

proxy_url = "https://proxy.qg.net/allocate?Key=OSVD9AHC&Num=10"
proxy_resp = requests.get(proxy_url).json()["Data"]
proxyAddr_list = [proxy_resp[i]["host"] for i in range(len(proxy_resp))]

# targetURL = "https://www.csdn.net/"

# authKey = "OSVD9AHC"
# password = "996C24265E0A"
# # 账密模式
# proxyUrl = "http://%(user)s:%(password)s@%(server)s" % {
#     "user": authKey,
#     "password": password,
#     "server": proxyAddr,
# }
# proxies = {
#     "http": proxyUrl,
#     "https": proxyUrl,
# }
# resp = requests.get(targetURL, proxies=proxies)
# print(resp.text)

print(random.choice(proxyAddr_list))