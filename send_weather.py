#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @file: get_weather.py
# @author: xulinzhou
# @date  : 2020/01/218

import requests
import json
import sxtwl
import time
from datetime import date
from translate import Translator
import re

# 时间戳转阳历日期
def time_stamp_to_date(time_stamp):
    return time.strftime("%Y--%m--%d", time.localtime(time_stamp))


# 日历中文索引
ymc = [u"十一", u"十二", u"正", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十"]
rmc = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十", \
       u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九", \
       u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", u"廿九", u"三十", u"卅一"]

# 阳历转阴历，入参格式为：xxxx-xx-xx
def solar_to_lunar(solar_date):
    # 日历库实例化
    lunar = sxtwl.Lunar()

    today = str(solar_date)  # 如 2019-08-08
    today_list = today.split('-')  # ['2019', '08', '08']
    lunar_day = lunar.getDayBySolar((int)(today_list[0]), (int)(today_list[1]), (int)(today_list[2]))  # 输入年月日
    # 判断是否为润年
    if (lunar_day.Lleap):
        # print("润{0}月{1}".format(ymc[lunar_day.Lmc], rmc[lunar_day.Ldi]))
        return "润{0}月{1}".format(ymc[lunar_day.Lmc], rmc[lunar_day.Ldi])
    else:
        # print("{0}月{1}".format(ymc[lunar_day.Lmc], rmc[lunar_day.Ldi]))
        return "{0}月{1}".format(ymc[lunar_day.Lmc], rmc[lunar_day.Ldi])

# 获取星期几
def get_week_day(date):
  week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期日',
  }
  day = date.weekday()
  return week_day_dict[day]


# 当前天气转换，入参为接口返回的string
def sky_exchange_chinese(sky):
    # 天气：晴、多云、阴、小雨、中雨、大雨、暴雨、小雪、中雪、大雪、暴雪
    if sky.startswith("CLEAR"):
        sky = "晴"
    elif sky.startswith("CLOUDY"):
        sky = "多云"
    elif sky.startswith('PARTLY_CLOUDY'):
        sky = "阴"
    elif sky.startswith("HAZE"):
        sky = "霾"
    elif sky.startswith("RAIN_L"):
        sky = "小雨"
    elif sky.startswith("RAIN_M"):
        sky = "中雨"
    elif sky.startswith("SNOW_L"):
        sky = "小雪"
    elif sky.startswith("SNOW_M"):
        sky = "中雪"
    elif sky == "WIND":
        sky = "风"
    else:
        translator = Translator(from_lang="English", to_lang="chinese")
        sky = translator.translate(sky)
    return sky


# 整天天气转换，参数为早上天气和晚上天气
def daily_sky_exchange(down_sky, up_sky):
    down_sky = sky_exchange_chinese(down_sky)
    up_sky = sky_exchange_chinese(up_sky)
    if down_sky == up_sky:
        tomorrow_sky = down_sky
    else:
        tomorrow_sky = down_sky + "转" + up_sky
    return tomorrow_sky


# aqi转换
def aqi_exchange(aqi):
    if aqi <= 0:
        aqi = ""
    elif aqi <= 50:
        aqi = str(aqi) + "优"
    elif aqi <= 100:
        aqi = str(aqi) + "良"
    elif aqi <= 150:
        aqi = str(aqi) + "轻度污染"
    elif aqi <= 200:
        aqi = str(aqi) + "中度污染"
    elif aqi <= 300:
        aqi = str(aqi) + "重度污染"
    elif aqi > 300:
        aqi = str(aqi) + "严重污染"
    else:
        pass
    return aqi


