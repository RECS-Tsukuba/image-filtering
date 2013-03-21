# coding: utf-8

import Tkinter
import tkFileDialog

def _print_stab():
    print "This is a stab."

class MainFrame(Tkinter.Frame):
    """
     Main frame class.
    """
#    def __init__(self, *args, **kwargs):
    def __init__(self, master=None, width=800, height=600):
        """
         コンストラクタ。
        """
        # スーパークラスのコンストラクタの呼び出し
        Tkinter.Frame.__init__(self, master)

        self.__initialize(width, height)

        # メインフレームの設定
        self.master.__config(menu=self.__menu, bg='black')
        self.pack()

        self.__add_menu_items(master)

        self.__original_canvas.pack(side=Tkinter.LEFT)
        self.__filtered_canvas.pack(side=Tkinter.LEFT)

        # TODO(鈴木):きちんとキャンバスが配置されているかどうかのチェック
        self.__original_image = Tkinter.PhotoImage(file='sample.gif')
        self.__original_canvas.create_image(
            0, 0, anchor=Tkinter.NW, image=self.__original_image)


    def __initialize(self, width, height):
        """
         メンバの宣言、初期化。
        """
        # メニュー
        self.__menu = Tkinter.Menu(self, tearoff=0)
        # 画像を表示するキャンバス
        self.__original_canvas = Tkinter.Canvas(
            self, width=width, height=height, bg='red')
        self.__filtered_canvas = Tkinter.Canvas(
            self, width=width, height=height, bg='white')

        self.__config = (
            Tkinter.IntVar(value=100), Tkinter.BooleanVar(value=False))

    def __add_menu_items(self, master=None):
        """
         メニューへアイテムを追加。
        """
        # カスケードを追加
        main_cascade = Tkinter.Menu(self.__menu, tearoff=False)
        self.__frequency_cascade = Tkinter.Menu(self.__menu, tearoff=False)
        self.__colored_flag_cascade = Tkinter.Menu(self.__menu, tearoff=False)
        self.__menu.add_cascade(label='メニュー', under=0, menu=main_cascade)
        self.__menu.add_cascade(
            label='動作周波数', under=0, menu=self.__frequency_cascade)
        self.__menu.add_cascade(
            label='色', under=0, menu=self.__colored_flag_cascade)
        # メインメニューにアイテムを追加
        main_cascade.add_command(label='開始', under=0, command=_print_stab)
        main_cascade.add_command(label='停止', under=3, command=_print_stab)
        main_cascade.add_command(label='終了', under=0, command=self.quit)
        # 動作周波数メニューにアイテムを追加
        self.__frequency_cascade.add_radiobutton(
            label='100 MHz', variable=self.__config[0], value=100)
        self.__frequency_cascade.add_radiobutton(
            label='50 MHz', variable=self.__config[0], value=50)
        self.__frequency_cascade.add_radiobutton(
            label='25 MHz', variable=self.__config[0], value=25)
        # 
        self.__colored_flag_cascade.add_radiobutton(
            label='白黒', variable=self.__config[1], value=False)
        self.__colored_flag_cascade.add_radiobutton(
            label='カラー', variable=self.__config[1], value=True)

        # TODO(鈴木): テストメニューを追加。削除予定
        test_cascade = Tkinter.Menu(self.__menu, tearoff=False)
        self.__menu.add_cascade(label='test', under=0, menu=test_cascade)
        test_cascade.add_command(
            label='disable' ,under=0, command=self.disable_frequency_cascade)
        test_cascade.add_command(
            label='enable' ,under=0, command=self.enable_freqency_cascade)
        test_cascade.add_command(
            label='show___config' ,under=0, command=self.__show_confg)

    def update_image(self, original, filtered):
        """
         Args:
            original: カメラからのオリジナル画像
            filtered: フィルタがかけられた画像
        """
        self.__original_image = original
        self.__filtered_image = filtered
        self.update()

    def get_bitfile_name(self):
        return tkFileDialog.askopenfilename(
            parent=self, filetypes=[('ビットファイル','*.bit')])

    def get_config(self):
        return (self.__config[0].get(), self.__config[1].get())

    def disable_frequency_cascade(self):
        self.__frequency_cascade.entry__config(index=0, state=Tkinter.DISABLED)
        self.__frequency_cascade.entry__config(index=1, state=Tkinter.DISABLED)
        self.__frequency_cascade.entry__config(index=2, state=Tkinter.DISABLED)

    def enable_freqency_cascade(self):
        self.__frequency_cascade.entry__config(index=0, state=Tkinter.NORMAL)
        self.__frequency_cascade.entry__config(index=1, state=Tkinter.NORMAL)
        self.__frequency_cascade.entry__config(index=2, state=Tkinter.NORMAL)

    def __show_confg(self):
        print "%d MHz, %r" % (
            self.__config[0].get(), self.__config[1].get()
        )

