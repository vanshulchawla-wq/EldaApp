from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
from pymongo import MongoClient
import os
import re

# ISD codes with country and expected phone length
ISD_CODES = [
    ("+91", "India", 10),
    ("+1", "US/Canada", 10),
    ("+44", "UK", 10),
    ("+61", "Australia", 9),
    ("+971", "UAE", 9),
    ("+65", "Singapore", 8),
]

ISD_DISPLAY = [f"{code} ({country})" for code, country, _ in ISD_CODES]


def validate_phone(phone_text, isd_index=0):
    """Validate phone number length based on selected ISD code."""
    digits = re.sub(r'\D', '', phone_text)
    expected_len = ISD_CODES[isd_index][2]
    if not digits:
        return False, "Phone number is required"
    if len(digits) != expected_len:
        return False, f"Phone must be {expected_len} digits for {ISD_CODES[isd_index][1]}"
    return True, ""


def validate_name(text):
    if not text.strip():
        return False, "Name is required"
    if not re.match(r'^[a-zA-Z\s\.]+$', text.strip()):
        return False, "Name must contain only letters, spaces, or dots"
    return True, ""


def validate_age(text):
    if not text.strip():
        return False, "Age is required"
    if not text.strip().isdigit():
        return False, "Age must be a number"
    age = int(text.strip())
    if age < 1 or age > 120:
        return False, "Age must be between 1 and 120"
    return True, ""


