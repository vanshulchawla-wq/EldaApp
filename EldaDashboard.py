from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import TwoLineListItem
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://elda:eldaonboard.streamlit.app@elda.wzcx5kq.mongodb.net/?appName=Elda"

# Elda brand colors from getelda.com
ELDA_PRIMARY = (0.106, 0.498, 0.290, 1)      # #1B7F4A
ELDA_ACCENT = (0.125, 0.729, 0.361, 1)       # #20BA5C
ELDA_LIGHT_BG = (0.941, 0.976, 0.957, 1)     # #f0f9f4
ELDA_DARK = (0.059, 0.149, 0.125, 1)         # #0f2620

def get_collection():
    client = MongoClient(MONGO_URI)
    db = client["EldaOnboardPlatform"]
    return db["EldaCustomerOnboardData"]

KV = '''
ScreenManager:
    HomeScreen:
    OnboardScreen:
    DashboardScreen:
    DirectoryScreen:
    DetailScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Elda"
            md_bg_color: 0.106, 0.498, 0.290, 1
            specific_text_color: 1, 1, 1, 1

        BoxLayout:
            orientation: "vertical"
            padding: "30dp"
            spacing: "20dp"
            canvas.before:
                Color:
                    rgba: 0.941, 0.976, 0.957, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Widget:
                size_hint_y: 0.15

            Image:
                source: "icon.png"
                size_hint: None, None
                size: "120dp", "120dp"
                pos_hint: {"center_x": 0.5}

            MDLabel:
                text: "elda."
                font_style: "H3"
                halign: "center"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.106, 0.498, 0.290, 1
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "Senior First Companion"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.3, 0.3, 0.3, 1
                size_hint_y: None
                height: self.texture_size[1]

            Widget:
                size_hint_y: 0.1

            MDRaisedButton:
                text: "Onboard New Customer"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.9
                md_bg_color: 0.106, 0.498, 0.290, 1
                text_color: 1, 1, 1, 1
                on_release: root.manager.current = "onboard"

            MDRaisedButton:
                text: "Customer Directory"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.9
                md_bg_color: 0.125, 0.729, 0.361, 1
                text_color: 1, 1, 1, 1
                on_release: root.manager.current = "directory"

            Widget:

<OnboardScreen>:
    name: "onboard"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "New Customer"
            md_bg_color: 0.106, 0.498, 0.290, 1
            specific_text_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "16dp"
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: onboard_name
                    hint_text: "Senior's Name"
                    mode: "rectangle"
                MDTextField:
                    id: onboard_age
                    hint_text: "Age"
                    mode: "rectangle"
                MDTextField:
                    id: onboard_mobile
                    hint_text: "Mobile"
                    mode: "rectangle"
                MDTextField:
                    id: onboard_location
                    hint_text: "Society/Apartment"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "🚀 Launch Dashboard"
                    pos_hint: {"center_x": 0.5}
                    size_hint_x: 0.9
                    md_bg_color: 0.106, 0.498, 0.290, 1
                    on_release: root.launch_dashboard()

<DashboardScreen>:
    name: "dashboard"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: root.header_text
            md_bg_color: 0.106, 0.498, 0.290, 1
            specific_text_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        MDTabs:
            id: tabs

            Tab:
                title: "Health"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"

                            MDTextField:
                                id: health_conditions
                                hint_text: "Conditions (comma separated)"
                                helper_text: "e.g. Diabetes, Thyroid"
                                helper_text_mode: "on_focus"
                                mode: "rectangle"

                            MDTextField:
                                id: med1_name
                                hint_text: "Medicine 1 - Name"
                                mode: "rectangle"
                            MDTextField:
                                id: med1_dose
                                hint_text: "Medicine 1 - Dose"
                                mode: "rectangle"
                            MDTextField:
                                id: med1_time
                                hint_text: "Medicine 1 - Time"
                                mode: "rectangle"

                            MDTextField:
                                id: med2_name
                                hint_text: "Medicine 2 - Name"
                                mode: "rectangle"
                            MDTextField:
                                id: med2_dose
                                hint_text: "Medicine 2 - Dose"
                                mode: "rectangle"
                            MDTextField:
                                id: med2_time
                                hint_text: "Medicine 2 - Time"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "Save Health"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: root.save_health()

            Tab:
                title: "Home"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"

                            MDTextField:
                                id: app1_name
                                hint_text: "Appliance 1 - Name"
                                mode: "rectangle"
                            MDTextField:
                                id: app1_vendor
                                hint_text: "Appliance 1 - Vendor/Phone"
                                mode: "rectangle"
                            MDTextField:
                                id: app1_status
                                hint_text: "Appliance 1 - Status"
                                text: "Healthy"
                                mode: "rectangle"

                            MDTextField:
                                id: app2_name
                                hint_text: "Appliance 2 - Name"
                                mode: "rectangle"
                            MDTextField:
                                id: app2_vendor
                                hint_text: "Appliance 2 - Vendor/Phone"
                                mode: "rectangle"
                            MDTextField:
                                id: app2_status
                                hint_text: "Appliance 2 - Status"
                                text: "Healthy"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "Save Home"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: root.save_home()

            Tab:
                title: "Social"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"

                            MDTextField:
                                id: social1_name
                                hint_text: "Activity 1 - Name"
                                mode: "rectangle"
                            MDTextField:
                                id: social1_freq
                                hint_text: "Activity 1 - Frequency"
                                mode: "rectangle"
                            MDTextField:
                                id: social1_desc
                                hint_text: "Activity 1 - Description"
                                mode: "rectangle"

                            MDTextField:
                                id: social2_name
                                hint_text: "Activity 2 - Name"
                                mode: "rectangle"
                            MDTextField:
                                id: social2_freq
                                hint_text: "Activity 2 - Frequency"
                                mode: "rectangle"
                            MDTextField:
                                id: social2_desc
                                hint_text: "Activity 2 - Description"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "Save Social"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: root.save_social()

            Tab:
                title: "Emergency"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"

                            MDTextField:
                                id: em_hospital
                                hint_text: "Hospital"
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
                                id: em_primary
                                hint_text: "Primary Contact"
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
                                id: em_ambulance
                                hint_text: "Ambulance"
                                text: "102"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "Save Emergency"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                on_release: root.save_emergency()

<DirectoryScreen>:
    name: "directory"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Customer Directory"
            md_bg_color: 0.106, 0.498, 0.290, 1
            specific_text_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        MDTextField:
            id: search_field
            hint_text: "Search by phone..."
            mode: "rectangle"
            size_hint_x: 0.95
            pos_hint: {"center_x": 0.5}
            on_text: root.search(self.text)

        ScrollView:
            MDList:
                id: customer_list

<DetailScreen>:
    name: "detail"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Details"
            md_bg_color: 0.106, 0.498, 0.290, 1
            specific_text_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.go_directory()]]

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: root.customer_name
                    font_style: "H5"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDLabel:
                    text: root.customer_info
                    size_hint_y: None
                    height: self.texture_size[1]
                MDSeparator:
                MDLabel:
                    text: root.emergency_text
                    size_hint_y: None
                    height: self.texture_size[1]
                MDSeparator:
                MDLabel:
                    text: root.social_text
                    size_hint_y: None
                    height: self.texture_size[1]
                MDSeparator:
                MDLabel:
                    text: root.health_text
                    size_hint_y: None
                    height: self.texture_size[1]
                MDSeparator:
                MDLabel:
                    text: root.home_text
                    size_hint_y: None
                    height: self.texture_size[1]

<Tab>:
'''


