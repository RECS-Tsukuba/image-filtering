import Tkinter
import main_frame

def main():
    root = Tkinter.Tk()
    width = 800
    height = 600

    f = main_frame.MainFrame(master=root, width=width, height=height)
    f.pack()
    f.mainloop()


if __name__ == '__main__':
    main()