def validate_required(text, field_name):
    if not text.strip():
        return False, f"{field_name} is required"
    return True, ""

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
                BoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "48dp"
                    spacing: "8dp"

                    Spinner:
                        id: isd_picker
                        text: "+91 (India)"
                        values: app.isd_values
                        size_hint_x: 0.4
                        background_color: 0.106, 0.369, 0.125, 1
                        color: 1, 1, 1, 1

                    MDTextField:
                        id: onboard_mobile
                        hint_text: "Mobile (digits only)"
                        text: "9909987899"
                        mode: "rectangle"
                        input_filter: "int"
                        max_text_length: 10
                MDTextField:
                    id: onboard_location
                    hint_text: "Society/Apartment"
                    text: "Gurgaon"
                    mode: "rectangle"

                MDLabel:
                    id: onboard_error
                    text: ""
                    theme_text_color: "Error"
                    size_hint_y: None
                    height: self.texture_size[1] if self.text else 0
                    padding: [0, 4]

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
                                input_filter: "int"
                                max_text_length: 10
                            MDTextField:
                                id: em_doctor
                                hint_text: "Doctor"
                                mode: "rectangle"
                            MDTextField:
                                id: em_dr_phone
                                hint_text: "Dr. Phone"
                                mode: "rectangle"
                                input_filter: "int"
                                max_text_length: 10
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
    def get_isd_index(self):
        picker_text = self.ids.isd_picker.text
        for i, display in enumerate(ISD_DISPLAY):
            if display == picker_text:
                return i
        return 0

    def launch_dashboard(self):
        # Validate all fields
        errors = []
        valid, msg = validate_name(self.ids.onboard_name.text)
        if not valid:
            errors.append(msg)

        valid, msg = validate_age(self.ids.onboard_age.text)
        if not valid:
            errors.append(msg)

        isd_idx = self.get_isd_index()
        valid, msg = validate_phone(self.ids.onboard_mobile.text, isd_idx)
        if not valid:
            errors.append(msg)

        valid, msg = validate_required(self.ids.onboard_location.text, "Location")
        if not valid:
            errors.append(msg)

        if errors:
            self.ids.onboard_error.text = "\n".join(errors)
            return

        self.ids.onboard_error.text = ""
        app = MDApp.get_running_app()
        isd_code = ISD_CODES[isd_idx][0]
        app.customer_name = self.ids.onboard_name.text.strip()
        app.customer_age = self.ids.onboard_age.text.strip()
        app.customer_mobile = f"{isd_code}{self.ids.onboard_mobile.text.strip()}"
        app.customer_location = self.ids.onboard_location.text.strip()

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
        from kivymd.toast import toast
        app = MDApp.get_running_app()

        # Validate: at least one condition or one medicine required
        conditions = [c.strip() for c in self.ids.health_conditions.text.split(",") if c.strip()]
        has_med1 = bool(self.ids.med1_name.text.strip())
        has_med2 = bool(self.ids.med2_name.text.strip())

        if not conditions and not has_med1 and not has_med2:
            toast("Enter at least one condition or medicine")
            return

        # Validate medicine fields are complete if partially filled
        for prefix, label in [("med1", "Medicine 1"), ("med2", "Medicine 2")]:
            name = self.ids[f"{prefix}_name"].text.strip()
            if name:
                if not self.ids[f"{prefix}_dose"].text.strip():
                    toast(f"{label}: Dose is required")
                    return
                if not self.ids[f"{prefix}_time"].text.strip():
                    toast(f"{label}: Time is required")
                    return

        medications = []
        if has_med1:
            medications.append({
                "Medicine": self.ids.med1_name.text.strip(),
                "Dose": self.ids.med1_dose.text.strip(),
                "Time": self.ids.med1_time.text.strip(),
                "Days": self.ids.med1_days.text.strip(),
            })
        if has_med2:
            medications.append({
                "Medicine": self.ids.med2_name.text.strip(),
                "Dose": self.ids.med2_dose.text.strip(),
                "Time": self.ids.med2_time.text.strip(),
                "Days": self.ids.med2_days.text.strip(),
            })

        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"health": {"conditions": conditions, "medications": medications}}},
                upsert=True
            )
            toast("Health data saved!")
        except Exception as e:
            print(f"Save error: {e}")

    def save_home(self):
        from kivymd.toast import toast
        app = MDApp.get_running_app()

        VALID_STATUSES = ["healthy", "needs service", "broken"]
        appliances = []
        for prefix, label in [("app1", "Appliance 1"), ("app2", "Appliance 2")]:
            name = self.ids[f"{prefix}_name"].text.strip()
            if name:
                status = self.ids[f"{prefix}_status"].text.strip()
                if status.lower() not in VALID_STATUSES:
                    toast(f"{label}: Status must be Healthy/Needs Service/Broken")
                    return
                appliances.append({
                    "name": name,
                    "vendor": self.ids[f"{prefix}_vendor"].text.strip(),
                    "status": status,
                })

        if not appliances:
            toast("Add at least one appliance")
            return

        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"home": {"appliances": appliances}}},
                upsert=True
            )
            toast("Home data saved!")
        except Exception as e:
            print(f"Save error: {e}")

    def save_social(self):
        from kivymd.toast import toast
        app = MDApp.get_running_app()

        activities = []
        for prefix, label in [("social1", "Activity 1"), ("social2", "Activity 2")]:
            name = self.ids[f"{prefix}_name"].text.strip()
            if name:
                if not self.ids[f"{prefix}_freq"].text.strip():
                    toast(f"{label}: Frequency is required")
                    return
                activities.append({
                    "name": name,
                    "frequency": self.ids[f"{prefix}_freq"].text.strip(),
                    "description": self.ids[f"{prefix}_desc"].text.strip(),
                })

        if not activities:
            toast("Add at least one activity")
            return

        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"social": {"activities": activities}}},
                upsert=True
            )
            toast("Social data saved!")
        except Exception as e:
            print(f"Save error: {e}")

    def save_emergency(self):
        from kivymd.toast import toast
        app = MDApp.get_running_app()

        # Validate required fields
        required = [
            ("em_hospital", "Hospital"),
            ("em_er_phone", "ER Phone"),
            ("em_primary", "Primary Contact"),
        ]
        for field_id, label in required:
            if not self.ids[field_id].text.strip():
                toast(f"{label} is required")
                return

        # Validate phone fields (digits only, 3-15 chars for flexibility)
        phone_fields = [
            ("em_er_phone", "ER Phone"),
            ("em_dr_phone", "Dr. Phone"),
        ]
        for field_id, label in phone_fields:
            val = self.ids[field_id].text.strip()
            if val and (not val.isdigit() or len(val) < 3 or len(val) > 15):
                toast(f"{label}: Must be 3-15 digits")
                return

        try:
            collection = get_collection()
            collection.update_one(
                {"name": app.customer_name},
                {"$set": {"emergency": {
                    "hospital": self.ids.em_hospital.text.strip(),
                    "er_phone": self.ids.em_er_phone.text.strip(),
                    "doctor": self.ids.em_doctor.text.strip(),
                    "dr_phone": self.ids.em_dr_phone.text.strip(),
                    "primary_contact": self.ids.em_primary.text.strip(),
                    "nearby_relative": self.ids.em_relative.text.strip(),
                    "security_desk": self.ids.em_security.text.strip(),
                    "rwa_emergency": self.ids.em_rwa.text.strip(),
                    "police_station": self.ids.em_police.text.strip(),
                    "ambulance": self.ids.em_ambulance.text.strip(),
                }}},
                upsert=True
            )
            toast("Emergency data saved!")
        except Exception as e:
            print(f"Save error: {e}")


class EldaOnboardApp(MDApp):
    customer_name = StringProperty("")
    customer_age = StringProperty("")
    customer_mobile = StringProperty("")
    customer_location = StringProperty("")
    isd_values = ISD_DISPLAY

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.title = "Elda Onboard"
        return Builder.load_string(KV)


if __name__ == "__main__":
    EldaOnboardApp().run()
