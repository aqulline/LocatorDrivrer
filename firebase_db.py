class FireBase:

    def register_admin(self, busid, name):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('LocatorDriver').child("BusId").child(busid).child("Details")
                ref.set(
                    {
                        "car_name": name,
                        "car_plate_number": busid
                    }
                )

    def add_Shedules(self, data, phone):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('LocatorDriver').child("BusId").child(phone).child("BusStops")
                ref.set(data)

    def prev_current(self, phone, prev, current):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('LocatorDriver').child("BusId").child(phone).child("current_location")
                ref.set({
                    "prev": prev,
                    "current": current,
                })

    def track_loc(self, phone, lan, lon):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('LocatorDriver').child("BusId").child(phone).child("Tracker")
                ref.set({
                    "lat": lan,
                    "lon": lon
                })

    def notifier(self, phone, lan, lon):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('LocatorDriver').child("BusId").child(phone).child("Notifier").child(lan).child(lon)
                ref.set({
                    "phone": lon,
                })

    def get_notifier(self, phone="T657"):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            try:
                if not firebase_admin._apps:
                    cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                    initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                    ref = db.reference('LocatorDriver').child("BusId").child(phone).child("Notifier")

                    return ref.get()
            except:

                return False

    def get_number(self, loc):
        num = []
        x = self.get_notifier()
        if x:
            if loc in x:
                for i in x[loc].keys():
                    num.append(i)
            return num
        else:
            return num



