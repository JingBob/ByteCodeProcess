import requests
import re
from time import sleep
import pandas as pd
import os
from requests.adapters import HTTPAdapter

# 这里改成自己的代理，我的代理都是http，不设置代理运行20次都不一定连的上
http_proxy = "http://127.0.0.1:1087"
https_proxy = "http://127.0.0.1:1087"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
}

session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=5))  # 设置重试次数为3次
session.mount('https://', HTTPAdapter(max_retries=5))

# 你去你自己浏览器抓包一下header
headers = {
    'authority': 'github.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'referer': 'https://github.com/login?client_id=fc21d3f3a55a8993a3ba&return_to=^%^2Flogin^%^2Foauth^%^2Fauthorize^%^3Fclient_id^%^3Dfc21d3f3a55a8993a3ba^%^26redirect_uri^%^3Dhttp^%^253A^%^252F^%^252Flocalhost^%^253A8000^%^252Foauth^%^252Fredirect',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_device_id=b9ad40169b03a06f5df01354566a8c5b; _octo=GH1.1.572039612.1631370445; tz=Etc^%^2FGMT-8; tz=Etc^%^2FGMT-8; color_mode=^%^7B^%^22color_mode^%^22^%^3A^%^22auto^%^22^%^2C^%^22light_theme^%^22^%^3A^%^7B^%^22name^%^22^%^3A^%^22light^%^22^%^2C^%^22color_mode^%^22^%^3A^%^22light^%^22^%^7D^%^2C^%^22dark_theme^%^22^%^3A^%^7B^%^22name^%^22^%^3A^%^22dark^%^22^%^2C^%^22color_mode^%^22^%^3A^%^22dark^%^22^%^7D^%^7D; has_recent_activity=1; user_session=0xw5HZYt3oW3UOI0PIdyqY7RjmNuGs4PjLa9sA0RlGj_L5cj; __Host-user_session_same_site=0xw5HZYt3oW3UOI0PIdyqY7RjmNuGs4PjLa9sA0RlGj_L5cj; logged_in=yes; dotcom_user=JingBob; _gh_sess=sVmautyn5ZmIpoxmWOEXbtoJrqyM83CFxaPBDGRBkiAqcIFSMcMoigLVrpG^%^2BOZsol8m3uxj4OQ7iX4MGmHr9xBStVLBgxjbbdw4wqVAPaEKid6jEtxD5eFmbnPu^%^2Bk8qS7ITLOCBArpm^%^2BDPSwGcnFgFWT5qSFpaprD4yaGRU5Ywxcl1X7INIM4q2zLzjlYZTiwUQEPU^%^2FRD9ycmfg1onWXLLv5uNv^%^2B8OmUNjs^%^2FFWi2XvH9K5d4o2pGw2xYGpMLbKLl3PCpgAR^%^2B0OpDNJtLAOOGETQ2jfdVv^%^2Ftp^%^2BAtJHEgeSd0anWpOZuRgIkmjW2^%^2FycGSCgQwq8NBePLT4M9^%^2Bs9B^%^2FBzCBU10OUiDmopX5j0rrRH608n9R7DFmV5cDybxZ3EE4Pcr5ZEqTjtsq4463P2fQZgA2GK64g6FBTj8EXNLSoG3p5aLjIjJ^%^2Bpq8zlUa6Ee2Rb4I77roeEJ07sReToF130RhMQSne9ZYNGjT6F7vugioDfRiLZ9TNm^%^2FKG8xyytzHE9UBmwxA^%^2B71G4fXYz9P71lVYf73orOQOWdQyw^%^2BjluAgC4cyZXO^%^2BJhtbTNpsWAgMUu2NR1XBwDIBOYdxCcf8vfs1l071R24dYjL02fXj1Wc^%^2FQlQFkH6wxb4PL^%^2FeAWO0TIIUTh9oaF8w3rv5wXIxMrzvqOl5T0kJvPGjbBYQ06Y9LK^%^2B2sbrNjnddcc8axm1GtFROFO9DUlXmiiBw1qsd4GNx3B2hfk2Hh3v1UgTb4CnI1JkaYWzggscZRW3BQDztrzSOCrP2WwqpTI7HwJOiHw1iqRCj4xa6vh8N0pE7XToPf^%^2By^%^2FuF2c7hKx11RE3N8hbtyiaSaNBKqtWMe8Ugks0nPSyJNEqOupEFL5LYCB8nQRQ5rZ^%^2B3lb8Fxy6bnJjKeWBlgLfL18Cl8ScRvjODNA27scZWuV^%^2FpHv79lWeGP4CMVWK3FhT7zpENoqhhDu0i5FjtAcvRdwkCT9fsPvvL23--w9Ty2E0m48C58JP4--QTXLdTgxEbBpju9Agxjohw^%^3D^%^3D',
    'if-none-match': 'W/^\\^8cca622ac86cf58e94505c1961754d01^\\^',
}

