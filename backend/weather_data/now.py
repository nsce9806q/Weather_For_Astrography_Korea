import urllib.parse, urllib.request
from bs4 import BeautifulSoup
import datetime, time
import redis

def getTimeNow():
    '''
    현재 시간을 dict 형으로 반환
    ['year'] = 년, ['month'] = 월, ['day'] = 일, ['hour'] = 시 
    '''

    dt = datetime.datetime.now()
    if(dt.month < 10): month = '0'+str(dt.month)
    else: month = dt.month
    if(dt.day < 10): day = '0'+str(dt.day)
    else: day = dt.day
    if(dt.hour < 10): hour = '0'+str(dt.hour)
    else: hour = dt.hour

    time = {
        'year': dt.year,
        'month': month,
        'day': day,
        'hour': hour
    }

    return time

#weather_table > tbody > tr:nth-child(31) > td:nth-child(5)

def getCityCode(city):
    '''
    도시 명을 입력 받아 해당 도시 index를 반환
    '''
    code = {
        'seoul': '41',
        'gangneung': '1',
        'daejeon': '20',
        'daegu': '19',
        'busan': '31',
        'jeonju': '70',
        'gwangju': '11',
        'jeju': '73'
    }
    return code[city]

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
            index_city = getCityCode(i)
            weather = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(2)'.format(index_city)).text
            visibilty = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(3)'.format(index_city)).text
            cloud = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(4)'.format(index_city)).text
            cloud_low = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(5)'.format(index_city)).text
            temp = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(6)'.format(index_city)).text

            rd.set('now_{}_weather'.format(i),weather)
            rd.set('now_{}_visibilty'.format(i),visibilty)
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
            visibilty = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(3)'.format(index_city)).text
            cloud = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(4)'.format(index_city)).text
            cloud_low = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(5)'.format(index_city)).text
            temp = soup.select_one('#weather_table > tbody > tr:nth-child({}) > td:nth-child(6)'.format(index_city)).text

            rd.set('now_{}_weather'.format(i),weather)
            rd.set('now_{}_visibilty'.format(i),visibilty)
            rd.set('now_{}_cloud'.format(i),cloud)
            rd.set('now_{}_cloud_low'.format(i),cloud_low)
            rd.set('now_{}_temp'.format(i),temp)

