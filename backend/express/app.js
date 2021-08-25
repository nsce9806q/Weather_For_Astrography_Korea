/*
1. redis에 저장 된 데이터들을 정제하여 RestApi 통신
*/


const express = require('express');
const app = express();
const port = 3000;

//redis 연동
const redis = require('redis');
var client = redis.createClient();
client.on('error', function (err) {
    console.log('Error ' + err);
});

//CORS 에러 해결
const cors = require('cors');
const { SSL_OP_DONT_INSERT_EMPTY_FRAGMENTS } = require('constants');
app.use(cors());

//const kassi = require('./modules/moonset_time.js');

app.get('/', (req, res) => {
    res.send([{location: 'Seoul', moonset_time: 1234}]);
})

function getCityKo(city){
    city_kor = {
        'seoul': '서울',
        'gangneung': '강릉',
        'daejeon': '대전',
        'daegu': '대구',
        'busan': '부산',
        'jeonju': '전주',
        'gwangju': '광주',
        'jeju': '제주'
    }

    return city_kor[city]
}

// async error 문제
app.get('/now', async (req, res) => {
    const cities = ['seoul','gangneung','daejeon','daegu','busan','jeonju','gwangju','jeju'];
    var item = []
    for (var i in cities){
        city = cities[i]
        var weather = 'now_'+city+'_weather';
        var visibilty = 'now_'+city+'_visibility';
        var cloud = 'now_'+city+'_cloud';
        var cloud_low = 'now_'+city+'_cloud_low';
        var temp = 'now_'+city+'_temp';
        var sunrise = 'today_'+city+'_sunrise'
        var sunset = 'today_'+city+'_sunset'
        var moonrise = 'today_'+city+'_moonrise'
        var moonset = 'today_'+city+'_moonset'

        item.push({
            '도시명': getCityKo(city),
            '날씨': await getData(weather),
            '시정거리': await getData(visibilty),
            '운량': await getData(cloud),
            '중하운량': await getData(cloud_low),
            '현재 기온': await getData(temp),
            '일출 시간': await getData(sunrise),
            '일몰 시간': await getData(sunset),
            '월출 시간': await getData(moonrise),
            '월몰 시간': await getData(moonset)
        })
    }

    res.send(item);
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
}) 
    

function getData(key){
    return new Promise((resv, rej) => {
        client.get(key, (err, reply) => {
            resv(reply)
        });
    })
}