# 风力转换，单位：km/h
def wind_speed_exchange(windSpeed):
    if windSpeed <= 0.2 * 3.6:
        windSpeed = "无风"
    elif windSpeed <= 1.5 * 3.6:
        windSpeed = "1级软风"
    elif windSpeed <= 3.3 * 3.6:
        windSpeed = "2级轻风"
    elif windSpeed <= 5.4 * 3.6:
        windSpeed = "3级微风"
    elif windSpeed <= 7.9 * 3.6:
        windSpeed = "4级和风"
    elif windSpeed <= 10.7 * 3.6:
        windSpeed = "5级清风"
    elif windSpeed <= 13.8 * 3.6:
        windSpeed = "6级强风"
    elif windSpeed <= 17.1 * 3.6:
        windSpeed = "7级疾风"
    elif windSpeed <= 20.7 * 3.6:
        windSpeed = "8级大风"
    elif windSpeed <= 24.4 * 3.6:
        windSpeed = "9级烈风"
    elif windSpeed <= 28.4 * 3.6:
        windSpeed = "10级狂风"
    elif windSpeed <= 32.6 * 3.6:
        windSpeed = "11级暴风"
    elif windSpeed <= 36.9 * 3.6:
        windSpeed = "12级台风"
    elif windSpeed <= 41.4 * 3.6:
        windSpeed = "13级台风（一级飓风）"
    elif windSpeed <= 46.1 * 3.6:
        windSpeed = "14级强台风（一级飓风）"
    elif windSpeed <= 50.9 * 3.6:
        windSpeed = "15级强台风（二级飓风）"
    elif windSpeed <= 56.0 * 3.6:
        windSpeed = "16级超强台风（三级飓风）"
    elif windSpeed <= 61.2 * 3.6:
        windSpeed = "17级超强台风（四级飓风）"
    elif windSpeed > 61.2 * 3.6:
        windSpeed = "18级超强台风（五级飓风）"
    else:
        pass
    return windSpeed


# 风向转换
def wind_direction_exchange(windDirection):
    if windDirection <= 11.25 or windDirection > 348.76:
        windDirection = "北风"
    elif windDirection < 33.75:
        windDirection = "北东北风"
    elif windDirection < 56.25:
        windDirection = "东北风"
    elif windDirection < 78.75:
        windDirection = "东东北风"
    elif windDirection < 101.25:
        windDirection = "东风"
    elif windDirection < 123.75:
        windDirection = "东东南风"
    elif windDirection < 146.25:
        windDirection = "东南风"
    elif windDirection < 168.75:
        windDirection = "南东南风"
    elif windDirection < 191.25:
        windDirection = "南风"
    elif windDirection < 213.75:
        windDirection = "南西南风"
    elif windDirection < 236.25:
        windDirection = "西南风"
    elif windDirection < 258.75:
        windDirection = "西西南风"
    elif windDirection < 281.25:
        windDirection = "西风"
    elif windDirection < 303.75:
        windDirection = "西西北风"
    elif windDirection < 326.25:
        windDirection = "西北风"
    elif windDirection < 348.75:
        windDirection = "北西北风"
    else:
        pass
    return windDirection


# 当前提示语转换
def des_exchange(des):
    # 用Translator翻译成中文也不是很友好，所以优先人工翻译
    if "clear weather over the next 24 hours" == des:
        des = "未来24小时晴"
    elif "overcast, drizzle after" in des and "o'clock tomorrow midnight, followed by cloudy" in des:
        des = "小雨，明天午夜" + str(re.findall(r"\d+", des)[0]) + "点钟后雨停，转阴，其后小雨"
    elif "drizzle turn into overcast, drizzle expected after" in des and "o'clock tomorrow midnight" in des:
        des = "阴，明天午夜" + str(re.findall(r"\d+", des)[0]) + "点钟后转小雨，其后阴"
    elif "clear weather, cloudy after" in des and "tomorrow afternoon, increasing cloudiness" in des:
        des = "晴，明天傍晚" + str(re.findall(r"\d+", des)[0]) + "点钟后转多云，其后云渐多"
    elif "overcast, drizzle after" in des and "o'clock tomorrow morning, followed by overcast" in des:
        des = "多云，明天早上" + str(re.findall(r"\d+", des)[0]) + "点后有毛毛雨，随后多云"
    else:
        m = re.compile(r'^[a-zA-Z0-9,\'\s.]*$') # 判断是否为英文字符串
        if m.match(des): # 如果是英文字符串，则翻译成中文
            translator = Translator(from_lang="English", to_lang="chinese")
            des = translator.translate(des)
        else:
            pass
    return des


