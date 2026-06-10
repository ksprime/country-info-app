"""
Country Information App

A desktop application built with Python and PyQt5 that retrieves
country information from the REST Countries API.

Features:
- Country search
- Capital city lookup
- Population data
- Region information
- Currency information
- Country flag display
- Error handling

Author: Kelvin Agidigbi
"""

import sys
import requests

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLabel, QLineEdit, QVBoxLayout)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class CountryApp(QWidget):
    def __init__(self):
        super(). __init__()
        self.search_label = QLabel("Enter a country: ", self)
        self.search_input = QLineEdit(self)
        self.get_info_button = QPushButton("Get Info", self)
        self.country_label = QLabel(self)
        self.capital_label = QLabel(self)
        self.population_label = QLabel(self)
        self.region_label = QLabel(self)
        self.currency_label = QLabel(self)
        self.flag_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Country Info App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.search_label)
        vbox.addWidget(self.search_input)
        vbox.addWidget(self.get_info_button)
        vbox.addWidget(self.country_label)
        vbox.addWidget(self.capital_label)
        vbox.addWidget(self.population_label)
        vbox.addWidget(self.region_label)
        vbox.addWidget(self.currency_label)
        vbox.addWidget(self.flag_label)

        self.setLayout(vbox)

        self.search_label.setAlignment(Qt.AlignCenter)
        self.search_input.setAlignment(Qt.AlignCenter)
        self.country_label.setAlignment(Qt.AlignCenter)
        self.capital_label.setAlignment(Qt.AlignCenter)
        self.population_label.setAlignment(Qt.AlignCenter)
        self.region_label.setAlignment(Qt.AlignCenter)
        self.currency_label.setAlignment(Qt.AlignCenter)
        self.flag_label.setAlignment(Qt.AlignCenter)

        self.search_label.setObjectName("search_label")
        self.search_input.setObjectName("search_input")
        self.get_info_button.setObjectName("get_info_button")
        self.country_label.setObjectName("country_label")
        self.capital_label.setObjectName("capital_label")
        self.population_label.setObjectName("population_label")
        self.region_label.setObjectName("region_label")
        self.currency_label.setObjectName("currency_label")
        self.flag_label.setObjectName("flag_label")

        self.setStyleSheet("""
             QPushButton, QLabel{
                 font-size: 35px;
                 font-family: calibri;
             }
             QLabel#search_label{
                 font-style: italic;
             }
             QLineEdit#search_input{
                 font-size: 30px;
                 
             }
             QPushButton#get_info_button{
                 font-size: 45px;
                 font-weight: bold;
             }
            
        """)


        self.get_info_button.clicked.connect(self.get_country_info)

    def get_country_info(self):
        country = self.search_input.text()
        url = f"https://restcountries.com/v3.1/name/{country}"


        try:

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.display_info(data)

        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                self.display_error("Country not Found")
            else:
                self.display_error(f"HTTP Error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            self.display_error("Check your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Request timed out")

        except requests.exceptions.RequestException as e:
            self.display_error(f"Failed to Retrieve Data:\n{e}")


    def display_error(self, message):
        self.country_label.setText(message)
        self.capital_label.clear()
        self.population_label.clear()
        self.region_label.clear()
        self.currency_label.clear()
        self.flag_label.clear()

    def display_info(self, data):
        country = data[0]['name']['official']
        capital = data[0]['capital'][0]
        population = data[0]['population']
        region = data[0]['region']
        currency = data[0]['currencies']
        flag = data[0]['flags']['png']



        self.country_label.setText(f"Country: {country}")
        self.capital_label.setText(f"Capital: {capital}")
        self.population_label.setText(f"Population: {population}")
        self.region_label.setText(f"Region: {region}")
        for currency_code, currency_info in currency.items():
            self.currency_label.setText(f"Currency: {currency_info['name']}")
        self.get_flags(flag)


    def get_flags(self, flag_url):
        response = requests.get(flag_url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)

        self.flag_label.setPixmap(pixmap)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    country_app = CountryApp()
    country_app.show()
    sys.exit(app.exec_())