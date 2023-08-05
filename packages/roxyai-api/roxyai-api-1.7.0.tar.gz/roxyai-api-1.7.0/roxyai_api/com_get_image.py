# (c) Roxy Corp. 2020-
# Roxy AI Analyze-Server API
import struct

from .com_definition import CommandCode, CommandStatus
from .com_base import BaseCommand, HEADER_SIZE


class GetImageCommand(BaseCommand):

    _CODE = CommandCode.GET_IMAGE
    PROB_OFFSET = 14 - HEADER_SIZE

    def __init__(
        self,
        inspect_id: int,
        connection=None,
    ):
        """ GetImage コマンド制御

        Args:
            inspect_id (int):                   取得対象の検査番号
            connection (Connection, option):    通信対象のTCP接続
        """
        super().__init__(connection)
        self.inspect_id = inspect_id
        self.data = struct.pack(f'< Q', inspect_id)

        self.data_format = None
        self.image_data = None

    def _decode_reply(self, reply: bytes):
        """ Inspect コマンドの応答内容確認

        Args:
            reply (bytes):      受信応答データ（ヘッダ以外）
        """
        self.data_format, = struct.unpack('< B', reply)
        image_data = b''
        size = self.rest_size
        if size > 0:
            # 画像データの受信
            while len(image_data) < size:
                image_data += self.connection.sock.recv(size - len(image_data))
        self.image_data = image_data

    def __str__(self):
        string = (
            f'{super().__str__()} '
            f'InspectID: {self.inspect_id}(=0x{self.inspect_id:016X}) -> '
        )
        if self.is_received_ack:
            string += (
                f'DataFromat: 0x{self.data_format:02X}, '
                f'ImageData: {len(self.image_data):,d} bytes '
                f'({self.process_time} ms)'
            )
        return string
