from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://<db_username>:<db_password>@elda.wzcx5kq.mongodb.net/?appName=Elda")

def get_collection():
    client = MongoClient(MONGO_URI)
    db = client["EldaOnboardPlatform"]
    return db["EldaCustomerOnboardData"]

KV = '''
#:import toast kivymd.toast.toast

ScreenManager:
    OnboardScreen:
    DashboardScreen:

<OnboardScreen>:
    name: "onboard"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Elda | Life Ledger"
            md_bg_color: 0.106, 0.369, 0.125, 1
            specific_text_color: 1, 1, 1, 1

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "16dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "📝 Initial Setup"
                    font_style: "H5"
                    size_hint_y: None
                    height: self.texture_size[1]
                    padding: [0, 10]

                MDTextField:
                    id: onboard_name
                    hint_text: "Senior's Name"
                    text: "Mrs. Chawla"
                    mode: "rectangle"
                MDTextField:
                    id: onboard_age
                    hint_text: "Age"
                    text: "62"
                    mode: "rectangle"
                MDTextField:
                    id: onboard_mobile
                    hint_text: "Mobile"
                    text: "9909987899"
                    mode: "rectangle"
                MDTextField:
                    id: onboard_location
                    hint_text: "Society/Apartment"
                    text: "Gurgaon"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "🚀 Launch Dashboard"
                    pos_hint: {"center_x": 0.5}
                    size_hint_x: 0.9
                    md_bg_color: 0.106, 0.369, 0.125, 1
                    on_release: root.launch_dashboard()

<DashboardScreen>:
    name: "dashboard"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: root.header_text
            md_bg_color: 0.106, 0.369, 0.125, 1
            specific_text_color: 1, 1, 1, 1

        MDTabs:
            id: tabs
            on_tab_switch: root.on_tab_switch(*args)

            Tab:
                title: "Health"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    spacing: "8dp"

                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"
                            padding: "4dp"

                            MDLabel:
                                text: "💊 Medical Conditions & Meds"
                                font_style: "H6"
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDTextField:
                                id: health_conditions
                                hint_text: "Conditions (comma separated)"
                                helper_text: "e.g. Diabetes, Thyroid, Hypertension"
                                helper_text_mode: "on_focus"
                                mode: "rectangle"

                            MDLabel:
                                text: "Medicine 1"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: med1_name
                                hint_text: "Medicine Name"
                                mode: "rectangle"
                            MDTextField:
                                id: med1_dose
                                hint_text: "Dose"
                                mode: "rectangle"
                            MDTextField:
                                id: med1_time
                                hint_text: "Time (Morning/Night/Both)"
                                mode: "rectangle"
                            MDTextField:
                                id: med1_days
                                hint_text: "Days (e.g. M,T,W,Th,F,S,Su)"
                                mode: "rectangle"

                            MDLabel:
                                text: "Medicine 2"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: med2_name
                                hint_text: "Medicine Name"
                                mode: "rectangle"
                            MDTextField:
                                id: med2_dose
                                hint_text: "Dose"
                                mode: "rectangle"
                            MDTextField:
                                id: med2_time
                                hint_text: "Time (Morning/Night/Both)"
                                mode: "rectangle"
                            MDTextField:
                                id: med2_days
                                hint_text: "Days (e.g. M,T,W,Th,F,S,Su)"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "💾 Save Health Data"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: root.save_health()

            Tab:
                title: "Home"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    spacing: "8dp"

                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"
                            padding: "4dp"

                            MDLabel:
                                text: "🏠 Appliance Registry"
                                font_style: "H6"
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDLabel:
                                text: "Appliance 1"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: app1_name
                                hint_text: "Appliance Name"
                                text: "RO Water Purifier"
                                mode: "rectangle"
                            MDTextField:
                                id: app1_vendor
                                hint_text: "Service Partner (Name/Phone)"
                                mode: "rectangle"
                            MDTextField:
                                id: app1_status
                                hint_text: "Status (Healthy/Needs Service/Broken)"
                                text: "Healthy"
                                mode: "rectangle"

                            MDLabel:
                                text: "Appliance 2"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: app2_name
                                hint_text: "Appliance Name"
                                text: "Inverter/UPS"
                                mode: "rectangle"
                            MDTextField:
                                id: app2_vendor
                                hint_text: "Service Partner (Name/Phone)"
                                mode: "rectangle"
                            MDTextField:
                                id: app2_status
                                hint_text: "Status (Healthy/Needs Service/Broken)"
                                text: "Healthy"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "💾 Save Home Data"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: root.save_home()

            Tab:
                title: "Social"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    spacing: "8dp"

                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"
                            padding: "4dp"

                            MDLabel:
                                text: "✨ Social Activities"
                                font_style: "H6"
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDLabel:
                                text: "Activity 1"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: social1_name
                                hint_text: "Activity Name"
                                mode: "rectangle"
                            MDTextField:
                                id: social1_freq
                                hint_text: "Frequency"
                                mode: "rectangle"
                            MDTextField:
                                id: social1_desc
                                hint_text: "Description"
                                mode: "rectangle"

                            MDLabel:
                                text: "Activity 2"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: social2_name
                                hint_text: "Activity Name"
                                mode: "rectangle"
                            MDTextField:
                                id: social2_freq
                                hint_text: "Frequency"
                                mode: "rectangle"
                            MDTextField:
                                id: social2_desc
                                hint_text: "Description"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "💾 Save Social Data"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: root.save_social()

            Tab:
                title: "Emergency"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    spacing: "8dp"

                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"
                            padding: "4dp"

                            MDLabel:
                                text: "🚨 Crisis Directory"
                                font_style: "H6"
                                size_hint_y: None
                                height: self.texture_size[1]

                            MDTextField:
                                id: em_hospital
                                hint_text: "Hospital"
                                text: "Fortis Memorial, Gurgaon"
                                mode: "rectangle"
                            MDTextField:
                                id: em_er_phone
                                hint_text: "ER Phone"
                                mode: "rectangle"
                            MDTextField:
                                id: em_doctor
                                hint_text: "Doctor"
                                mode: "rectangle"
                            MDTextField:
                                id: em_dr_phone
                                hint_text: "Dr. Phone"
                                mode: "rectangle"
                            MDTextField:
                                id: em_primary
                                hint_text: "Primary Contact (Son/Daughter)"
                                mode: "rectangle"
                            MDTextField:
                                id: em_relative
                                hint_text: "Nearby Relative"
                                mode: "rectangle"
                            MDTextField:
                                id: em_security
                                hint_text: "Security Desk"
                                mode: "rectangle"
                            MDTextField:
                                id: em_rwa
                                hint_text: "RWA Emergency"
                                mode: "rectangle"
                            MDTextField:
                                id: em_police
                                hint_text: "Police Station"
                                mode: "rectangle"
                            MDTextField:
                                id: em_ambulance
                                hint_text: "Ambulance"
                                text: "102"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "💾 Save Emergency Data"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: root.save_emergency()

<Tab>:
'''


