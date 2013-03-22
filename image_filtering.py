# coding: utf-8

import threading
import time
import camera

class ImageFiltering(threading.Thread):
    def __init__(self, observer, capture):
        threading.Thread.__init__(self)

        self.__observer = observer
        self.__capture = capture

        self.__is_running = True
        self.__flag_condition = threading.Condition()

    def run(self):
        """
         オーバーライド
        """
        while True:
            with self.__flag_condition:
                if not self.__is_running:
                    print "a thread was stopped"
                    return
            time.sleep(0.5)
#            print "a thread is running"
            original = self.__capture.get_frame()
            filtered = self.__capture.get_grayscale_frame()
            self.__observer.update_image(original, filtered)

    def stop(self):
        with self.__flag_condition:
            self.__is_running = False

