# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivymd.toast import toast
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
import os

class Ui(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Brown'
        Builder.load_file('design.kv')
        return Ui()  

    def change_user(self):
        self.root.current = "password_screen"

    def verify_password(self, password):
        if password == "GIS":
            self.root.current = "config_mode_screen"
        else:
            toast("Contraseña incorrecta")

    def load_categoria(self, categoria):
        grid = self.root.get_screen("categoria_screen").ids.grid_pictos
        grid.clear_widgets()

        ruta = f"pics/{categoria}/"
        for filename in os.listdir(ruta):
            if filename.endswith(".png"):
                nombre = os.path.splitext(filename)[0].capitalize()

                card = MDCard(
                    orientation="vertical",
                    size_hint_y=None,
                    height="160dp",
                    md_bg_color=(1, 1, 0.996, 1),
                    padding="8dp",
                    spacing="4dp",
                    ripple_behavior=True,
                )
                img = Image(
                    source=os.path.join(ruta, filename),
                    size_hint_y=0.75,
                    allow_stretch=True,
                    keep_ratio=True,
                )
                titulo = MDCard(
                    size_hint_y=0.25,
                    md_bg_color=(0.76, 0.94, 0.79, 1),
                    radius=[8],
                    elevation=1,
                    padding=0,
                )
                label = MDLabel(
                    text=nombre,
                    halign="center",
                    font_name="fonts/ComicNeue-Bold.ttf"
                )
                titulo.add_widget(label)
                card.add_widget(img)
                card.add_widget(titulo)
                grid.add_widget(card)


    def mostrar_categoria(self, nombre_carpeta, titulo):
        self.root.current = "categoria_screen"

        def update_screen_text(*args):
            try:
                screen = self.root.get_screen("categoria_screen")
                print("Accediendo a screen:", screen.name)
                print("IDs disponibles:", screen.ids.keys())
                screen.ids.categoria_titulo.text = titulo
                self.load_categoria(nombre_carpeta)
            except Exception as e:
                print(" ERROR EN mostrar_categoria:", e)

        from kivy.clock import Clock
        Clock.schedule_once(update_screen_text, 0.1)




if __name__ == "__main__":
    MainApp().run()
