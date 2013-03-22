# coding: utf-8
#import camera
#import image_filtering

class Controller(object):
    def __init__(self):
        self.__capture = None
        self.__image_filtering = None

    def start_filtering(self, observer):
#        self.__capture = camera.Capture(
#            width=observer.winfo_width()/2, height=observer.winfo_height())
#
#        self.__image_filtering.ImageFiltering(observer, capture)
#        self.__image_filtering.start()
        observer.disable_control()
        observer.disable_config_menu()

        print "start filtering"

    def stop_filtering(self, observer):
#        self.__image_filtering.stop()

        observer.enable_control()
        observer.enable_config_menu()
        print "stop filtering"

