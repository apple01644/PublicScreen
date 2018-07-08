import re
import urllib.request

def get_food(a):
    url = "http://www.dgsw.hs.kr/user/carte/list.do?menuCd=MCD_000000000000029947"

    data = urllib.request.urlopen(url).read()
    src = data.decode('utf-8')

    start = src.find('<ul class="meals_today_list">')

    src = src[start + len('<ul class="meals_today_list">'):]

    end = src.find('</ul>')
    src = src[:end]
    src = src.replace('\t','')
    src = src.replace('\r','')

    src = src.replace('.','')
    src = src.replace('0','')
    src = src.replace('1','')
    src = src.replace('2','')
    src = src.replace('3','')
    src = src.replace('4','')
    src = src.replace('5','')
    src = src.replace('6','')
    src = src.replace('7','')
    src = src.replace('8','')
    src = src.replace('9','')

    food_early = ""
    food_middle = ""
    food_late = ""

    src = src[src.find('<img'):]
    src = src[src.find('/>') + len('/>'):]

    food_early = src[:src.find('</li>')];

    src = src[src.find('<img'):]
    src = src[src.find('/>') + len('/>'):]

    food_middle = src[:src.find('</li>')];

    src = src[src.find('<img'):]
    src = src[src.find('/>') + len('/>'):]

    food_late = src[:src.find('</li>')];

    if a == 0:
        fe = food_early.split('\n')
    elif a == 1:
        fe = food_middle.split('\n')
    elif a == 2:
        fe = food_late.split('\n')

    returns = []
    for s in fe:
        if len(s) == 0:
            continue
        while s[0] == ' ':
            s = s[1:]
            if len(s) == 0:
                break
        if len(s) == 0:
            continue
        while s[-1] == ' ':
            s = s[:-1]
            if len(s) == 0:
                break
        if len(s) > 0:
            #print(s,":")
            returns.append(s)
    return returns
    #print("점심\n", food_middle)
    #print("저녁\n", food_late)
