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
app.use(cors());

//const kassi = require('./modules/moonset_time.js');

app.get('/', (req, res) => {
    res.send([{location: 'Seoul', moonset_time: 1234}]);
})

// async error 문제
app.get('/time', async (req, res) => {
    item = [
        {location: '서울', time: await getData('seoul')},
        {location: '대전', time: await getData('daejeon')},
        {location: '대구', time: await getData('daegu')},
        {location: '부산', time: await getData('busan')},
    ]
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