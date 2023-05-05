# 大体プライグインreloadしたら治ります`plugin reload pras`

# GBC-RLCS
- GBC用オーバーレイ追加ソフトウェア（ブースト・トランジション）

# Features
- 前提の**bakkesmod Plugin**を導入することで簡単に利用することができます．
- オーバーレイはOBSにて**Local Browser**として簡単に読み込むことができます．
- ユーザー用の**CUI**を完備
- Websocket，Socket通信で実装しているため，**リアルタイム性が高い**です．

# Requirement
- Bakkesmod Plugin "Pras"
- Windows Terminal
  
# Installation
- bakkesmod Pluginの導入に関しては[ここ](https://note.com/forusian/n/n0d15fde904d3)を参照ください．
- Windows Terminalの導入に関しては[ここ](https://www.curict.com/item/26/2629f94.html)を参照ください．

# Usage

1\. `GB_RLCS`フォルダで右クリックし，**ターミナルで開く**をクリックします．
そして，`./GBC_RLCS.exe`と打ち込むと本ソフトウェアが起動します．

2\.  RL内のbakkesmodにてPrasをロードします．(F6押下から`plugin load pras`)  

3\. CUIにて，**RL=>GBC-S2Ws**欄の**Others**が`None`から変化すれば接続良好です．(UDP通信のため，コネクションを確立する必要はありません)  

4\. `graphics`フォルダにある`boost.html`,`transition.html`をOBSのブラウザソースにて**ローカルファイル**にチェックを入れ，読み込みます．(**シーンがアクティブになったときにブラウザの表示を更新する**にチェックを入れておくのをおすすめします)  

5\. 各ブラウザソースを読み込み，CUI右側の**GBC-S2Ws=>=Overlay**の`Connection Status`が**None**から**Connected**に変化すれば接続完了です．(TCP通信のため，こちらはコネクション確立が必要です)  

6\. すべての`Connection Status`が**Connected**になれば，準備完了です．観戦画面にいき，動作を確認しましょう！

# Note
- CUIの説明
  - `RL=>=GBC-S2Ws`はRLから送られてきたデータを表示しています
  - `GBC-S2Ws=>=Overlay`は本ソフトウェアからブラウザへの接続状況を表しています

# Author
* 作成者:[kazuryu](https://twitter.com/kazuryu_RL)
* 所属：なし

# Remarks
- 2023/5/5 RLCSように変更
- 2023/5/2 PraSのURLを更新
  
# License
Copyright (c) 2023 Kazuryu
