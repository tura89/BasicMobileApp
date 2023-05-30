import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('design.kv')


class MainScreen(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    @staticmethod
    def get_city(data):
        """Get the most likely entry."""
        for entry in data:
            if entry['type'] in ['town', 'city']:
                return entry

        return data[0]

    def find(self, city):
        target_url = F'https://nominatim.openstreetmap.org/search?q={city}&format=json'
        if not city:
            return

        try:
            data = requests.get(target_url, timeout=10).json()
            data = self.get_city(data)
            self.ids.coordinates.text = F"{city} Latitude: {data['lat']}, Longitude: {data['lon']}"
        except Exception as ex:
            self.ids.coordinates.text = str(ex)


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
