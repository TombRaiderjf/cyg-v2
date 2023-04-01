import requests
from get_cookies import get_cookies
import numpy as np
import string
import time
import torch
import cv2
from torch2trt import TRTModule
import sys, os


def decode(sequence):
    characters = '-' + string.digits + string.ascii_uppercase
    a = ''.join([characters[x] for x in sequence])
    s = ''.join([x for j, x in enumerate(a[:-1]) if x != characters[0] and x != a[j+1]])
    if len(s) == 0:
        return ''
    if a[-1] != characters[0] and s[-1] != a[-1]:
        s += a[-1]
    return s


# 四叶天代理
def get_proxy(tiquApiUrl):
    # 请求地址 简单提取 具体需要根据实际情况获取 记得添加白名单 http://www.siyetian.com/member/whitelist.html
    apiRes = requests.get(tiquApiUrl, timeout=5)
    # 代理服务器
    ipport = apiRes.text
    proxies = {
        'http': ipport,
        'https': ipport
    }
    return proxies


def identify(model, image):
    x_test = torch.Tensor(image).permute(2, 0, 1).unsqueeze(0) / 255
    x_test = x_test.cuda()
    output = model(x_test)
    output_argmax = output.detach().permute(1, 0, 2).argmax(dim=-1)
    return decode(output_argmax[0])


def main(id, neice=False, with_proxy=False, num_proxy=1, proxy_raw=""):
    try:
        os.remove("Cookies.db")
    except:
        print("error")
    width, height = 91, 30

    model_trt = TRTModule()
    model_trt.load_state_dict(torch.load("1130rt_model.pth"))
    model_trt.eval()
    ts = model_trt(torch.randn((1, 3, height, width)).cuda())
    print(ts[0][0][0])
    print("预热结束--------------")

    goodUrl = "http://tl.cyg.changyou.com/goods/char_detail?serial_num=" + id
    img_path = "http://tl.cyg.changyou.com/transaction/captcha-image?goods_serial_num=" + id + "&t=1670051375133"
    if neice:
        goodUrl = "http://tllm.cyg.changyou.com/goods/char_detail?serial_num=" + id
        img_path = "http://tllm.cyg.changyou.com/transaction/captcha-image?goods_serial_num=" + id + "&t=1670051375133"

    buyUrl = "http://tl.cyg.changyou.com/transaction/buy"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'referer': goodUrl
    } 

    # ===============================================
    # 请到get_cookies.py line 55 配置谷歌浏览器cookie路径
    # ===============================================
    cookie_dic = get_cookies("changyou")

    # 查询剩余时间
    page = requests.get(url=goodUrl, headers=header).text
    flag = page.find("data-second")
    if flag != -1:
        time_remained = int(page[flag + 13: flag + 20].split('"')[0])
        print("剩余时间：", time_remained)
    else:
        print("未查询到剩余时间！")
        exit(-1)
    # ===============================================
    # 0.8秒作为预估的公示区到交易区过渡时间的值，可自行修改
    # ===============================================
    time.sleep(time_remained + 0.8)
    # set proxy pool
    if with_proxy:
        proxy_pool = []
        for i in range(num_proxy):
            proxy = get_proxy(proxy_raw)
            proxy_pool.append(proxy)
    count = 0
    multiple = 8
    for i in range(multiple * num_proxy):
        print(i, "********************************")
        t0 = time.time()
        if with_proxy:
            p = proxy_pool[i % num_proxy]
            img = requests.get(url=img_path, cookies=cookie_dic, headers=header, proxies=p).content
        else:
            img = requests.get(url=img_path, cookies=cookie_dic, headers=header).content

        image_np = cv2.imdecode(np.frombuffer(img, np.uint8), 1)

        captcha = identify(model_trt, image_np)
        print(captcha)
        if len(captcha) != 4:
            print("验证码长度错误, 跳过本次post")
            continue
        data = {
            "goods_serial_num": id,
            "captcha_code": captcha
        }
        if with_proxy:
            r = requests.post(url=buyUrl, cookies=cookie_dic, headers=header, data=data, proxies=p)
        else:
            r = requests.post(url=buyUrl, cookies=cookie_dic, headers=header, data=data)
        t_end = time.time()

        print(t_end - t0)
        if r.text == "captcha_error" or r.text == "service_not_available":
            print(r.text)
            continue
        else:
            count += 1
            print(r.text)
            break


if __name__ == '__main__':
    # args: login.py [id] [use_neice] [use_proxy] [num_proxy] [proxy]
    # 参数释义：
    # id: 角色商品号 use_neice: 是否内测（是为1，否为0） use_proxy: 是否使用代理（是为1，否为0）
    # num_proxy：代理可切换的数量 proxy：代理生成的网址
    # example:
    # 使用代理
    # python3 login.py 202303251746489233 0 1 3 http://proxy.siyetian.com/apis_get.html?token=AesJWLORURw4EVJdXTqlEeNpWQx4kaJBjTR1STqFUeNpWR51ERRhXTqVleNpXS65ERJlnT6VFN.wM2IjM0MDM4YTM&limit=1&type=0&time=10&split=1&split_text=&area=0&repeat=0&isp=0
    # 不使用代理（可能出现访问频繁被短暂封ip的情况）
    # python3 login.py 202303251746489233 0 0
    # http://proxy.siyetian.com/apis_get.html?token=AesJWLORURw4EVJdXTqlEeNpWQx4kaJBjTR1STqFUeNpWR51ERRhXTqVleNpXS65ERJlnT6VFN.wM2IjM0MDM4YTM&limit=1&type=0&time=10&split=1&split_text=&area=0&repeat=0&isp=0
    if len(sys.argv) != 6 and len(sys.argv) != 4:
        print("参数错误！")
        sys.exit(-1)
    id_in = sys.argv[1]
    use_neice = bool(int(sys.argv[2]))
    use_proxy = bool(int(sys.argv[3]))
    if len(sys.argv) == 6:
        num_proxy_in = int(sys.argv[4])
        proxy_raw_in = sys.argv[5]
        main(id_in, use_neice, use_proxy, num_proxy_in, proxy_raw_in)
    else:
        main(id_in, use_neice)