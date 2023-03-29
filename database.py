import json
from firebase_db import FireBase as FB
from beem import sms as SM


class Database:
    data_file_name = ""

    def write(self, data):
        with open(self.data_file_name, "w") as file:
            initial_data = json.dumps(data, indent=4)
            file.write(initial_data)
            FB.add_Shedules(FB(), data, "T657")

    def load(self):
        with open(self.data_file_name, "r") as file:
            initial_data = json.load(file)
        return initial_data

    def current_pos(self, prev, current):
        idd = "T657"
        FB.prev_current(FB(), idd, prev, current)
        self.send_sms(current)

    def send_sms(self, current):
        num = FB.get_number(FB(), current)

        if num:
            for i in num:
                SM.send_sms(i, f"Marangu imefika {current} kwa sasa")
    def bus_list(self):
        with open("database/stops.json") as expenses:
            exp = json.load(expenses)

            return exp

    def data_loc(self, lan, lon):
        idd = "T657"
        FB.track_loc(FB(), idd, lan, lon)

    def delete_stop(self, name):
        self.data_file_name = "database/stops.json"
        initial_data = self.load()
        initial_data.pop(name)
        self.write(initial_data)

    def new_stop(self, name):
        self.data_file_name = "database/stops.json"
        data = {name: "google-maps"}
        self.update_data(data)

    def update_data(self, data):
        initial_data = self.load()
        final_data = data
        initial_data.update(final_data)
        self.write(initial_data)
