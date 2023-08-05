# **<font color="#0068B7">Roxy AI</font>** API

**<font color="#0068B7">Roxy AI</font>** の検査サーバを利用する Python 用の API です。

テストサンプルを実行するには以下の準備が必要となります。

1. Python仮想環境の構築
1. 検査サーバの起動
1. テストの実行
1. _Visual Studio Code_ 環境の整備

## Python仮想環境の構築と有効化

仮想環境の構築には仮想環境構築スクリプト `install_win.bat` を実行します。

仮想環境を有効にするには `env/Script/activate` を実行します。

詳細は Python の[公式マニュアル](https://docs.python.org/ja/3.7/library/venv.html) を参照ください。


## 検査サーバの起動

[検査サーバ](../inspect-server) の `README.md` を参照ください。

## テストの実行

### 単体テスト pytest のコマンドライン実行

コマンドライン上で仮想環境を有効にした状態で `pytest` を実行します。

実行例

```Shell
(env) c:\RoxyAI\roxy-ai-dev\roxyai-api>pytest
===================================================== test session starts =====================================================
platform win32 -- Python 3.7.7, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- c:\RoxyAI\roxy-ai-dev\python\roxyai-api\env\scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\RoxyAI\roxy-ai-dev\python\roxyai-api, inifile: pytest.ini, testpaths: tests
collected 34 items
(中略)
PASSED2020-07-02 17:08:37,240 INFO <2820> [connection]
---- close connection: 127.0.0.1:53739 -> 127.0.0.1:6945
2020-07-02 17:08:37,240 DEBUG <2820> [connection] release lock 1652236766600


================================================ 34 passed in 77.59s (0:01:17) ================================================ 
```

モデルデータを用意する必要があるので、初期状態ではテストは全て PASS にはなりません。


### サンプルファイルの実行

サンプルスクリプト `sample/inspect_sample.py` を実行します。

```shell
(env) C:\Users\zin\work\roxy-ai-dev\python\roxyai-api>python sample\inspect_sample.py
[NOK]: C:\Users\zin\work\roxy-ai-dev\python\roxyai-api\sample\product\Product1\fixed_model\master.jpg
[NOK]: C:\Users\zin\work\roxy-ai-dev\python\roxyai-api\sample\product\Product1\fixed_model\master.jpg
[NOK]: C:\Users\zin\work\roxy-ai-dev\python\roxyai-api\sample\product\Product1\fixed_model\master.jpg
[NOK]: C:\Users\zin\work\roxy-ai-dev\python\roxyai-api\sample\product\Product1\fixed_model\master.jpg
(Ctrl+Cで終了まで継続)
```

## Visual Studio Code 環境の整備

_Visual Studio Code (VSC)_ をインストールして、拡張機能 `Python` を有効にします。

[ファイル]-[ワークスペースを開く] で `.vscode\roxyai-api.code-workspace` を開きます。


### 単体テストの実行

[F1] で Discover Tests を選択すると単体テストアイコン（フラスコ）が左端のバーに追加されます。

アイコンをクリックすると Test Exploler が開き、各単体テストを自由に実行できるようになります。

単体テストスクリプトにエラーがあるとテストが表示されなくなります。
その場合には、下部の[出力]タブで [Python Test Log] を開き、エラーの内容を確認して修正します。

### サンプルプログラムの実行

サンプルプログラムのコード（ `sample\inspect_sample.py` など）を開いた状態で、デバグ実行の対象として `Python: Current File (roxyai-api)` を選択し、[F5] キーなどでデバグ実行することでサンプルを実行できます。

## ライセンス

本プロジェクト（**<font color="#0068B7">Roxy AI</font>** API） は _[APACHE LICENSE 2.0](http://www.apache.org/licenses/)_ に基づいて公開しています。（参考：[APL2.0日本語訳](https://ja.osdn.net/projects/opensource/wiki/licenses/Apache_License_2.0)）