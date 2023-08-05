# (c) Roxy Corp. 2020-
# Roxy AI Coordinator
from __future__ import annotations
from typing import Optional
from enum import IntEnum
import numpy as np
import struct
import cv2
import traceback
from pathlib import Path

import logging.config
log = logging.getLogger(__name__)


class ImageFormat(IntEnum):
    """ イメージフォーマット値の定義クラス
    """
    RAW = 0x01
    JPEG = 0x02
    PNG = 0x03
    BMP = 0x04
    # 内部利用のフォーマット形式
    NDARRAY = 0xFF

    def __str__(self):
        return f'{self.name}(0x{self.value:02X})'

    @property
    def suffix(self) -> str:
        return IMG_FORMAT_SUF(self.value)

    @staticmethod
    def all_suffix(header: str = None) -> tuple:
        if header is None:
            return IMG_SUFFIX_LIST
        return tuple(header + s for s in IMG_SUFFIX_LIST)

    @classmethod
    def from_suffix(cls, suffix: str) -> ImageFormat:
        """ 拡張子からフォーマット値を取得
        Args:
            suffix (str)    拡張子文字列
        Returns:
            ImageFormat:    拡張子に対応するフォーマット値
            None:           拡張子が不正
        """
        suf = suffix.lower()
        if suf[0] != '.':
            suf = '.' + suf
        val = IMG_SUFFIX_FMT.get(suf)
        if val:
            return cls(val)
        return None


class ColorOrder(IntEnum):
    """ Rawイメージの色データバイト順の定義クラス
    """
    GRAY = 1
    BGR = 2
    RGB = 3
    BGRA = 4

    @property
    def depth(self):
        """ 色順序による色深度（ピクセルあたりバイト数）
        """
        if self == ColorOrder.GRAY:
            ret = 1
        elif self in (ColorOrder.BGR, ColorOrder.RGB):
            ret = 3
        elif self == ColorOrder.BGRA:
            ret = 4
        return ret

    def __str__(self):
        return f'{self.name}({self.value:d})'


# フォーマット変換の定義
IMG_FORMAT_SUF = {
    ImageFormat.RAW: '.bin',
    ImageFormat.JPEG: '.jpg',
    ImageFormat.PNG: '.png',
    ImageFormat.BMP: '.bmp',
}

IMG_SUFFIX_LIST = tuple(IMG_FORMAT_SUF.values())

IMG_SUFFIX_FMT = {
    **{v: ImageFormat(k) for k, v in IMG_FORMAT_SUF.items()},
    '.jpeg': ImageFormat(ImageFormat.JPEG),
}

# CVの変換用パラメータ定義
__JPEG_PARAMS = (cv2.IMWRITE_JPEG_QUALITY, 95)
__PNG_PARAMS = (cv2.IMWRITE_PNG_COMPRESSION, 1)


def _bin_to_ndarary(src):
    # 構造情報の設定
    width, height, order = struct.unpack('< H H B', src[:5])
    dt = np.dtype('uint8')
    dt = dt.newbyteorder('<')
    dst = np.frombuffer(src, dtype=dt, offset=5)
    depth = ColorOrder(order).depth
    if depth == 1:
        dst = dst.reshape((height, width))
    else:
        dst = dst.reshape((height, width, depth))
    return dst, ColorOrder(order)


def _image_to_ndarary(src):
    dt = np.dtype('uint8')
    dt = dt.newbyteorder('<')
    buf = np.frombuffer(src, dtype=dt, offset=0)
    dst = cv2.imdecode(buf, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_UNCHANGED)
    if len(dst.shape) == 2:
        order = ColorOrder.GRAY
    elif dst.shape[2] == 3:
        # CVは24bitをBGRの色順で保持
        order = ColorOrder.BGR
    elif dst.shape[2] == 4:
        # CVは32bitをBGRAの色順で保持
        order = ColorOrder.BGRA
    return dst, ColorOrder(order)


def _ndarary_to_bin(src, order: ColorOrder) -> bytes:
    shape = (src.shape[1], src.shape[0], order)
    dst = struct.pack('< H H B', *shape)
    dst += src.tobytes()
    return dst


