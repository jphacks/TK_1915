const express = require("express");
const path = require("path");
const line = require("@line/bot-sdk");
const fetch = require('node-fetch');

const PORT = process.env.PORT || 5000;
const config = {
  channelAccessToken: process.env.LINE_TOKEN,
  channelSecret: process.env.LINE_SECRET
};
const client = new line.Client(config);

express()
  .use(express.static(path.join(__dirname, "public")))
  .get("/get/", (req, res) => res.json({ method: "GET" }))
  .post("/hook/", line.middleware(config), (req, res) => lineBot(req, res))
  .listen(PORT, () => console.log(`Listening on ${PORT}`));

function lineBot(req, res) {
  res.status(200).end();
  const events = req.body.events;
  const promises = events.map(e => fetchServer(e));
  Promise.all(promises).then(console.log("pass"));
}

async function fetchServer(event) {
  const restaurantName = event.message.text;
  console.log(restaurantName);
  console.log(typeof restaurantName);
  const res = await fetch(`http://ec2-52-14-100-80.us-east-2.compute.amazonaws.com/count?name=${ encodeURIComponent(restaurantName) }`);
  let formattedRes = await res.json();
  console.log(JSON.stringify(formattedRes));
  console.log(formattedRes.data)
  return client.replyMessage(event.replyToken, {
    type: "text",
    text: `${ restaurantName }は今${ formattedRes.data.count }人並んでいます。\n${ formattedRes.data.que_time }秒程度待つかもしれません。`
  })
}