# 我用的是oauth验证方式，参考链接：http://www.ruanyifeng.com/blog/2019/04/github-oauth.html
# 主要分为以下几步
# 首先你得去自己的github生成自己的oauth，记住自己的id和secret，下面这些是我的
ClientID = 'fc21d3f3a55a8993a3ba'
ClientSecrets = '8b29a47979e4706d2639e61e20d0bc49321aea0c'

params = (
    ('client_id', ClientID),
    ('redirect_uri', 'http://localhost:8000/oauth/redirect'),
)
# 先请求github进行验证，这里得模拟一波github登录，由于我cookie有的登录信息，我直接get就相当于直接登录了
response = session.get('https://github.com/login/oauth/authorize', headers=headers, params=params, proxies=proxyDict,
                       verify=False)
print(response.text)
# 然后获取github返回的code
codeurl = re.findall('data-url=".*?"', response.text, re.S)
print(codeurl)
for i in codeurl:
    i = i.split("code=")
    code = i[-1][0:-1]
    print(code)
    break


# 接着用这个code获取github的验证token，之后访问api带上这个token就能实现5000次访问
def github_token(code):
    """
    通过传入的 code 参数，带上client_id、client_secret、和code请求GitHub，以获取access_token
    :param code: 重定向获取到的code参数
    :return: 成功返回acces_token；失败返回None；
    """
    token_url = 'https://github.com/login/oauth/access_token?''client_id={}&client_secret={}&code={}'
    token_url = token_url.format(ClientID, ClientSecrets, code)  # 这里的client_id、client_secret修改为自己的真实ID与Secret
    header = {
        'accept': 'application/json'
    }
    print(token_url)
    res = session.post(token_url, headers=header, proxies=proxyDict, verify=False)
    if res.status_code == 200:
        res_dict = res.json()
        print(res_dict)
        return res_dict['access_token']
    return None


# 到此为止，验证完成
access_token = github_token(code)
print(access_token)


def IfContainPom(url, headers):
    url = url
    print(url)
    sleep(0.5)
    # 设置header维持cookie
    r = session.get(url, headers=headers, proxies=proxyDict, verify=False, timeout=(600, 600))
    d = r.json()
    print(d)
    for item in d:
        if item['name'] == 'pom.xml':
            return 1
        if item['name'] == "build.gradle":
            return 2
    return 0


getwhatpro = 'kotlin'


def get_java(access_token):
    """
    通过传入的access_token，带上access_token参数，向GitHub用户API发送请求以获取用户信息；
    :param access_token: 用于访问API的token
    :return: 成功返回用户信息，失败返回None
    """
    if not os.path.exists(getwhatpro + "data"):
        os.mkdir(getwhatpro + "data")
    getcount = '11-21'

    access_token = 'token {}'.format(access_token)
    headers = {
        'accept': 'application/json',
        'Authorization': access_token
    }
    for i in range(10, 21):
        # 看一下剩余的查询API次数
        print(i)
        print(
            session.get('https://api.github.com/rate_limit?access_token=%s' % access_token, headers=headers,
                        proxies=proxyDict, verify=False).json())
        # 规定每页包含100条数据，访问前10页，按照星数排列
        url = 'https://api.github.com/search/repositories?q=%s+language:%s&sort=stars&order=desc&page=' % (
            getwhatpro, getwhatpro) + str(i) + '&per_page=100'
        # 分别设置请求超时时间和读取超时时间
        r = session.get(url, headers=headers, proxies=proxyDict, verify=False, timeout=(600, 600))
        print(r.status_code)
        if r.status_code == 200:
            d = r.json()
            print(len(d['items']))
            df = pd.DataFrame(columns=['name', 'owner', 'description', 'stars', 'date', 'url'])
            for j in range(len(d['items'])):
                owner = d['items'][j]['owner']['login']
                name = d['items'][j]['name']
                description = d['items'][j]['description']
                url = d['items'][j]['html_url']
                stars = d['items'][j]['stargazers_count']
                date = d['items'][j]['created_at']
                url1 = 'https://api.github.com/repos/' + url[
                                                         re.search('https://github.com/', url).end():] + '/contents'
                flag = IfContainPom(url1, headers)
                if flag == 1:
                    with open("%sdata//%sscriptPOM%s.bat" % (getwhatpro, getwhatpro, getcount), "a+")as f:
                        f.write(
                            "git clone git://github.com/" + url[
                                                            re.search('https://github.com/', url).end():] + "\n")
                elif flag == 2:
                    with open("%sdata//%sscriptGradle%s.bat" % (getwhatpro, getwhatpro, getcount), "a+")as f:
                        f.write(
                            "git clone git://github.com/" + url[
                                                            re.search('https://github.com/', url).end():] + "\n")
                df.loc[len(df)] = [name, owner, description, stars, date, url]
            df.to_csv('%sdata//%s%s.csv' % (getwhatpro, getwhatpro, getcount), mode='a+', index=0,
                      encoding='utf_8_sig')


get_java(access_token)
