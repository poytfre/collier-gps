from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.utils import platform

# Pour l'envoi de SMS, on utilise plyer (uniquement Android)
try:
    from plyer import sms
except ImportError:
    sms = None

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 20

        MDLabel:
            text: "Collier GPS - Demander Position"
            halign: "center"
            font_style: "H5"

        MDTextField:
            id: phonefield
            hint_text: "Numéro du collier (ex: +33612345678)"
            helper_text: "Entrer le numéro SIM du collier"
            helper_text_mode: "on_focus"

        MDRaisedButton:
            text: "Demander Position"
            on_release: app.send_position_sms()
            pos_hint: {"center_x": .5}

        MDTextField:
            id: smsresponse
            hint_text: "Réponse SMS du collier"
            helper_text: "Colle ici la réponse du collier (ex: LAT:48.85;LON:2.35)"
            helper_text_mode: "on_focus"

        MDRaisedButton:
            text: "Afficher sur la carte"
            on_release: app.show_on_map()
            pos_hint: {"center_x": .5}

        MDLabel:
            id: resultlabel
            text: ""
            halign: "center"
'''

class GPSCollarApp(MDApp):
    def build(self):
        self.title = "Collier GPS"
        return Builder.load_string(KV)

    def send_position_sms(self):
        number = self.root.ids.phonefield.text.strip()
        if not number:
            self.root.ids.resultlabel.text = "[color=ff0000]Veuillez saisir le numéro du collier.[/color]"
            return
        if platform != "android" or sms is None:
            self.root.ids.resultlabel.text = "[color=ff0000]L’envoi de SMS ne fonctionne que sur Android.[/color]"
            return
        try:
            sms.send(recipient=number, message="POS?")
            self.root.ids.resultlabel.text = "[color=00ff00]SMS envoyé au collier ![/color]"
        except Exception as e:
            self.root.ids.resultlabel.text = f"[color=ff0000]Erreur SMS : {e}[/color]"

    def show_on_map(self):
        msg = self.root.ids.smsresponse.text.strip()
        import re, webbrowser
        m = re.search(r"([Ll][Aa][Tt] *: *([\d\.\-]+))[^0-9\-]*([Ll][Oo][Nn] *: *([\d\.\-]+))", msg)
        if not m:
            self.root.ids.resultlabel.text = "[color=ff0000]Format incorrect. Ex: LAT:48.85;LON:2.35[/color]"
            return
        lat = m.group(2)
        lon = m.group(4)
        self.root.ids.resultlabel.text = f"[color=00ff00]Position détectée : {lat}, {lon}[/color]"
        url = f"https://maps.google.com/?q={lat},{lon}"
        try:
            webbrowser.open(url)
        except Exception:
            pass

if __name__ == "__main__":
    GPSCollarApp().run()