class Tab(BoxLayout, MDTabsBase):
    pass


class OnboardScreen(Screen):
    def launch_dashboard(self):
        app = MDApp.get_running_app()
        app.customer_name = self.ids.onboard_name.text
        app.customer_age = self.ids.onboard_age.text
        app.customer_mobile = self.ids.onboard_mobile.text
        app.customer_location = self.ids.onboard_location.text

        # Save to MongoDB
        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {
                    "name": app.customer_name,
                    "age": app.customer_age,
                    "mobile": app.customer_mobile,
                    "location": app.customer_location
                }},
                upsert=True
            )
        except Exception as e:
            print(f"MongoDB save error: {e}")

        # Switch to dashboard
        dashboard = self.manager.get_screen("dashboard")
        dashboard.header_text = f"{app.customer_name} ({app.customer_age} yrs)"
        self.manager.current = "dashboard"


class DashboardScreen(Screen):
    header_text = StringProperty("Elda Dashboard")

    def on_tab_switch(self, *args):
        pass

    def save_health(self):
        app = MDApp.get_running_app()
        conditions = [c.strip() for c in self.ids.health_conditions.text.split(",") if c.strip()]

        medications = []
        if self.ids.med1_name.text:
            medications.append({
                "Medicine": self.ids.med1_name.text,
                "Dose": self.ids.med1_dose.text,
                "Time": self.ids.med1_time.text,
                "Days": self.ids.med1_days.text,
            })
        if self.ids.med2_name.text:
            medications.append({
                "Medicine": self.ids.med2_name.text,
                "Dose": self.ids.med2_dose.text,
                "Time": self.ids.med2_time.text,
                "Days": self.ids.med2_days.text,
            })

        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"health": {"conditions": conditions, "medications": medications}}},
                upsert=True
            )
            from kivymd.toast import toast
            toast("Health data saved!")
        except Exception as e:
            print(f"Save error: {e}")

    def save_home(self):
        app = MDApp.get_running_app()
        appliances = []
        if self.ids.app1_name.text:
            appliances.append({
                "name": self.ids.app1_name.text,
                "vendor": self.ids.app1_vendor.text,
                "status": self.ids.app1_status.text,
            })
        if self.ids.app2_name.text:
            appliances.append({
                "name": self.ids.app2_name.text,
                "vendor": self.ids.app2_vendor.text,
                "status": self.ids.app2_status.text,
            })

        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"home": {"appliances": appliances}}},
                upsert=True
            )
            from kivymd.toast import toast
            toast("Home data saved!")
        except Exception as e:
            print(f"Save error: {e}")

    def save_social(self):
        app = MDApp.get_running_app()
        activities = []
        if self.ids.social1_name.text:
            activities.append({
                "name": self.ids.social1_name.text,
                "frequency": self.ids.social1_freq.text,
                "description": self.ids.social1_desc.text,
            })
        if self.ids.social2_name.text:
            activities.append({
                "name": self.ids.social2_name.text,
                "frequency": self.ids.social2_freq.text,
                "description": self.ids.social2_desc.text,
            })

        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"social": {"activities": activities}}},
                upsert=True
            )
            from kivymd.toast import toast
            toast("Social data saved!")
        except Exception as e:
            print(f"Save error: {e}")

    def save_emergency(self):
        app = MDApp.get_running_app()
        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"emergency": {
                    "hospital": self.ids.em_hospital.text,
                    "er_phone": self.ids.em_er_phone.text,
                    "doctor": self.ids.em_doctor.text,
                    "dr_phone": self.ids.em_dr_phone.text,
                    "primary_contact": self.ids.em_primary.text,
                    "nearby_relative": self.ids.em_relative.text,
                    "security_desk": self.ids.em_security.text,
                    "rwa_emergency": self.ids.em_rwa.text,
                    "police_station": self.ids.em_police.text,
                    "ambulance": self.ids.em_ambulance.text,
                }}},
                upsert=True
            )
            from kivymd.toast import toast
            toast("Emergency data saved!")
        except Exception as e:
            print(f"Save error: {e}")


class EldaOnboardApp(MDApp):
    customer_name = StringProperty("")
    customer_age = StringProperty("")
    customer_mobile = StringProperty("")
    customer_location = StringProperty("")

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.title = "Elda Onboard"
        return Builder.load_string(KV)


if __name__ == "__main__":
    EldaOnboardApp().run()