# 未来2小时提示语转换
def desc_exchange(desc):
    # 用Translator翻译成中文也不是很友好，所以优先人工翻译
    if "No snow in the next hour, go out and play" == desc:
        desc = "未来两小时不会下雪，放心出门吧"
    elif "No rain in the next hour, go out and play" == desc:
        desc = "未来两小时不会下雨，放心出门吧"
    elif "Very windy outside! Don't get blown away" == desc:
        desc = "大风起兮...注意不要被风刮跑"
    elif "Cloudy here but it's raining east" in desc and "km away" in desc:
        desc = "您东边" + str(re.findall(r"\d+", desc)[0]) + "公里外正在下雨哦"
    elif "Cloudy here but it's raining south" in desc and "km away" in desc:
        desc = "这里多云，但南边" + str(re.findall(r"\d+", desc)[0]) + "公里处正在下雨"
    elif desc == "Get some rest indoors; the air isn't clean":
        desc = "空气不太好，在室内休息一下吧"
    else:
        m = re.compile(r'^[a-zA-Z0-9,\'\s.]*$') # 判断是否为英文字符串
        if m.match(desc): # 如果是英文字符串，则翻译成中文
            translator = Translator(from_lang="English", to_lang="chinese")
            desc = translator.translate(desc)
        else:
            pass
    return desc


headers = {
    "Host": "wr.bubr.net:8080",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "User-Agent": "LiveWeather/1.8.3 (iPhone; iOS 11.4.1; Scale/2.00)",
    "AccessToken": "b7ee103a47d274940b1a0cce54abac17",
    "Accept-Language": "zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-CN;q=0.8, zh-Hant-HK;q=0.7",
    "Content-Length": "464",
    "Connection": "keep-alive"
}


data = {
	"address": {
		"state": "北京市",
		"temp": -6,
		"zt": "Asia\/Shanghai",
		"longitude": "116.3979471",
		"subLocality": "",
		"latitude": "39.9081726",
		"city": "北京市",
		"maxTemp": 0,
		"skycon": "CLEAR_DAY",
		"country": "中国",
		"isScenic": "false",
		"minTemp": 0
	}
}

# 【实况天气】app的首页请求
url = "http://wr.bubr.net:8080/weather/data2"


