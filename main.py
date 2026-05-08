from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
from pymongo import MongoClient
import os

# Set MONGO_URI environment variable or replace the fallback below with your actual URI
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://<db_username>:<db_password>@elda.wzcx5kq.mongodb.net/?appName=Elda")

def get_collection():
    client = MongoClient(MONGO_URI)
    db = client["EldaOnboardPlatform"]
    return db["EldaCustomerOnboardData"]

KV = '''
ScreenManager:
    ListingScreen:
    DetailScreen:
    EditScreen:

<ListingScreen>:
    name: "listing"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Elda Directory"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1

        MDTextField:
            id: search_field
            hint_text: "Search by phone number..."
            mode: "rectangle"
            size_hint_x: 0.95
            pos_hint: {"center_x": 0.5}
            padding: [12, 12]
            on_text: root.search(self.text)

        ScrollView:
            MDList:
                id: customer_list

<DetailScreen>:
    name: "detail"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Customer Details"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.go_back()]]
            right_action_items: [["pencil", lambda x: app.go_edit()]]

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
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
                    text: "🚨 Emergency"
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDLabel:
                    text: root.emergency_text
                    size_hint_y: None
                    height: self.texture_size[1]

                MDSeparator:

                MDLabel:
                    text: "✨ Social Activities"
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDLabel:
                    text: root.social_text
                    size_hint_y: None
                    height: self.texture_size[1]

                MDSeparator:

                MDLabel:
                    text: "💊 Health"
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDLabel:
                    text: root.health_text
                    size_hint_y: None
                    height: self.texture_size[1]

                MDSeparator:

                MDLabel:
                    text: "🏠 Home Appliances"
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]
                MDLabel:
                    text: root.home_text
                    size_hint_y: None
                    height: self.texture_size[1]

<EditScreen>:
    name: "edit"
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Edit Customer"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: 1, 1, 1, 1
            left_action_items: [["arrow-left", lambda x: app.go_detail()]]

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "👤 Profile"
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDTextField:
                    id: edit_name
                    hint_text: "Name"
                    mode: "rectangle"
                MDTextField:
                    id: edit_age
                    hint_text: "Age"
                    mode: "rectangle"
                MDTextField:
                    id: edit_mobile
                    hint_text: "Mobile"
                    mode: "rectangle"
                MDTextField:
                    id: edit_location
                    hint_text: "Location"
                    mode: "rectangle"

                MDLabel:
                    text: "🚨 Emergency"
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDTextField:
                    id: edit_hospital
                    hint_text: "Hospital"
                    mode: "rectangle"
                MDTextField:
                    id: edit_er_phone
                    hint_text: "ER Phone"
                    mode: "rectangle"
                MDTextField:
                    id: edit_doctor
                    hint_text: "Doctor"
                    mode: "rectangle"
                MDTextField:
                    id: edit_primary
                    hint_text: "Primary Contact"
                    mode: "rectangle"

                MDLabel:
                    text: "✨ Social (Activity 1)"
                    font_style: "H6"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDTextField:
                    id: edit_social_name
                    hint_text: "Activity Name"
                    mode: "rectangle"
                MDTextField:
                    id: edit_social_freq
                    hint_text: "Frequency"
                    mode: "rectangle"
                MDTextField:
                    id: edit_social_desc
                    hint_text: "Description"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "💾 Save Changes"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.save_edit()
'''


class ListingScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.load_customers(), 0.1)

    def load_customers(self, query=None):
        if 'customer_list' not in self.ids:
            return
        self.ids.customer_list.clear_widgets()
        collection = get_collection()
        if query:
            customers = list(collection.find({"mobile": {"$regex": query}}, {"_id": 0}).limit(50))
        else:
            customers = list(collection.find({}, {"_id": 0}).limit(50))

        for c in customers:
            item = TwoLineListItem(
                text=c.get("name", "Unknown"),
                secondary_text=f"📱 {c.get('mobile', '')} | 📍 {c.get('location', '')}",
                on_release=lambda x, cust=c: MDApp.get_running_app().show_detail(cust)
            )
            self.ids.customer_list.add_widget(item)

    def search(self, text):
        self.load_customers(text if text else None)


class DetailScreen(Screen):
    customer_name = StringProperty("")
    customer_info = StringProperty("")
    emergency_text = StringProperty("")
    social_text = StringProperty("")
    health_text = StringProperty("")
    home_text = StringProperty("")


class EditScreen(Screen):
    pass


