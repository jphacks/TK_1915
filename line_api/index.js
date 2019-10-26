const express = require("express");
const path = require("path");
const line = require("@line/bot-sdk");

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
  console.log(events);
  const promises = events.map(e => echoman(e));
  Promise.all(promises).then(console.log("pass"));
}

// 追加
async function echoman(ev) {
  const pro =  await client.getProfile(ev.source.userId);
  console.log(pro);
  return client.replyMessage(ev.replyToken, {
    type: "text",
    text: `${pro.displayName}さん、今「${ev.message.text}」って言いました？`
  })
}
