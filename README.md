# chmdict
中国麻雀役の辞書とPython製辞書作成スクリプト

## Requirement
 
* GNU Make
* Python 3.6以上

## Usage

* make all  
辞書の生成
* make clean  
辞書の削除

## Components

* src  
単語と読み方の対応付けが記述されたJSONファイルを含むディレクトリ
* products  
生成された辞書ファイルが置かれるディレクトリ  
mozc.txtはGoogle日本語入力、ms.txtはMicrosoft IME向け
* makedict.py  
辞書作成スクリプト本体
* makefile  
ビルドルール