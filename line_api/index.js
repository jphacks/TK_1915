const express = require("express");
const path = require("path");
const line = require("@line/bot-sdk");
const fetch = require('node-fetch');

const PORT = process.env.PORT || 5000;
const baseURL = 'http://ec2-52-14-100-80.us-east-2.compute.amazonaws.com/';
const config = {
  channelAccessToken: process.env.LINE_TOKEN,
  channelSecret: process.env.LINE_SECRET
};

const client = new line.Client(config);

function lineBot(req, res) {
  res.status(200).end();
  const events = req.body.events;
  const promises = events.map(e => fetchServer(e));
  Promise.all(promises)
    .then( console.log('request arrived') );
}

async function fetchServer(event) {
  const restaurantName = event.message.text;
  const res = await fetch(`${ baseURL }count?name=${ encodeURIComponent(restaurantName) }`);
  const json = await res.json();
  if (!('data' in json))　{
    return client.replyMessage(event.replyToken, {
      type: 'text',
      text: `すみません。${ restaurantName }というお店は登録されていないか、サービスが一時的に混雑しているようです。`
    })
  }
  const lineStr = json.data.count
    ? `今${ json.data.count }人並んでいます。`
    : `今お店は空いているようです。`;
  const timeStr = json.data.que_time
    ? `\n${ Math.round(Number(json.data.que_time.split('.')[0]) / 60) }分程度待つかもしれません。`
    : ``;
  return client.replyMessage(event.replyToken, {
    type: 'text',
    text: `${ restaurantName }の行列の様子をお伝えします！\n${ lineStr }${ timeStr }`
  })
}

express()
  .get('/', (req, res) => res.send('^o^'))
  .post("/hook/", line.middleware(config), (req, res) => lineBot(req, res))
  .listen(PORT, () => console.log(`Listening on ${PORT}`));
