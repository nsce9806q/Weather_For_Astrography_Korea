import urllib.parse, urllib.request
from bs4 import BeautifulSoup
import redis
import time
from date import getTimeNow

def getCityKor(city):
    '''
    도시 명을 입력 받아 한글로 반환
    '''
    cities_kor = {
        'seoul': '서울',
        'gangneung': '강릉',
        'daejeon': '대전',
        'daegu': '대구',
        'busan': '부산',
        'jeonju': '전주',
        'gwangju': '광주',
        'jeju': '제주'
    }
    return cities_kor[city]

def getCityCode(city, soup):
    '''
    도시 명과 HTML을 입력 받아 해당 도시 index를 반환
    '''
    for i in range (1,96):
        temp = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(1) > a'.format(i)).text
        if(temp == getCityKor(city)):
            return i

def setWeatherNow():
    '''
    지금 현재 날씨 정보를 redis에 저장
    '''
    rd = redis.StrictRedis(host='localhost',port=6379,charset="utf-8",decode_responses=True,db=0)
    cities = ['seoul','gangneung','daejeon','daegu','busan','jeonju','gwangju','jeju']
    time = getTimeNow()

    try:
        url = "https://www.weather.go.kr/w/obs-climate/land/city-obs.do?auto_man=m&stn=0&dtm=&type=t99&reg=100&tm={}.{}.{}.{}%3A00".format(time['year'],time['month'],time['day'],time['hour'])
        html = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        for i in cities:
            index_city = getCityCode(i,soup)
            weather = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(2)'.format(index_city)).text
            visibility = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(3)'.format(index_city)).text
            cloud = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(4)'.format(index_city)).text
            cloud_low = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(5)'.format(index_city)).text
            temp = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(6)'.format(index_city)).text

            rd.set('now_{}_weather'.format(i),weather)
            rd.set('now_{}_visibility'.format(i),visibility)
            rd.set('now_{}_cloud'.format(i),cloud)
            rd.set('now_{}_cloud_low'.format(i),cloud_low)
            rd.set('now_{}_temp'.format(i),temp)

    except:
        time.sleep(60)
        url = "https://www.weather.go.kr/w/obs-climate/land/city-obs.do?auto_man=m&stn=0&dtm=&type=t99&reg=100&tm={}.{}.{}.{}%3A00".format(time['year'],time['month'],time['day'],time['hour'])
        html = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        for i in cities:
            index_city = getCityCode(i)
            weather = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(2)'.format(index_city)).text
            visibility = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(3)'.format(index_city)).text
            cloud = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(4)'.format(index_city)).text
            cloud_low = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(5)'.format(index_city)).text
            temp = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(6)'.format(index_city)).text

            rd.set('now_{}_weather'.format(i),weather)
            rd.set('now_{}_visibility'.format(i),visibility)
            rd.set('now_{}_cloud'.format(i),cloud)
            rd.set('now_{}_cloud_low'.format(i),cloud_low)
            rd.set('now_{}_temp'.format(i),temp)

setWeatherNow()