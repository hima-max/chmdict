#!/usr/bin/python
# -*- coding: utf-8 -*-
""" @package makedict.py
JSONからIME用辞書ファイルを生成するPythonスクリプト
動作にはPython3.6以降が必要
"""

import json
import argparse
import sys
import abc # 抽象基底クラスライブラリ
import platform

class DictMaker(object, metaclass=abc.ABCMeta):
    """ IME辞書生成を行う抽象クラス
    """
    def __init__(self, word_list, reading_list, japanese_reading_list, word_class, explanation):
        """ コンストラクタ
        word_list: 単語が含まれるリスト（同じ読み方、意味で複数の書き方が出来るケースを想定）
        reading_list: 読み方が含まれるリスト（同じ単語、意味で複数の読み方が出来るケースを想定）
        japanese_reading_list: 日本語の読み方が含まれるリスト（同じ単語、意味で複数の読み方が出来るケースを想定）
        word_class: 品詞
        explanation: 説明文（任意、無い場合はNoneが来るものと想定する）
        """
        self.word_list = word_list
        self.reading_list = reading_list
        self.japanese_reading_list = japanese_reading_list
        self.word_class = word_class
        self.explanation = explanation

    @abc.abstractmethod
    def print_dict(self):
        """ IME辞書文字列の出力を行う抽象メソッド
        """
        pass

class MSDictMaker(DictMaker):
    """ MS-IME用辞書生成クラス
    """
    def print_dict(self):
        """ 辞書文字列の出力
        """
        sys.stdout.buffer.write(b'\xFF\xFE') # UTF-16 Little Endian を示すBOM(Byte Order Mark)を付与
        reading_lists = [self.reading_list, self.japanese_reading_list]
        self.__print_reading_lists(reading_lists)

    def __print_reading_lists(self, reading_lists):
        """ 読み方の出力
        reading_lists: 読み方が含まれるリストのリスト
        """
        for word in self.word_list:
            for reading_list in reading_lists:
                self.__print_reading_list(word, reading_list)

    def __print_reading_list(self, word, reading_list):
        """ 読み方の出力
        word_list: 単語が含まれるリスト
        reading_list: 読み方が含まれるリスト
        """
        for reading in reading_list:
            output = "\t".join([reading, word, self.word_class])
            if self.explanation != None:
                output = output + "\t" + self.explanation + "\n"
            else:
                output = output + "\n"
            sys.stdout.buffer.write(output.encode('utf-16-le'))

class MozcDictMaker(DictMaker):
    """ Mozc用辞書生成クラス
    """
    def print_dict(self):
        """ 辞書文字列の出力
        """
        reading_lists = [self.reading_list, self.japanese_reading_list]
        self.__print_reading_lists(reading_lists)

    def __print_reading_lists(self, reading_lists):
        """ 読み方の出力
        reading_lists: 読み方が含まれるリストのリスト
        """
        for word in self.word_list:
            for reading_list in reading_lists:
                self.__print_reading_list(word, reading_list)

    def __print_reading_list(self, word, reading_list):
        """ 読み方の出力
        word_list: 単語が含まれるリスト
        reading_list: 読み方が含まれるリスト
        """
        for reading in reading_list:
            output = "\t".join([reading, word, self.word_class])
            if self.explanation != None:
                output = output + "\t" + self.explanation
            print(output)

