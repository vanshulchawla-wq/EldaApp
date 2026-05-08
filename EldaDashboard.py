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
                    spacing: "8dp"

                    ScrollView:
                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"

                            MDLabel:
                                text: "💊 Medical Conditions & Meds"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
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
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
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
                                hint_text: "Days (e.g. M,T,W,Th,F,S,Su or Daily)"
                                mode: "rectangle"

                            MDLabel:
                                text: "Medicine 2"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
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
                                hint_text: "Days (e.g. M,T,W,Th,F,S,Su or Daily)"
                                mode: "rectangle"

                            MDLabel:
                                text: "Medicine 3"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: med3_name
                                hint_text: "Medicine Name"
                                mode: "rectangle"
                            MDTextField:
                                id: med3_dose
                                hint_text: "Dose"
                                mode: "rectangle"
                            MDTextField:
                                id: med3_time
                                hint_text: "Time (Morning/Night/Both)"
                                mode: "rectangle"
                            MDTextField:
                                id: med3_days
                                hint_text: "Days (e.g. M,T,W,Th,F,S,Su or Daily)"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "💾 Save Health"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                md_bg_color: 0.106, 0.498, 0.290, 1
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

                            MDLabel:
                                text: "Appliance 1"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: app1_name
                                hint_text: "Name"
                                text: "RO Water Purifier"
                                mode: "rectangle"
                            MDTextField:
                                id: app1_vendor
                                hint_text: "Service Partner (Name/Phone)"
                                mode: "rectangle"
                            MDTextField:
                                id: app1_last_service
                                hint_text: "Last Service Date (e.g. 2024-01-15)"
                                mode: "rectangle"
                            MDTextField:
                                id: app1_status
                                hint_text: "Status (Healthy/Needs Service/Broken)"
                                text: "Healthy"
                                mode: "rectangle"

                            MDLabel:
                                text: "Appliance 2"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: app2_name
                                hint_text: "Name"
                                text: "Inverter/UPS"
                                mode: "rectangle"
                            MDTextField:
                                id: app2_vendor
                                hint_text: "Service Partner (Name/Phone)"
                                mode: "rectangle"
                            MDTextField:
                                id: app2_last_service
                                hint_text: "Last Service Date (e.g. 2024-01-15)"
                                mode: "rectangle"
                            MDTextField:
                                id: app2_status
                                hint_text: "Status (Healthy/Needs Service/Broken)"
                                text: "Healthy"
                                mode: "rectangle"

                            MDLabel:
                                text: "Appliance 3"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: app3_name
                                hint_text: "Name"
                                mode: "rectangle"
                            MDTextField:
                                id: app3_vendor
                                hint_text: "Service Partner (Name/Phone)"
                                mode: "rectangle"
                            MDTextField:
                                id: app3_last_service
                                hint_text: "Last Service Date (e.g. 2024-01-15)"
                                mode: "rectangle"
                            MDTextField:
                                id: app3_status
                                hint_text: "Status (Healthy/Needs Service/Broken)"
                                text: "Healthy"
                                mode: "rectangle"

                            MDLabel:
                                text: "Appliance 4"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: app4_name
                                hint_text: "Name"
                                mode: "rectangle"
                            MDTextField:
                                id: app4_vendor
                                hint_text: "Service Partner (Name/Phone)"
                                mode: "rectangle"
                            MDTextField:
                                id: app4_last_service
                                hint_text: "Last Service Date (e.g. 2024-01-15)"
                                mode: "rectangle"
                            MDTextField:
                                id: app4_status
                                hint_text: "Status (Healthy/Needs Service/Broken)"
                                text: "Healthy"
                                mode: "rectangle"

                            MDRaisedButton:
                                text: "💾 Save Home"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                md_bg_color: 0.106, 0.498, 0.290, 1
                                on_release: root.save_home()

            Tab:
                title: "Social"
                BoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    spacing: "8dp"

                    ScrollView:
                        BoxLayout:
                            id: social_container
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: "8dp"

                    MDRaisedButton:
                        text: "➕ Add Activity"
                        pos_hint: {"center_x": 0.5}
                        size_hint_x: 0.9
                        md_bg_color: 0.125, 0.729, 0.361, 1
                        on_release: root.add_social_activity()

                    MDRaisedButton:
                        text: "💾 Save Social"
                        pos_hint: {"center_x": 0.5}
                        size_hint_x: 0.9
                        md_bg_color: 0.106, 0.498, 0.290, 1
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

                            MDLabel:
                                text: "🏥 Medical"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
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

                            MDLabel:
                                text: "👨‍👩‍👧‍👦 Family"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: em_primary
                                hint_text: "Primary Contact (Son/Daughter)"
                                mode: "rectangle"
                            MDTextField:
                                id: em_relative
                                hint_text: "Nearby Relative"
                                mode: "rectangle"

                            MDLabel:
                                text: "🏢 Society & RWA"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDTextField:
                                id: em_security
                                hint_text: "Security Desk"
                                mode: "rectangle"
                            MDTextField:
                                id: em_rwa
                                hint_text: "RWA Emergency"
                                mode: "rectangle"
                            MDTextField:
                                id: em_maintenance
                                hint_text: "Maintenance"
                                mode: "rectangle"

                            MDLabel:
                                text: "👮 Local Services"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.369, 0.125, 1
                                size_hint_y: None
                                height: self.texture_size[1]
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
                                text: "💾 Save Emergency"
                                pos_hint: {"center_x": 0.5}
                                size_hint_x: 0.9
                                md_bg_color: 0.106, 0.498, 0.290, 1
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


