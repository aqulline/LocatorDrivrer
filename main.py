import time

from kivy.properties import DictProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.base import EventLoop
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy import utils, platform
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from plyer import gps

from database import Database as DT

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = (412, 732)


class Emergency(MDBoxLayout):
    pass


class Tab(MDBoxLayout, MDTabsBase):
    pass


class MainApp(MDApp):
    bus_stops = DictProperty(DT.bus_list(DT()))
    item = BooleanProperty(False)
    current_loc = StringProperty("Stand Home")
    prev_loc = StringProperty("Stand")
    size_x, size_y = Window.size

    # MAP
    lat, lon = NumericProperty(-6.8059668), NumericProperty(39.2243981)

    # LOCATION
    region = StringProperty("------------------")
    city = StringProperty("------------------")
    city_district = StringProperty("------------------")
    sub_ward = StringProperty("------------------")
    sub_urb = StringProperty("------------------")
    road = StringProperty("------------------")

    # screen
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    def on_start(self):
        self.add_bus()
        self.keyboard_hooker()
        self.gps_init()

    def keyboard_hooker(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    def category_sheet(self, data):
        bottom_sheet_menu = MDListBottomSheet()
        vimbweta = data
        count = 1
        for i in vimbweta.items():
            bottom_sheet_menu.add_item(
                i[0],
                lambda x, y=i[0], z=i[1]: self.callback_for_menu_items(y, z),
                icon=i[1],
            )
            count += 1
        bottom_sheet_menu.radius_from = 'top'
        bottom_sheet_menu.open()

    @mainthread
    def callback_for_menu_items(self, y, z):
        self.prev_loc = self.current_loc
        self.current_loc = y
        try:
            DT.current_pos(DT(), self.prev_loc, self.current_loc)
        except:
            toast("Network error!")

    def add_bus(self):

        self.root.ids.stops.data = {}
        if not self.bus_stops:
            self.root.ids.stops.data.append(
                {
                    "viewclass": "BusInfo",
                    "name": "No Cars Yet!",
                    "route": "",
                    "lcn": "",
                    "price": "",
                    "seats": ""
                }
            )
        else:
            for i, y in self.bus_stops.items():
                self.root.ids.stops.data.append(
                    {
                        "viewclass": "Emergency",
                        "name": i,
                        "icon": y,
                        "phone": "",
                        "fsize": "16",
                        "pos_x": .27,
                        "pos_y": .5,
                        "isize": "30sp",
                        "call": "delete",
                    }
                )

    @mainthread
    def delete_location(self, name):
        DT.delete_stop(DT(), name)
        self.bus_stops = DT.bus_list(DT())
        self.add_bus()

    @mainthread
    def add_location(self, name):
        DT.new_stop(DT(), name)
        self.bus_stops = DT.bus_list(DT())
        self.add_bus()

    def fetch_location(self):

        DT.data_loc(DT(), self.lat, self.lon)



    def add_screen(self):
        self.screen_capture("add_stop")
        self.item = True

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        self.item = False
        print(self.item)
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)


    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION, Permission.CALL_PHONE], callback)

    @mainthread
    def gps_init(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)

        except NotImplementedError:
            import traceback
            traceback.print_exc()
            gps_status = 'GPS is not implemented for your platform'

            return gps_status

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

    @mainthread
    def start(self, minTime=1000, minDistance=1):
        gps.start(minTime, minDistance)
        toast("GPS Running...")

    @mainthread
    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

        toast("geting location.....")

        self.lat = float(kwargs["lat"])
        self.lon = float(kwargs["lon"])
        self.fetch_location()

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def build(self):
        pass


MainApp().run()
