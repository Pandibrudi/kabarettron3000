from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from jokes import Punchliner
import vlc

Window.size = (1920, 1080)

class Interface(Widget):
    pl = Punchliner()
    output = ObjectProperty(None)
    input_city = ObjectProperty(None)
    input_topics = ObjectProperty(1)
    input_punchlines = ObjectProperty(1)
    input_name = ObjectProperty(None)
    read_aloud_check = ObjectProperty(None)
    
    def generate(self):
        self.city = self.input_city.text
        self.name = self.input_name.text
        self.topics = int(self.input_topics.value)
        self.punchlines = int(self.input_punchlines.value)

        if self.read_aloud_check.active:#muss noch angepasst werden
            joke = self.pl.make_audio(self.city, self.name, self.topics, self.punchlines)#also hier die arguments 
            self.output.text = joke[1]
            self.filename = joke[0]
            self.media = vlc.MediaPlayer(self.filename)
            self.media.play()

        else:
            joke = self.pl.make_comedy_set(self.city, self.name, self.topics, self.punchlines)
            self.output.text = joke

    def stop(self):
        try:
            self.media.stop()
        except:
            pass

    def clear(self):
        try:
            self.output.text = ""
        except:
            pass
    
    def show_popup_loaded_news(self):
        show = Label(text="Die aktuellen Nachrichten wurden geladen!") 
        popupWindow = Popup(title="News geladen", content=show, size_hint=(None,None),size=(400,400)) 
        popupWindow.open()       

    def load_news(self):
        self.pl.update_news()
        self.show_popup_loaded_news()

class mainApp(App):

    def build(self):
        self.icon = 'ico/lol.ico'
        self.title = 'Kabaretttron 3000'
        return Interface()

        
if __name__ == "__main__":
    mainApp().run()