# @allure.feature("首页")
def get_weather():
    s = requests.post(url, headers=headers, json=data)
    s = json.loads(s.text)
    # print(str(s) + '\n')

    # 获取接口response返回的相关字段
    waring_info = "无"
    try:
        waring_info = s["data"]["alert"]["Description"]
    except:
        pass
    cur_sky = s["data"]["cur"]["skycon"]
    try:
        cur_aqi = s["data"]["cur"]["aqi"]  # 当前空气质量
    except:
        cur_aqi = -1
    cur_pm25 = s["data"]["cur"]["pm25"]  # PM2.5
    cur_pm10 = s["data"]["cur"]["pm10"]  # PM10
    cur_temperature = s["data"]["cur"]["temperature"] # 当前温度
    cur_humidity = s["data"]["cur"]["humidity"] # 空气湿度
    cur_des = s["data"]["cur"]["des"] # 未来24小时晴
    cur_desc = s["data"]["cur"]["desc"] # 未来两小时不会下雪，放心出门吧
    cur_windSpeed = s["data"]["cur"]["windSpeed"]  # 风速8.9
    cur_windDirection = s["data"]["cur"]["windDirection"] # 风向321.09

    today_infos = s["data"]["daily"]["list"][0]
    tomorrow_infos = s["data"]["daily"]["list"][1]
    today_htemp = today_infos[1] # 今日最高温度
    today_ltemp = today_infos[2] # 今日最低温度
    today_sunset = today_infos[18]  # 今日日出
    today_sunrise = today_infos[19] # 今日日落
    tomorrow_htemp = tomorrow_infos[1]  # 明天最高温度
    tomorrow_ltemp = tomorrow_infos[2]  # 明天最低温度
    tomorrow_aqi = tomorrow_infos[5] # 明天空气
    tomorrow_sunrise = tomorrow_infos[19]  # 明天日出
    tomorrow_sunset = tomorrow_infos[18]  # 明天日落
    tomorrow_down_sky = tomorrow_infos[7] # 明天早上天气
    tomorrow_up_sky = tomorrow_infos[8] # 明天晚上天气

    # 将接口拿到的数据进行进一步格式化处理，以下为最后得到的数据
    cur_sky = sky_exchange_chinese(cur_sky)
    today_ltemp = str(round(today_ltemp))
    today_htemp = str(round(today_htemp))
    cur_windDirection = wind_direction_exchange(cur_windDirection)
    cur_windSpeed = wind_speed_exchange(cur_windSpeed)
    cur_wind_info = cur_windDirection + " " + cur_windSpeed
    cur_aqi = aqi_exchange(int(cur_aqi))
    if cur_aqi == "":
        cur_aqi_info = ""
    else:
        cur_aqi_info = "{0}(PM2.5={1}，PM10={2})，".format(cur_aqi, cur_pm25, cur_pm10)
    cur_temperature = round(cur_temperature)
    cur_humidity = str(int(float(cur_humidity) * 100)) + "%"
    cur_des = des_exchange(cur_des)
    cur_desc = desc_exchange(cur_desc)
    tomorrow_sky = daily_sky_exchange(tomorrow_down_sky, tomorrow_up_sky)
    tomorrow_htemp = round(tomorrow_htemp)
    tomorrow_ltemp = round(tomorrow_ltemp)
    tomorrow_aqi = aqi_exchange(int(tomorrow_aqi))
    tomorrow_sunrise = tomorrow_sunrise
    tomorrow_sunset = tomorrow_sunset
    # 公历日期（今天）
    solar_date = date.today()
    # 阴历日期
    lunar_date = solar_to_lunar(solar_date)
    # 今天星期几
    today_weekday = get_week_day(solar_date)

    # 最后要发送的信息内容
    notice_info = "{0}({1} {2})：\n北京今日{3}，{4} ~ {5}℃，{6}，空气质量{7}当前室外温度{8}℃，湿度{9}。{10}；{11}\n预警信号：{12}\n\n预计明天：{13}，{14} ~ {15}℃，空气质量{16}，日出{17} 日落{18}。".format(
        solar_date, lunar_date, today_weekday, cur_sky, today_ltemp, today_htemp, cur_wind_info, cur_aqi_info, cur_temperature, cur_humidity, cur_des, cur_desc,
        waring_info, tomorrow_sky, tomorrow_ltemp, tomorrow_htemp, tomorrow_aqi, tomorrow_sunrise, tomorrow_sunset)

    # 如果是晚上八点到八点半之间执行的脚步，则写入history.txt
    print("time hours:" + str(int(time.strftime("%H", time.localtime()))))
    print("time minutes:" + str(int(time.strftime("%M", time.localtime()))))
    write_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if (int(time.strftime("%H", time.localtime())) == 20) and (int(time.strftime("%M", time.localtime())) < 5):
        print("写入history.txt:" + str(write_time))
        # 如果脚本执行时间在设定的时间段内，则将每日天气的信息保存到history.txt中
        with open("history.txt", "a+") as f:
            row = str(write_time) + "    " + str(solar_date) + "（" + str(lunar_date) + "）" + str(today_weekday) + "    " + str(cur_sky) + "    " + str(today_ltemp) + "    " + str(today_htemp) + "    " + str(cur_windDirection) + "    " + str(cur_windSpeed) + "    " + str(cur_aqi_info[:-1]) + "    " + str(cur_humidity) + "    " + str(today_sunrise) + "    " + str(today_sunset) + "    " + str(waring_info) + "\n"
            print("row:" + row)
            f.write(row)
    # 否则，测试数据写入test_zzz.txt，用于平时调试
    else:
        print("写入test_zzz.txt:" + write_time)
        with open("test_zzz.txt", "a+") as f:
            row = str(write_time) + "    " + str(solar_date) + "（" + str(lunar_date) + "）" + str(today_weekday) + "    " + str(cur_sky) + "    " + str(today_ltemp) + "    " + str(today_htemp) + "    " + str(cur_windDirection) + "    " + str(cur_windSpeed) + "    " + str(cur_aqi_info[:-1]) + "    " + str(cur_humidity) + "    " + str(today_sunrise) + "    " + str(today_sunset) + "    " + str(waring_info) + "\n"
            print("row:" + row)
            f.write(row)

    return notice_info


if __name__ == "__main__":
    weather_message = get_weather()
    print(weather_message)
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": weather_message
        }
    }
    # 下面改成你的机器人对应的webhook地址
    kim_robot_url = "https://kim.corp.kuaishou.com/hooks/robot/send?key=xxxxxx"
    dingtalk_robot_url = "https://oapi.dingtalk.com/robot/send?access_token=xxxxxx"
    weixin_robot_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxx"
    r = requests.post(url=kim_robot_url, headers=headers, json=data)
    print("kim发送状态：" + r.text) # 查看kim的发送状态
    r = requests.post(url=dingtalk_robot_url, headers=headers, json=data)
    print("钉钉发送状态：" + r.text) # 查看钉钉的发送状态
    r = requests.post(url=weixin_robot_url, headers=headers, json=data)
    print("企业微信发送状态：" + r.text) # 查看企业微信的发送状态
