

import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import emoji

class Wapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter le nom de la ville :", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Afficher", self)
        self.temperature_label = QLabel( self)
        self.emoji_label = QLabel( self)
        self.decription_label = QLabel( self)
        self.initui()

    def initui(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.decription_label)

        self.setLayout(vbox)

        # Centrer les items
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.decription_label.setAlignment(Qt.AlignCenter)

        # Nommer les widgets
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.decription_label.setObjectName("decription_label")

        # Style sheet
        self.setStyleSheet("""
        
            QLabel, QPushButton {
                font-family: calibri;
                background-color: #4e03fc;
             
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                  font-size: 40px;
                  font-family: "Montserrat", sans-serif;
                  width: 100%;
                  height: 45px;
                  padding-left: 2.5rem;
                  box-shadow: 0 0 0 1.5px #2b2c37, 0 0 25px -17px #000;
                  border: 0;
                  border-radius: 12px;
                  background-color: #FFFFFF;
                  outline: none;
                  color: #000000;
                  transition: all 0.25s cubic-bezier(0.19, 1, 0.22, 1);
                  cursor: text;
                  z-index: 0;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
                background-color: #eee;
             }                
                           
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#decription_label {
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "c7492b54bea0580d70b4bfd5dfb26e00"
        city = self.city_input.text()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            print (data)

            if data["cod"] != 200:
                self.temperature_label.setText("City not found")
                self.emoji_label.setText("")
                self.decription_label.setText("")
                return

            temperature = data["main"]["temp"]
            weather_condition = data["weather"][0]["main"]
            description = data["weather"][0]["description"]
            print (description)

            self.temperature_label.setText(f"{temperature}°C")
            self.decription_label.setText(description.capitalize())

            # Set emoji based on weather condition
            if weather_condition == "Clear":
                self.emoji_label.setText("☀️")
            elif weather_condition == "Clouds":
                self.emoji_label.setText(emoji.emojize("\U0001F325"))
            elif weather_condition == "Rain":
                self.emoji_label.setText("⛈️")
            elif weather_condition == "Snow":
                self.emoji_label.setText(emoji.emojize("\U00002603"))
            else:
                self.emoji_label.setText("🌍")

        except requests.exceptions.RequestException :
            self.temperature_label.setText("ville non trouvable")
            self.emoji_label.setText(emoji.emojize(":cross_mark:"))
            self.decription_label.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = Wapp()
    weather_app.show()
    sys.exit(app.exec_())