class Tab(BoxLayout, MDTabsBase):
    pass


class HomeScreen(Screen):
    pass


class OnboardScreen(Screen):
    def launch_dashboard(self):
        app = MDApp.get_running_app()
        app.customer_name = self.ids.onboard_name.text
        app.customer_age = self.ids.onboard_age.text
        app.customer_mobile = self.ids.onboard_mobile.text
        app.customer_location = self.ids.onboard_location.text

        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"name": app.customer_name, "age": app.customer_age,
                          "mobile": app.customer_mobile, "location": app.customer_location}},
                upsert=True
            )
        except Exception as e:
            print(f"Error: {e}")

        dashboard = self.manager.get_screen("dashboard")
        dashboard.header_text = f"{app.customer_name} ({app.customer_age})"
        self.manager.current = "dashboard"


class DashboardScreen(Screen):
    header_text = StringProperty("Dashboard")

    def save_health(self):
        app = MDApp.get_running_app()
        conditions = [c.strip() for c in self.ids.health_conditions.text.split(",") if c.strip()]
        meds = []
        if self.ids.med1_name.text:
            meds.append({"Medicine": self.ids.med1_name.text, "Dose": self.ids.med1_dose.text, "Time": self.ids.med1_time.text})
        if self.ids.med2_name.text:
            meds.append({"Medicine": self.ids.med2_name.text, "Dose": self.ids.med2_dose.text, "Time": self.ids.med2_time.text})
        try:
            get_collection().update_one({"name": app.customer_name}, {"$set": {"health": {"conditions": conditions, "medications": meds}}}, upsert=True)
        except Exception as e:
            print(f"Error: {e}")

    def save_home(self):
        app = MDApp.get_running_app()
        appliances = []
        if self.ids.app1_name.text:
            appliances.append({"name": self.ids.app1_name.text, "vendor": self.ids.app1_vendor.text, "status": self.ids.app1_status.text})
        if self.ids.app2_name.text:
            appliances.append({"name": self.ids.app2_name.text, "vendor": self.ids.app2_vendor.text, "status": self.ids.app2_status.text})
        try:
            get_collection().update_one({"name": app.customer_name}, {"$set": {"home": {"appliances": appliances}}}, upsert=True)
        except Exception as e:
            print(f"Error: {e}")

    def save_social(self):
        app = MDApp.get_running_app()
        activities = []
        if self.ids.social1_name.text:
            activities.append({"name": self.ids.social1_name.text, "frequency": self.ids.social1_freq.text, "description": self.ids.social1_desc.text})
        if self.ids.social2_name.text:
            activities.append({"name": self.ids.social2_name.text, "frequency": self.ids.social2_freq.text, "description": self.ids.social2_desc.text})
        try:
            get_collection().update_one({"name": app.customer_name}, {"$set": {"social": {"activities": activities}}}, upsert=True)
        except Exception as e:
            print(f"Error: {e}")

    def save_emergency(self):
        app = MDApp.get_running_app()
        try:
            get_collection().update_one({"name": app.customer_name}, {"$set": {"emergency": {
                "hospital": self.ids.em_hospital.text, "er_phone": self.ids.em_er_phone.text,
                "doctor": self.ids.em_doctor.text, "primary_contact": self.ids.em_primary.text,
                "nearby_relative": self.ids.em_relative.text, "security_desk": self.ids.em_security.text,
                "ambulance": self.ids.em_ambulance.text,
            }}}, upsert=True)
        except Exception as e:
            print(f"Error: {e}")


class DirectoryScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.load_customers(), 0.1)

    def load_customers(self, query=None):
        if "customer_list" not in self.ids:
            return
        self.ids.customer_list.clear_widgets()
        try:
            collection = get_collection()
            q = {"mobile": {"$regex": query}} if query else {}
            customers = list(collection.find(q, {"_id": 0}).limit(50))
            for c in customers:
                item = TwoLineListItem(
                    text=c.get("name", ""),
                    secondary_text=f"{c.get('mobile', '')} | {c.get('location', '')}",
                    on_release=lambda x, cust=c: MDApp.get_running_app().show_detail(cust)
                )
                self.ids.customer_list.add_widget(item)
        except Exception as e:
            print(f"Error: {e}")

    def search(self, text):
        self.load_customers(text if text else None)


class DetailScreen(Screen):
    customer_name = StringProperty("")
    customer_info = StringProperty("")
    emergency_text = StringProperty("")
    social_text = StringProperty("")
    health_text = StringProperty("")
    home_text = StringProperty("")


class EldaApp(MDApp):
    customer_name = StringProperty("")
    customer_age = StringProperty("")
    customer_mobile = StringProperty("")
    customer_location = StringProperty("")

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.title = "Elda"
        return Builder.load_string(KV)

    def go_home(self):
        self.root.current = "home"

    def go_directory(self):
        self.root.current = "directory"

    def show_detail(self, customer):
        screen = self.root.get_screen("detail")
        screen.customer_name = customer.get("name", "")
        screen.customer_info = f"📱 {customer.get('mobile', '')} | 📍 {customer.get('location', '')} | Age: {customer.get('age', '')}"

        em = customer.get("emergency", {})
        if em:
            lines = [f"{k}: {v}" for k, v in em.items() if v]
            screen.emergency_text = "🚨 Emergency\n" + "\n".join(lines)
        else:
            screen.emergency_text = "🚨 No emergency data"

        social = customer.get("social", {})
        acts = social.get("activities", []) if social else []
        if acts:
            lines = [f"• {a.get('name','')} — {a.get('frequency','')}" for a in acts]
            screen.social_text = "✨ Social\n" + "\n".join(lines)
        else:
            screen.social_text = "✨ No social data"

        health = customer.get("health", {})
        if health:
            screen.health_text = f"💊 Health\nConditions: {', '.join(health.get('conditions', []))}"
        else:
            screen.health_text = "💊 No health data"

        appliances = customer.get("home", {}).get("appliances", [])
        if appliances:
            lines = [f"• {a.get('name','')} — {a.get('status','')}" for a in appliances]
            screen.home_text = "🏠 Home\n" + "\n".join(lines)
        else:
            screen.home_text = "🏠 No home data"

        self.root.current = "detail"


if __name__ == "__main__":
    EldaApp().run()
