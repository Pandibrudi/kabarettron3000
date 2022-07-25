from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from jokes import Punchliner
import vlc


class P(FloatLayout):
        pass

class Interface(Widget):
    pl = Punchliner()
    output = ObjectProperty(None)
    input_city = ObjectProperty(None)
    input_topics = ObjectProperty(1)
    input_name = ObjectProperty(None)
    read_aloud_check = ObjectProperty(None)
    
    def generate(self):
        self.city = self.input_city.text
        self.topics = int(self.input_topics.value)

        if self.read_aloud_check.active:
            joke = self.pl.make_audio(self.city, self.topics)
            self.output.text = joke[1]
            self.filename = joke[0]
            self.media = vlc.MediaPlayer(self.filename)
            self.media.play()

        else:
            joke = self.pl.make_comedy_set(self.city, self.topics)
            self.output.text = joke
    
    def show_popup_loaded_news(self):
        show = P() 
        popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(400,400)) 
        popupWindow.open()       

    def load_news(self):
        self.pl.update_news()
        self.show_popup_loaded_news()

class mainApp(App):

    def build(self):
        return Interface()

        
if __name__ == "__main__":
    mainApp().run()