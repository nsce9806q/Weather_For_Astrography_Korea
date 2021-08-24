import urllib.parse, requests
from bs4 import BeautifulSoup
import redis
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

def setSolarlunarWeek():
    '''
    월령 정보, 해/달 출몰시각 정보 조회 및 저장
    한국천문연구원_월령 정보 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15012689)\n
    한국천문연구원_출몰시각 정보 (https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15012688)
    '''

    # 해/달 출몰시각 정보 조회 및 저장
    url = 'http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getAreaRiseSetInfo'
    service_key = '0rbtzJz4rdyh7HakrikUwkSLlNgQyxNYCrl18zmLIEDrmAngnRRsijrTZmOVani6JZiLnEwRLm%2BbOTQOZ0geJg%3D%3D'
    time = getTimeNow()
    date = time['year']+time['month']+time['day']
    cities = ['seoul','gangneung','daejeon','daegu','busan','jeonju','gwangju','jeju']
    
    rd = redis.StrictRedis(host='localhost',port=6379,charset="utf-8",decode_responses=True,db=0)
    
    for i in cities:
        city = getCityKor(i) 
        queryParams = '?'+'Servicekey='+service_key+'&locdate='+urllib.parse.quote(date)+'&location='+urllib.parse.quote(city)
        response = requests.get(url+queryParams)
        soup = BeautifulSoup(response.text, 'html.parser')

        sunrise = soup.find('sunrise').text
        sunset = soup.find('sunset').text
        moonrise = soup.find('moonrise').text
        moonset = soup.find('moonset').text

        rd.set('today_{}_sunrise'.format(i),sunrise)
        rd.set('today_{}_sunset'.format(i),sunset)
        rd.set('today_{}_moonrise'.format(i),moonrise)
        rd.set('today_{}_moonset'.format(i),moonset)

    # 월령 정보 조회 및 저장
    url = 'http://apis.data.go.kr/B090041/openapi/service/LunPhInfoService/getLunPhInfo'
    queryParams = '?'+'Servicekey='+service_key+'&solYear='+time['year']+'&solMonth='+time['month']+'&solDay='+time['day']
    response = requests.get(url+queryParams)
    soup = BeautifulSoup(response.text, 'html.parser')

    lunar_phase = soup.find('lunage').text
    rd.set('today_lunar_phase',lunar_phase)