class WordInfoContainer:
    """ 単語情報クラス
    """
    def __init__(self, json_file_path):
        """ コンストラクタ
        json_file: JSONファイルのパス

        受け取るJSONには以下のkeyが含まれていること
        word: 単語。必須key。valueは文字列または文字列配列であること。
        reading: 読み方。必須key。valueは文字列または文字列配列であること。
        japanese_reading: 日本語の読み方。必須key。valueは文字列または文字列配列であること。
        class: 品詞。必須key。valueは文字列であること。
        explanation: 説明。任意key。valueは文字列であること。
        """
        with open(json_file_path) as raw_file:
            all_json_info = json.load(raw_file)
        # ここからエラーチェック兼クラスメンバー変数初期化
        try: # JSONオブジェクトに必要なkeyが無い（KeyError）場合の例外をtry-exceptで処理
            # 単語の抽出
            if isinstance(all_json_info["word"], str):
                self.word_list = [all_json_info["word"],]
            elif isinstance(all_json_info["word"], list):
                self.word_list = all_json_info["word"]
            else: # "word"に対応するvalueが文字列またはリストでない場合はexceptで拾われない例外を起こしてスクリプトを停止させる
                raise Exception(f"The value of \"word\" must be \
                    string or list in {json_file_path}")
            # 読みの抽出
            if isinstance(all_json_info["reading"], str):
                self.reading_list = [all_json_info["reading"],]
            elif isinstance(all_json_info["reading"], list):
                self.reading_list = all_json_info["reading"]
            else: # "word"に対応するvalueが文字列またはリストでない場合はexceptで拾われない例外を起こしてスクリプトを停止させる
                raise Exception(f"The value of \"reading\" must be \
                    string or list in {json_file_path}")
            # 日本語の読みの抽出
            if isinstance(all_json_info["japanese_reading"], str):
                self.japanese_reading_list = [all_json_info["japanese_reading"],]
            elif isinstance(all_json_info["japanese_reading"], list):
                self.japanese_reading_list = all_json_info["japanese_reading"]
            else: # "word"に対応するvalueが文字列またはリストでない場合はexceptで拾われない例外を起こしてスクリプトを停止させる
                raise Exception(f"The value of \"japanese_reading\" must be \
                    string or list in {json_file_path}")
            # 品詞の抽出
            if isinstance(all_json_info["class"], str):
                self.word_class = all_json_info["class"]
            else: # "class"に対応するvalueが文字列でない場合はexceptで拾われない例外を起こしてスクリプトを停止させる
                raise Exception(f"The value of \"class\" must be string in {json_file_path}")
            # 説明の抽出
            if isinstance(all_json_info["explanation"], str):
                self.explanation = all_json_info["explanation"]
            else: # "explanation"に対応するvalueが文字列でない場合はexceptで拾われない例外を起こしてスクリプトを停止させる
                raise Exception(f"The value of \"explanation\" must be string in {json_file_path}")
        except KeyError as excpt:
            print(f"No \"{excpt.args[0]}\" key in {json_file_path}", file=sys.stderr)
            if excpt.args[0] == "explanation": # explanationは無くてもよいが、それ以外のケースは許可しない
                self.explanation = None
            else:
                print(f"Lacking \"{excpt.args[0]}\" key is not allowed", file=sys.stderr)
                sys.exit(-1)

class OptHandler:
    """ スクリプト実行時の引数情報クラス
    """
    def __init__(self):
        optparser = argparse.ArgumentParser(\
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='''このスクリプトはJSONからIME用辞書ファイルを生成します
リダイレクトでファイルに書き込んで下さい
入力出来るJSONのフォーマットは以下の通りです
----------------------------------------------------------------
{
    "word": ["単語1","単語2", ...],
    "reading": ["読み方1","読み方2", ...],
    "japanese_reading": ["読み方1","読み方2", ...],
    "class": "品詞",
    "explanation": "説明文"
}
----------------------------------------------------------------
wordに複数の書き方を指定できます（例：「灯明」と「燈明」、ともに読みは「とうみょう」）
reading, japanese_readingに複数の読み方を指定できます（例：「しじょう」と「いちば」、ともに漢字は「市場」）
''')
        optparser.add_argument('SOURCE_JSON', action='store', \
            nargs='+', type=str, default=None, help='入力するJSONファイル')
        optengine = optparser.add_mutually_exclusive_group() # optengineに登録したオプションは相互排他になる
        optengine.add_argument('--mozc', '-g', action='store_true', \
            help='Google日本語入力向けの辞書を出力（IMEの指定は必須、他のIME指定とは排他）')
        optengine.add_argument('--ms', '-m', action='store_true', \
            help='Microsoft IME向けの辞書を出力（IMEの指定は必須、他のIME指定とは排他）')
        self.opts = optparser.parse_args()
        if self.opts.mozc is not True and self.opts.ms is not True:
            print(f"Error: どのIME向けの辞書を出力するか指定してください", file=sys.stderr)
            sys.exit(1)

    def get_src_files(self):
        """ 引数として受け取ったファイル一覧を返す
        """
        file_list = list(set(self.opts.SOURCE_JSON))
        file_list.sort()
        return file_list

    def get_engine_type(self):
        """ どの辞書エンジンを指定したか返す
        """
        if self.opts.mozc is True:
            return "mozc"
        if self.opts.ms is True:
            return "ms"

if __name__ == '__main__':
    if int(platform.python_version_tuple()[0]) < 3 or int(platform.python_version_tuple()[1]) < 6:
        raise Exception("Python 3.6 or more is required.")
    OPTS = OptHandler()
    ChosenDict = {"mozc":MozcDictMaker, "ms":MSDictMaker}[OPTS.get_engine_type()]
    for json_file in OPTS.get_src_files():
        word_info = WordInfoContainer(json_file)
        word_dict = ChosenDict(word_info.word_list, word_info.reading_list, \
            word_info.japanese_reading_list, word_info.word_class, word_info.explanation)
        word_dict.print_dict()
