import requests, random

targetURL = "https://ip.cn/api/index?ip=&type=0"

authKey = "E969FED5"
password = "553B7B73C0CB"
proxyAddr ="tunnel6.qg.net:19707"
# 账密模式
proxyUrl = "http://%(user)s:%(password)s@%(server)s" % {
    "user": authKey,
    "password": password,
    "server": proxyAddr,
}
proxies = {
    "http": proxyUrl,
    "https": proxyUrl,
}
print(proxies)

resp = requests.get(targetURL, proxies=proxies)
print(resp.status_code)
