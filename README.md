# chmdict
中国麻雀役の辞書とPython製辞書作成スクリプト

## Requirement

* Python 3.6以上が動作するコマンドライン環境

## Usage

以下のコマンドにより`output.txt`という辞書データが得られる
```
python ./makedict.py [オプション] [辞書データ] > output.txt
```

* --mozc, -g
Mozc、Google日本語入力向けの辞書を出力（-ms, -mとは排他）
* --ms, -m
Microsoft IME向けの辞書を出力（--mozc, -gとは排他）
* --without-japanese, -s
日本語の読み方がない辞書を出力

例として日本語読みを含まないMozc用の辞書は以下のコマンドで得られる
```
python ./makedict.py -g -s src/*.json > mozc.txt
```


## Components

* src
単語と読み方の対応付けが記述されたJSONファイルからなる辞書データ
* makedict.py
辞書作成スクリプト本体
