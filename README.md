# Quline

[![Product Name](image.png)](https://www.youtube.com/watch?v=G5rULR53uMk)

## 製品概要
### 行列　X　Tech

### 背景
私たちは食堂やラーメン店など飲食店の行列を可視化できないか注目しました。なぜなら、行列は日常の中で無駄な時間を生み出し、ストレスの原因になるからです。  
特に、大学生は日常の中で数多くの行列に出会います。例えば、お気に入りのラーメン屋に行ってみたら行列でとても入れなかった、短い昼休憩の中行った食堂が長蛇の列で講義に遅れてしまったなど、行列に悩まされることは数多くあります。
  
行列を避け、限られた時間を有意義に利用するためにも、私たちは本アプリ、「Quline」を提案します。  

このQulineを開発するにあたって私たちは3つの仮定を置きました。
　　
1. 行列のできることは店側にとっては「繁盛の印、店の広告」という意味が、並んでる人にとってが「行列のできる店で美味しいものを食べる」という意味がある。したがって、行列を「0」にするよりも、「過度な行列を緩和する」アプローチのほうが有効である。
2. 行列の原因はある時間に需要が集中することにある。したがって、人々がある行列に並び始めるタイミングを調整すれば行列は緩和されるはずである。
3. 飲食店は顧客満足度のために過度な行列を緩和したいという気持ちはあるが、新しい技術やツールの導入コストやワークフローの変更への躊躇から、対策ができていない。

#### 飲食店の行列についての競合プロダクト
このプロダクトの競合サービスには以下のものがありますが、それらにも問題点があります。
* Google Map: スマートフォンの位置情報から統計情報を取得し、統計的な混雑度合いがわかります。しかし、統計的な情報なのでリアルタイムな混雑度合いとスマートフォンに表示されている混雑度合いが異なることがあります。
* O:der: リモート受付・l予約に対応したアプリ。店側はタブレット端末で注文を確認することができる。しかし、この方法だとアプリを使っている人の情報しかわからないという問題がある。また、店側のワークフローが変更させることになる。

### 製品説明
飲食店の行列は客にとって時間を無駄にしてしまう悩みのタネであり、できれば避けたいものです。
一方で店側にとっては繁盛の証でもありますが、列が長すぎると満足なサービスを提供できなくなる可能性があるため、うまく調節したい対象です。

このサービスでは，店先にネットワークカメラを設置するだけで映像から行列の人数を検出し，おおよその待ち時間を計算して客に通知するといった機能を提供します。

### 特長

#### 1. Plug & goのIoTカメラ

#### 2. あらゆるデバイスで

#### 3. ChainerCVで最先端の物体検出
ChainerCVを使えば最先端の画像分類モデルを手軽に実装できます。今回は、学習済みのYOLOv3モデルを用いて物体検出を用いて画像から人物の人数を推定しています。

### 解決出来ること

#### 行列にならぶ時間を短く
Qulineなら、あなたのスマートフォンからLINE bot使って気になるお店の今の待ち時間の状況がわかります。待ち時間が長ければ他のことをして後で行くもよし。他の店を発掘するのもよし。ただ、行列を待つよりも充実した時間を過ごすことができます。

#### ワークフローを変えることなく、来客数の最適化

常に客の来店数を適切な長さに調整することができます。また、デバイスを設置してwifiに接続するだけという手軽さで、店のワークフローを変更する必要がありません。今まで通りの注文、調理フローでデバイスを設置するだけで来客ピークの厨房の忙しさを緩和します。また、完全に行列の

### 今後の展望
今回は時間の都合で以下を達成することができませんでした。
- 周辺の店舗のレコメンド 
- 同一人物推定


## 開発内容・開発技術
### 活用した技術
#### API・データ
- AWS EC2

#### フレームワーク・ライブラリ・モジュール
* Python3 
* Flask 
* AWS EC2 
* React 
* ChainerCV, Chainer
* Node.js
* Heroku

#### デバイス
* Rasberry Pi 
* USBカメラ

### 研究内容・事前開発プロダクト（任意）
なし

### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* 
