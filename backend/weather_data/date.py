import datetime

def getTimeNow():
    '''
    현재 시간을 dict 형으로 반환
    ['year'] = 년, ['month'] = 월, ['day'] = 일, ['hour'] = 시, ['minute'] = 분, ['second'] = 초 
    '''

    dt = datetime.datetime.now()
    if(dt.month < 10): month = '0'+str(dt.month)
    else: month = dt.month
    if(dt.day < 10): day = '0'+str(dt.day)
    else: day = dt.day
    if(dt.hour < 10): hour = '0'+str(dt.hour)
    else: hour = dt.hour
    if(dt.minute < 10): minute = '0'+str(dt.minute)
    else: minute = dt.minute
    if(dt.second < 10): second = '0'+str(dt.second)
    else: second = dt.second

    time = {
        'year': str(dt.year),
        'month': str(month),
        'day': str(day),
        'hour': str(hour),
        'minute': str(minute),
        'second': str(second)
    }

    return time