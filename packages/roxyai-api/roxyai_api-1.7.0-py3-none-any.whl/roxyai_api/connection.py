# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
from __future__ import annotations
from typing import Optional
from socket import socket, AF_INET, SOCK_STREAM, timeout
from threading import Lock
from time import sleep

import logging.config

log = logging.getLogger(__name__)


class Connection():

    # クラス変数
    # 接続中のインスタンスを管理
    _dict = {}
    _host = None
    _port = None

    # サーバのデフォルト定義
    HOST = "127.0.0.1"
    PORT = 6945

    # 接続管理定数
    RETRY_INTERVAL = 0.2  # sec

    def __new__(cls, *args, **kwargs):
        # 同じサーバへの接続はインスタンスを使いまわす
        host = None
        port = None
        try:
            host = args[0]
            port = args[1]
        except IndexError:
            host = kwargs.get('host')
            port = kwargs.get('port')
        host = host or cls.HOST
        port = port or cls.PORT
        instance = cls._dict.get((host, port))
        if not instance:
            instance = super().__new__(cls)
            cls._dict[(host, port)] = instance
        return instance

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        retry: Optional[int] = None
    ):
        """ Inspect-Serverへの接続管理を行うクラス

        Args:
            host:
                (None, default):    クラスのデフォルト接続先を利用
                (str, option):      接続先ホストIPv4アドレス
            port:
                (None, default):    クラスのデフォルト接続ポートを利用
                (int, option):      接続先ホストTCPポート
            retry:                  サーバがビジーの場合に接続をリトライする回数
                (None, default):    リトライ回数制限無し
                (int, option):      指定リトライ回数
        """
        if self._host is None:
            # 初回のみ初期化する
            self._host = host or self.HOST
            self._port = port or self.PORT
            self._lock = Lock()
            self._sock = None
        self.retry = retry
        self.echo_check = True

    def __enter__(self) -> Connection:
        """ 接続開始 for with構文

        Returns:
            Connection:     接続した Connection のインスタンス
        """
        self.open(retry=self.retry)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ 接続完了 for with構文
        """
        self.close()

    def open(self, retry: Optional[int] = None):
        """ 接続開始

        Args:
            retry:                  サーバがビジーの場合に接続をリトライする回数
                (None, default):    リトライ回数制限無し
                (int, option):      指定リトライ回数
        """
        if not self._sock:
            # log.debug(f"wait lock {id(self)}")
            # self._lock.acquire()
            # log.debug(f"acuire lock {id(self)}")

            count = 0
            self._sock = socket(AF_INET, SOCK_STREAM)
            while True:
                try:
                    self._sock.connect((self._host, self._port))
                    if self.echo_check:
                        # Echoコマンドでの接続確認
                        # モジュールの依存関係のため実行時に読み込み
                        from .com_echo import EchoCommand
                        com = EchoCommand(b"", connection=self)
                        com.send(timeout=1.0)
                        while True:
                            try:
                                com.recv(timeout=1.0)
                                break
                            except RuntimeError as e:
                                # 期待しないデータは読み捨てる
                                log.warning(f"Unexpected data recv: {e}")
                    log.info(f"----- connected {self}")
                    break
                except (ConnectionError, timeout) as e:
                    self._sock.close()
                    count += 1
                    if (retry is None) or (count < retry):
                        log.info(f"{self} retry {count}/{retry} by {type(e)}")
                        sleep(self.RETRY_INTERVAL)
                        self._sock = socket(AF_INET, SOCK_STREAM)
                        continue
                    else:
                        log.warn(f"{self} refused by server by {type(e)}")
                        self._sock = None
                        return

    def close(self):
        """ 接続完了
        """
        if self._sock:
            self._sock.close()
            log.info(f"----- close {self}")

            self._sock = None

            # log.debug(f"release lock {id(self)}")
            # self._lock.release()

    def __str__(self):
        try:
            sockname = self._sock.getsockname()
            peername = self._sock.getpeername()
            return f"<Connection: {sockname[0]}:{sockname[1]} -> {peername[0]}:{peername[1]}>"
        except Exception:
            # ホスト名が取得できない場合は未接続
            return f"<Connection: unconnected -> {self._host}:{self._port}>"

    # 読み取り専用変数の定義
    @property
    def sock(self) -> socket:
        return self._sock
