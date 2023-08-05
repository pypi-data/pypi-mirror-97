# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
from .com_definition import CommandCode
from .com_base import BaseCommand


class TerminateCommand(BaseCommand):
    _CODE = CommandCode.TERMINATE

    def __init__(self, connection=None):
        """ Terminate コマンド制御

        Args:
            connection (Connection, option):    通信対象のTCP接続
        """
        super().__init__(connection)
        # 要求データの設定
        self.data = b''
