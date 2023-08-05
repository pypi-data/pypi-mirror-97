# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
from typing import Union
import json

from .com_definition import CommandCode
from .com_base import BaseCommand


class InitializeCommand(BaseCommand):

    _CODE = CommandCode.INITIALIZE
    send_json = ''

    def __init__(
        self,
        send_json: str = None,
        product: str = None,
        model_list: Union[list, tuple] = [],
        connection=None,
    ):
        """ Initialize コマンド制御

        Args:
            send_json (str, option):            初期設定をJSONデータで定義
            product (str, option):              初期設定のproduct名（設定パス）
            model_list (list, option):          初期設定のモデル名リスト
            connection (Connection, option):    通信対象のTCP接続

        Note:
            JSONデータか、product, model_list指定の何れかを選択する。

        Example:
            code-block:: markdown
            ```python
            from roxyai-api import InitializeCommand

            com = InitializeCommand(product='ProductName', model_list=['ModelName'])
            com.run()
            if com.status.is_error_reply:
                raise RuntimeError(str(com))
            ```
        """
        super().__init__(connection)
        # 要求データの設定
        if send_json:
            self.product = None
            self.model_list = []
            self.send_json = send_json
        else:
            self.product = product
            self.model_list = model_list
            self.__encode_json()
        self.data = self.send_json.encode('utf-8')

    def append_model(self, model_name: str, group_name: str = None):
        """ モデルを追加する（オプションで画像グループ指定を行う）
        """
        if self.product is None:
            # jsonコードの未解釈の場合は一度解釈する
            dic = json.loads(self.send_json, encoding='utf-8')
            self.product = dic['Product']
            self.model_list = dic['ModelList']

        if group_name:
            self.model_list.append((str(model_name), str(group_name)))
        else:
            self.model_list.append(str(model_name))
        self.__encode_json()

    def __encode_json(self) -> str:
        model_list = []
        for model in self.model_list:
            if type(model) in (list, tuple):
                if len(model) >= 2:
                    model = [str(model[0]), str(model[1])]
                else:
                    model = str(model[0])
            else:
                model = str(model)
            model_list.append(model)
        dic = {
            'Product': str(self.product),
            'ModelList': model_list
        }
        self.send_json = json.dumps(dic, ensure_ascii=False)

    def __str__(self):
        string = (
            f'{super().__str__()} '
            f'SendJson: {self.send_json} '
            f'{len(self.send_json)} bytes ->'
        )
        return string