class EldaApp(MDApp):
    current_customer = ObjectProperty(None, allownone=True)

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def show_detail(self, customer):
        self.current_customer = customer
        screen = self.root.get_screen("detail")

        screen.customer_name = customer.get("name", "Unknown")
        screen.customer_info = f"📱 {customer.get('mobile', '')} | 📍 {customer.get('location', '')} | Age: {customer.get('age', '')}"

        # Emergency
        em = customer.get("emergency", {})
        if em:
            lines = []
            for label, key in [("Hospital", "hospital"), ("ER Phone", "er_phone"), ("Doctor", "doctor"),
                               ("Primary", "primary_contact"), ("Security", "security_desk"), ("Ambulance", "ambulance")]:
                val = em.get(key, "")
                if val:
                    lines.append(f"{label}: {val}")
            screen.emergency_text = "\n".join(lines) if lines else "No data"
        else:
            screen.emergency_text = "No emergency data saved."

        # Social
        social = customer.get("social", {})
        activities = social.get("activities", []) if social else []
        if activities:
            lines = [f"• {a.get('name', '')} — {a.get('frequency', '')}\n  {a.get('description', '')}" for a in activities]
            screen.social_text = "\n".join(lines)
        else:
            screen.social_text = "No social data saved."

        # Health
        health = customer.get("health", {})
        if health:
            conditions = ", ".join(health.get("conditions", []))
            screen.health_text = f"Conditions: {conditions}" if conditions else "No conditions"
        else:
            screen.health_text = "No health data saved."

        # Home
        appliances = customer.get("home", {}).get("appliances", [])
        if appliances:
            lines = [f"• {a.get('name', '')} — {a.get('status', '')} | Vendor: {a.get('vendor', 'N/A')}" for a in appliances]
            screen.home_text = "\n".join(lines)
        else:
            screen.home_text = "No home data saved."

        self.root.current = "detail"

    def go_back(self):
        self.root.current = "listing"

    def go_edit(self):
        if not self.current_customer:
            return
        c = self.current_customer
        screen = self.root.get_screen("edit")
        screen.ids.edit_name.text = c.get("name", "")
        screen.ids.edit_age.text = c.get("age", "")
        screen.ids.edit_mobile.text = c.get("mobile", "")
        screen.ids.edit_location.text = c.get("location", "")

        em = c.get("emergency", {})
        screen.ids.edit_hospital.text = em.get("hospital", "")
        screen.ids.edit_er_phone.text = em.get("er_phone", "")
        screen.ids.edit_doctor.text = em.get("doctor", "")
        screen.ids.edit_primary.text = em.get("primary_contact", "")

        social = c.get("social", {})
        activities = social.get("activities", [])
        if activities:
            screen.ids.edit_social_name.text = activities[0].get("name", "")
            screen.ids.edit_social_freq.text = activities[0].get("frequency", "")
            screen.ids.edit_social_desc.text = activities[0].get("description", "")
        else:
            screen.ids.edit_social_name.text = ""
            screen.ids.edit_social_freq.text = ""
            screen.ids.edit_social_desc.text = ""

        self.root.current = "edit"

    def go_detail(self):
        self.root.current = "detail"

    def save_edit(self):
        screen = self.root.get_screen("edit")
        collection = get_collection()

        updated = {
            "name": screen.ids.edit_name.text,
            "age": screen.ids.edit_age.text,
            "mobile": screen.ids.edit_mobile.text,
            "location": screen.ids.edit_location.text,
            "emergency": {
                "hospital": screen.ids.edit_hospital.text,
                "er_phone": screen.ids.edit_er_phone.text,
                "doctor": screen.ids.edit_doctor.text,
                "primary_contact": screen.ids.edit_primary.text,
            },
            "social": {"activities": [{
                "name": screen.ids.edit_social_name.text,
                "frequency": screen.ids.edit_social_freq.text,
                "description": screen.ids.edit_social_desc.text,
            }]} if screen.ids.edit_social_name.text else {"activities": []}
        }

        # Preserve health and home data
        if self.current_customer.get("health"):
            updated["health"] = self.current_customer["health"]
        if self.current_customer.get("home"):
            updated["home"] = self.current_customer["home"]

        collection.update_one(
            {"name": self.current_customer.get("name")},
            {"$set": updated},
            upsert=True
        )

        self.current_customer = updated
        self.show_detail(updated)


if __name__ == "__main__":
    EldaApp().run()