def _ndarary_to_jpeg(src, order: ColorOrder) -> bytes:
    if order == ColorOrder.RGB:
        # CV2の色順に変換
        src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    ret, dst = cv2.imencode('.jpg', src, params=__JPEG_PARAMS)
    if not ret:
        RuntimeWarning('imencode for jpg failed')
    return bytes(np.frombuffer(dst, dtype=np.uint8))


def _ndarary_to_png(src, order: ColorOrder) -> bytes:
    if order == ColorOrder.RGB:
        # CV2の色順に変換
        src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    ret, dst = cv2.imencode('.png', src, params=__PNG_PARAMS)
    if not ret:
        RuntimeWarning('imencode for png failed')
    return bytes(np.frombuffer(dst, dtype=np.uint8))


def _ndarary_to_bmp(src, order: ColorOrder) -> bytes:
    if order == ColorOrder.RGB:
        # CV2の色順に変換
        src = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
    ret, dst = cv2.imencode('.bmp', src)
    if not ret:
        RuntimeWarning('imencode for bmp failed')
    return bytes(np.frombuffer(dst, dtype=np.uint8))


class InspectImage():
    """ 検査に利用するイメージデータのキャッシュ機能付き管理クラス
    """
    DECODER = {
        ImageFormat.RAW: _bin_to_ndarary,
        ImageFormat.JPEG: _image_to_ndarary,
        ImageFormat.PNG: _image_to_ndarary,
        ImageFormat.BMP: _image_to_ndarary,
    }

    ENCODER = {
        ImageFormat.RAW: _ndarary_to_bin,
        ImageFormat.JPEG: _ndarary_to_jpeg,
        ImageFormat.PNG: _ndarary_to_png,
        ImageFormat.BMP: _ndarary_to_bmp,
    }

    def __init__(
        self,
        fmt: ImageFormat,
        data: bytes,
        path: Optional[Path] = None,
        parent: Optional[InspectImage] = None,
        zoom: Optional[float] = 1.0,
        order: ColorOrder = None,
        fnc_buf_release: Optional[callable] = None,
    ):
        self._org_fmt = ImageFormat(fmt)
        self._data = {fmt: data}
        self._fnc_buf_release = fnc_buf_release
        self._path = path
        self._parent = parent
        self._zoom = zoom
        self._keep_count = 1
        if order is None:
            if fmt == ImageFormat.NDARRAY:
                if len(data.shape) == 2:
                    order = ColorOrder.GRAY
                elif data.shape[2] == 3:
                    # CVは24bitをBGRの色順で保持
                    order = ColorOrder.BGR
                elif data.shape[2] == 4:
                    # CVは32bitをBGRAの色順で保持
                    order = ColorOrder.BGRA
        self._order = order

    @classmethod
    def load(cls, path) -> InspectImage:
        """ ファイルから画像を読み込む
        """
        instance = None
        imgfile = Path(path)
        if imgfile.exists():
            fmt = IMG_SUFFIX_FMT.get(imgfile.suffix)
            if fmt:
                data = imgfile.read_bytes()
                instance = cls(fmt, data, imgfile)
        return instance

    def save(self, path) -> bool:
        """ ファイルに画像を書き込む
        Returns:
            True:   書き込み成功
            False:  書き込み失敗
        Note:
            ファイル名の拡張子で画像フォーマットを決定する
        """
        imgfile = Path(path)
        fmt = IMG_SUFFIX_FMT.get(imgfile.suffix)
        if fmt:
            data = self.get_image(fmt)
            if data:
                imgfile.write_bytes(data)
                return True
        return False

    def get_tf_image(self) -> np.ndarray:
        """ TensorFlow用のデータ取得
        """
        img = self.get_image()
        # ndarrayがTF形式RGB(24bit)でなければ変換
        if self._order == ColorOrder.GRAY:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif self._order == ColorOrder.BGR:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif self._order == ColorOrder.BGRA:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        return img

    def get_image(
        self, fmt: ImageFormat = ImageFormat.NDARRAY
    ) -> Optional[np.ndarray, bytes]:
        """ 指定フォーマトの画像データを取得
        """
        img = self._data.get(fmt)
        if img is not None:
            # 対象フォーマットがキャッシュにあればそれを返す
            return img
        # 無ければ画像変換してそれを返す
        self.__convert(fmt)
        img = self._data.get(fmt)
        return img

    def get_size(self, fmt: ImageFormat = None) -> int:
        """ 指定フォーマットのデータサイズを取得
        """
        fmt = fmt or self._org_fmt
        fmt = ImageFormat(fmt)
        img = self.get_image(fmt)
        if img is None:
            return None
        if fmt == ImageFormat.NDARRAY:
            return img.size
        else:
            return len(img)

    def __convert(self, fmt: ImageFormat = ImageFormat.NDARRAY):
        """ 画像フォーマット変換
        """
        if self._data.get(fmt) is not None:
            # 変換済みなら何もしない
            return

        if self._order is None:
            # 基準データ(ndarray)の作成
            src = self._data[self._org_fmt]
            converter = self.DECODER[self._org_fmt]
            try:
                dst, order = converter(src)
            except Exception as e:
                log.warning(traceback.format_exc())
                raise ImageConvertionFailed(self._org_fmt, ImageFormat.NDARRAY, None, e)
            self._data[ImageFormat.NDARRAY] = dst
            self._order = order

        if fmt != ImageFormat.NDARRAY:
            # 基準データ(ndarray)から変換先の画像データの作成
            src = self._data[ImageFormat.NDARRAY]
            converter = self.ENCODER[fmt]
            try:
                dst = converter(src, self._order)
            except Exception as e:
                log.warning(traceback.format_exc())
                raise ImageConvertionFailed(ImageFormat.NDARRAY, fmt, self._order, e)
            self._data[fmt] = dst

    def keep(self):
        """ 画像データを保持する(TBD)
        """
        self._keep_count += 1

    def release(self):
        """ 画像データを全て破棄する(TBD)
        """
        self._keep_count -= 1
        if self._keep_count > 0:
            # まだ保持している処理があるので破棄しない
            return
        self._data.clear()
        self._org_fmt = None
        if self._fnc_buf_release:
            # バッファの解放コールバックの呼び出し
            try:
                self._fnc_buf_release()
            except Exception as e:
                log.warning(
                    f"{e}: in callback for release image buffer: "
                    f"{self._fnc_buf_release()}"
                )
            self._fnc_buf_release = None

    def __str__(self):
        string = (
            f'org_image[{self._org_fmt.name}], '
            'cached '
        )
        cached = [
            f'{ImageFormat(fmt).name}: '
            f'{len(self._data.get(fmt)):,d} bytes'
            for fmt in IMG_FORMAT_SUF
            if type(self._data.get(fmt)) is bytes
        ]
        if self._order:
            # 基準データ(ndarray)作成済み
            raw = self._data.get(ImageFormat.NDARRAY)
            cached.append(
                f'{ImageFormat.NDARRAY.name}: '
                f'{self._order.name} '
                f'{raw.size:,d} bytes'
            )
        string += ', '.join(cached)
        return string

    # 読み取り専用のパラメータアクセス定義
    @property
    def format(self) -> int:
        return self._org_fmt

    @property
    def data(self) -> int:
        return self._data

    @property
    def path(self) -> Path:
        return self._path

    @property
    def parent(self) -> InspectImage:
        return self._parent

    @property
    def zoom(self) -> float:
        return self._zoom

    @property
    def order(self) -> ColorOrder:
        return self._order


class ImageConvertionFailed(RuntimeWarning):
    """ 画像変換エラー
    """
    def __init__(self, src_fmt, dst_fmt, order, exception):
        self.src_fmt = ImageFormat(src_fmt)
        self.dst_fmt = ImageFormat(dst_fmt)
        self.order = ColorOrder(order)
        self.exception = exception

    def __str__(self):
        return (
            f'image conversion failed '
            f'from [{self.src_fmt.name}] '
            f'to [{self.dst_fmt.name}] '
            f'color order: {self.order.name}'
        )
