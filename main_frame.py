# coding: utf-8

import Tkinter
import tkFileDialog
import controller
import functools

class MainFrame(Tkinter.Frame):
    """メインフレーム。

     オリジナルの画像とフィルタされた画像を表示する。
    """
    def __init__(
        self, master=None, controller=controller.Controller(), width=800, height=600):
        """コンストラクタ。

         Args:
            master: 親クラス
            width: 画像幅
            height: 画像の高さ
        """
        # スーパークラスのコンストラクタの呼び出し
        Tkinter.Frame.__init__(self, master)

        self.__controller=controller

        # 初期化
        self.__initialize_config()
        self.__initialize_menu()
        self.__initialize_canvas(width, height)
        # メインフレームの設定
        self.master.config(
            menu=self.__menu, width=width*2, height=height, bg='black')
        self.__canvas.pack(side=Tkinter.LEFT)

    def disable_config_menu(self):
        self.__set_config_menu_state(Tkinter.DISABLED)

    def disable_control(self):
        self.__set_control_menu_state(Tkinter.DISABLED, Tkinter.NORMAL)

    def enable_config_menu(self):
        self.__set_config_menu_state(Tkinter.NORMAL)

    def enable_control(self):
        self.__set_control_menu_state(Tkinter.NORMAL, Tkinter.DISABLED)

    def get_bitfile_name(self):
        """ビットファイル名を取得する。
        """
        return tkFileDialog.askopenfilename(
            parent=self, filetypes=[('ビットファイル','*.bit')])

    def get_config(self):
        """フィルタリングの設定を取得する。
        """
        return (self.__config[0].get(), self.__config[1].get())

    def update_image(self, original, filtered):
        """画像をセットし、画面を更新する

         Args:
            original: カメラからのオリジナル画像
            filtered: フィルタがかけられた画像
         TODO(鈴木):まだ仮設置
        """
        self.__original_image = original
        self.__filtered_image = filtered
        self.__canvas.itemconfigure(
            self.__original_image_item, image=self.__original_image)
        self.__canvas.itemconfigure(
            self.__filtered_image_item, image=self.__filtered_image)
        self.update()

    def __initialize_config(self):
        """メンバの宣言、初期化を行う。
        """
        self.__config = (
            Tkinter.IntVar(value=100), Tkinter.BooleanVar(value=False))

    def __initialize_canvas(self, width, height):
        """キャンバス、キャンバス内の画像オブジェクト、画像を作成する。

         Args:
            width: 画面幅
            height: 画面の高さ
        """
        # 画像を表示するキャンバス
        # TODO(鈴木):キャンバスと画面を区別するため、背景色を白に設定
        self.__canvas = Tkinter.Canvas(
            self, width=width*2, height=height, bg='white')
        # 画像
        # TODO(鈴木):キャンバスがきちんと配置されているかどうか、確認のため
        #            サンプルを読み込む
        self.__original_image = Tkinter.PhotoImage(file='sample.gif')
#        self.__original_image = Tkinter.PhotoImage()
        self.__filtered_image = Tkinter.PhotoImage()

        self.__original_image_item = self.__canvas.create_image(
            0, 0, anchor=Tkinter.NW, image=self.__original_image)
        self.__filtered_image_item = self.__canvas.create_image(
            width, 0, anchor=Tkinter.NW, image=self.__filtered_image)

    def __initialize_menu(self, master=None):
        """メニューを作成。

         Args:
            master: 親オブジェクト
        """
        # メニュー
        self.__menu = Tkinter.Menu(self, tearoff=0)
        # カスケードを追加
        self.__main_cascade = Tkinter.Menu(self.__menu, tearoff=False)
        self.__frequency_cascade = Tkinter.Menu(self.__menu, tearoff=False)
        self.__colored_flag_cascade = Tkinter.Menu(self.__menu, tearoff=False)
        self.__menu.add_cascade(label='メニュー', under=0, menu=self.__main_cascade)
        self.__menu.add_cascade(
            label='動作周波数', under=0, menu=self.__frequency_cascade)
        self.__menu.add_cascade(
            label='元画像の色', under=0, menu=self.__colored_flag_cascade)
        # メインメニューにアイテムを追加
        self.__main_cascade.add_command(
            label='開始', under=0,
            command=functools.partial(self.__controller.start_filtering, self))
        self.__main_cascade.add_command(
            label='停止', under=3, state=Tkinter.DISABLED,
            command=functools.partial(self.__controller.stop_filtering, self))
        self.__main_cascade.add_command(
            label='終了', under=0, command=self.quit)
        # 動作周波数メニューにアイテムを追加
        self.__frequency_cascade.add_radiobutton(
            label='100 MHz', variable=self.__config[0], value=100)
        self.__frequency_cascade.add_radiobutton(
            label='50 MHz', variable=self.__config[0], value=50)
        self.__frequency_cascade.add_radiobutton(
            label='25 MHz', variable=self.__config[0], value=25)
        # カラーか白黒を切り替えるメニューを追加
        self.__colored_flag_cascade.add_radiobutton(
            label='白黒', variable=self.__config[1], value=False)
        self.__colored_flag_cascade.add_radiobutton(
            label='カラー', variable=self.__config[1], value=True)

        # TODO(鈴木): テストメニューの生成。削除予定
        test_cascade = Tkinter.Menu(self.__menu, tearoff=False)
        self.__menu.add_cascade(label='test', under=0, menu=test_cascade)
        test_cascade.add_command(
            label='disable' ,under=0, command=self.disable_config_menu)
        test_cascade.add_command(
            label='enable' ,under=0, command=self.enable_config_menu)
        test_cascade.add_command(
            label='show___config' ,under=0, command=self.__show_confg)

    def __set_control_menu_state(self, state_start, state_stop):
        self.__main_cascade.entryconfig(index=0, state=state_start)
        self.__main_cascade.entryconfig(index=1, state=state_stop)

    def __set_config_menu_state(self, state):
        self.__frequency_cascade.entryconfig(index=0, state=state)
        self.__frequency_cascade.entryconfig(index=1, state=state)
        self.__frequency_cascade.entryconfig(index=2, state=state)

        self.__colored_flag_cascade.entryconfig(index=0, state=state)
        self.__colored_flag_cascade.entryconfig(index=1, state=state)

    def __show_confg(self):
        print "%d MHz, %r" % (
            self.__config[0].get(), self.__config[1].get()
        )

