import asyncio, time, schedule

# 날씨 정보 조회 및 db 저장 모듈
from now import setWeatherNow

'''
특정 시간마다 http 통신을 이용하여 redis에 날씨 정보 저장
'''

# 매 시간 마다
def job_every_hour():
    setWeatherNow()
# 매 자정 마다
def job_every_day():
    pass

'''
스케쥴 항목
'''
schedule.every().hour.at(":00").do(job_every_hour)

while True:
    schedule.run_pending()
    time.sleep(1)