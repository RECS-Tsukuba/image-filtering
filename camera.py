# coding: utf-8

import Image
import ImageTk
import cv

class Capture(object):
    def __init__(self, width, height, index=-1):
        """
         Args:
            width: 画像幅
            height: 画像の高さ
            index: カメラのインデックス
        """
        self.__capture = cv.CaptureFromCAM(index)
        cv.SetCaptureProperty(self.__capture, cv.CV_CAP_PROP_FRAME_WIDTH, width)
        cv.SetCaptureProperty(
            self.__capture, cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        # cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FPS, 15)

        self.__resized_frame = cv.CreateImage(
            (width, height) , cv.IPL_DEPTH_8U, 3)
        self.__grayscaled_frame = cv.CreateImage(
            (width, height) , cv.IPL_DEPTH_8U, 1)

    def get_frame(self):
        return self.__IPLImage2TkImage(self.__get_resized_frame())

    def get_grayscale_frame(self):
        return self.__IPLImage2TkImage(
            self.__change_to_grayscaled(
                src=self.__get_resized_frame(), dst=self.__grayscaled_frame)
        )

    def __get_resized_frame(self):
        return self.__resize(
            src=cv.QueryFrame(self.__capture), dst=self.__resized_frame)

    def __change_to_grayscaled(self, src, dst):
        cv.CvtColor(src, dst, cv.CV_RGB2GRAY)
        return dst

    def __IPLImage2TkImage(self, iplimage):
        """IPLImageをTk用に変換する。

         参考:
          http://peta.okechan.net/blog/archives/1116

         Args:
            iplimage: OpenCV形式(IPLImage)の画像
         Returns:
            Tk形式(Image)の画像
        """
        assert iplimage.depth == 8 and iplimage.nChannels in [1, 3]
        if iplimage.nChannels == 3:
            image = Image.fromstring(
                'RGB', cv.GetSize(iplimage), iplimage.tostring(),
                'raw', 'BGR', iplimage.width * 3, 0)
        elif iplimage.nChannels == 1:
            image = Image.fromstring(
                'L', cv.GetSize(iplimage), iplimage.tostring())
        return ImageTk.PhotoImage(image)

    def __resize(self, dst, src):
        """画像をリサイズする。

         Args:
            src: 入力画像。
            dst: 出力画像。事前に領域を確保する必要がある。
         Returns:
            リサイズされた画像
        """
        cv.Resize(src, dst)
        return dst