class DashboardScreen_PLACEHOLDER:
    pass

                BoxLayout:
                    orientation: "vertical"
                    padding: "20dp"
                    spacing: "16dp"
                    canvas.before:
                        Color:
                            rgba: 0.941, 0.976, 0.957, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size

                    MDLabel:
                        text: "Manager Oversight"
                        font_style: "H5"
                        theme_text_color: "Custom"
                        text_color: 0.106, 0.369, 0.125, 1
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDCard:
                        size_hint_y: None
                        height: "80dp"
                        padding: "16dp"
                        md_bg_color: 1, 1, 1, 1
                        radius: [10]
                        BoxLayout:
                            orientation: "vertical"
                            MDLabel:
                                text: "Medication Adherence"
                                theme_text_color: "Custom"
                                text_color: 0.4, 0.4, 0.4, 1
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                id: metric_adherence
                                text: "100%"
                                font_style: "H4"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.498, 0.290, 1
                                size_hint_y: None
                                height: self.texture_size[1]

                    MDCard:
                        size_hint_y: None
                        height: "80dp"
                        padding: "16dp"
                        md_bg_color: 1, 1, 1, 1
                        radius: [10]
                        BoxLayout:
                            orientation: "vertical"
                            MDLabel:
                                text: "Critical Tasks"
                                theme_text_color: "Custom"
                                text_color: 0.4, 0.4, 0.4, 1
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                id: metric_tasks
                                text: "0 Pending"
                                font_style: "H4"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.498, 0.290, 1
                                size_hint_y: None
                                height: self.texture_size[1]

                    MDCard:
                        size_hint_y: None
                        height: "80dp"
                        padding: "16dp"
                        md_bg_color: 1, 1, 1, 1
                        radius: [10]
                        BoxLayout:
                            orientation: "vertical"
                            MDLabel:
                                text: "Next Visit"
                                theme_text_color: "Custom"
                                text_color: 0.4, 0.4, 0.4, 1
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                id: metric_visit
                                text: "In 4 Days"
                                font_style: "H4"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.498, 0.290, 1
                                size_hint_y: None
                                height: self.texture_size[1]

                    MDCard:
                        size_hint_y: None
                        height: "80dp"
                        padding: "16dp"
                        md_bg_color: 1, 1, 1, 1
                        radius: [10]
                        BoxLayout:
                            orientation: "vertical"
                            MDLabel:
                                text: "Profile Complete"
                                theme_text_color: "Custom"
                                text_color: 0.4, 0.4, 0.4, 1
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                id: metric_profile
                                text: "Checking..."
                                font_style: "H4"
                                theme_text_color: "Custom"
                                text_color: 0.106, 0.498, 0.290, 1
                                size_hint_y: None
                                height: self.texture_size[1]

                    MDRaisedButton:
                        text: "🔄 Refresh"
                        pos_hint: {"center_x": 0.5}
                        size_hint_x: 0.9
                        md_bg_color: 0.106, 0.498, 0.290, 1
                        on_release: root.refresh_manager()

                    Widget:

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
    _social_count = 0

    def on_enter(self):
        if self._social_count == 0:
            self.add_social_activity()

    def add_social_activity(self):
        self._social_count += 1
        i = self._social_count
        container = self.ids.social_container

        from kivy.uix.boxlayout import BoxLayout
        from kivymd.uix.label import MDLabel
        from kivymd.uix.textfield import MDTextField

        box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=4, padding=[0, 4])
        box.bind(minimum_height=box.setter("height"))

        lbl = MDLabel(text=f"Activity {i}", font_style="H6",
                      theme_text_color="Custom", text_color=(0.106, 0.369, 0.125, 1),
                      size_hint_y=None, height="32dp")
        name_f = MDTextField(hint_text="Activity Name", mode="rectangle",
                             size_hint_y=None, height="48dp")
        freq_f = MDTextField(hint_text="Frequency (e.g. Every Thursday)", mode="rectangle",
                             size_hint_y=None, height="48dp")
        desc_f = MDTextField(hint_text="Description", mode="rectangle",
                             size_hint_y=None, height="48dp")

        name_f.id = f"social_name_{i}"
        freq_f.id = f"social_freq_{i}"
        desc_f.id = f"social_desc_{i}"

        for w in [lbl, name_f, freq_f, desc_f]:
            box.add_widget(w)

        box._social_fields = (name_f, freq_f, desc_f)
        container.add_widget(box)
    def save_health(self):
        app = MDApp.get_running_app()
        conditions = [c.strip() for c in self.ids.health_conditions.text.split(",") if c.strip()]
        meds = []
        for i in range(1, 4):
            name = self.ids[f"med{i}_name"].text
            if name:
                meds.append({
                    "Medicine": name,
                    "Dose": self.ids[f"med{i}_dose"].text,
                    "Time": self.ids[f"med{i}_time"].text,
                    "Days": self.ids[f"med{i}_days"].text,
                })
        try:
            get_collection().update_one({"name": app.customer_name}, {"$set": {"health": {"conditions": conditions, "medications": meds}}}, upsert=True)
            from kivymd.toast import toast
            toast("Health data saved!")
        except Exception as e:
            print(f"Error: {e}")

    def save_home(self):
        app = MDApp.get_running_app()
        appliances = []
        for i in range(1, 5):
            name = self.ids[f"app{i}_name"].text
            if name:
                appliances.append({
                    "name": name,
                    "vendor": self.ids[f"app{i}_vendor"].text,
                    "last_service": self.ids[f"app{i}_last_service"].text,
                    "status": self.ids[f"app{i}_status"].text,
                })
        try:
            get_collection().update_one({"name": app.customer_name}, {"$set": {"home": {"appliances": appliances}}}, upsert=True)
            from kivymd.toast import toast
            toast("Home data saved!")
        except Exception as e:
            print(f"Error: {e}")

    def save_social(self):
        app = MDApp.get_running_app()
        activities = []
        for box in self.ids.social_container.children[::-1]:
            if hasattr(box, "_social_fields"):
                name_f, freq_f, desc_f = box._social_fields
                if name_f.text.strip():
                    activities.append({
                        "name": name_f.text,
                        "frequency": freq_f.text,
                        "description": desc_f.text,
                    })
        try:
            get_collection().update_one({"name": app.customer_name}, {"$set": {"social": {"activities": activities}}}, upsert=True)
            from kivymd.toast import toast
            toast("Social data saved!")
        except Exception as e:
            print(f"Error: {e}")

    def refresh_manager(self):
        app = MDApp.get_running_app()
        try:
            doc = get_collection().find_one({"name": app.customer_name}, {"_id": 0})
            if not doc:
                return
            sections = ["health", "home", "social", "emergency"]
            filled = sum(1 for s in sections if doc.get(s))
            self.ids.metric_profile.text = f"{filled}/{len(sections)} Sections"
            meds = doc.get("health", {}).get("medications", [])
            self.ids.metric_adherence.text = "100%" if meds else "No Meds"
            self.ids.metric_tasks.text = "0 Pending"
            self.ids.metric_visit.text = "In 4 Days"
        except Exception as e:
            print(f"Error: {e}")


        app = MDApp.get_running_app()
        try:
            get_collection().update_one({"name": app.customer_name}, {"$set": {"emergency": {
                "hospital": self.ids.em_hospital.text,
                "er_phone": self.ids.em_er_phone.text,
                "doctor": self.ids.em_doctor.text,
                "dr_phone": self.ids.em_dr_phone.text,
                "primary_contact": self.ids.em_primary.text,
                "nearby_relative": self.ids.em_relative.text,
                "security_desk": self.ids.em_security.text,
                "rwa_emergency": self.ids.em_rwa.text,
                "maintenance": self.ids.em_maintenance.text,
                "police_station": self.ids.em_police.text,
                "ambulance": self.ids.em_ambulance.text,
            }}}, upsert=True)
            from kivymd.toast import toast
            toast("Emergency data saved!")
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
