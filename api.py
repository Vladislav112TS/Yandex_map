import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

SCREEN_SIZE = [805, 450]


class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.long = 92.954818
        self.width = 55.989698
        self.zoom = 0.001
        self.type = "map"
        self.pt = False
        self.full_address = ''
        self.get_image()
        self.initUI()

    def ll(self):
        return str(self.long) + "," + str(self.width)

    def spn(self):
        return f'{self.zoom},{self.zoom}'

    def get_image(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params={'ll': self.ll(), 'spn': self.spn(), 'l': self.type,
                                                     'pt': self.pt if self.pt else ''})
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def update_pixmap(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def geocode(self):

        search_api_server = f"http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(search_api_server, params={'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                                                           'geocode': self.search_label.text(), 'format': 'json'})
        if response:
            return response
        print("Ошибка выполнения запроса:")
        print(search_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    def search(self):
        try:
            response = self.geocode()
            toponym = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            self.long = float(toponym["Point"]["pos"].split()[0])
            self.width = float(toponym["Point"]["pos"].split()[1])
            self.full_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            envelope = toponym['boundedBy']["Envelope"]
            l, b = envelope['lowerCorner'].split(' ')
            r, t = envelope['upperCorner'].split(' ')
            dx = abs(float(l) - float(r)) / 2.0
            dy = abs(float(b) - float(t)) / 2.0
            self.zoom = min(dx, dy)  # тут должно было быть две координары, но тогда пришлось переделывать передвижение
            self.pt = f'{self.ll()},pm2rdl'
            self.get_image()
            self.update_pixmap()
            self.image.setFocus()
            self.error.setText('')
            self.address.setText(self.full_address)

        except Exception:
            self.error.setText('Адрес не найден')
            self.address.setText('')
    
    def change_layer(self):
        layer_dict = {"Схема": "map", "Спутник": "sat", "Гибрид": "sat,skl"}
        self.type = layer_dict[self.sender().text()]
        self.get_image()
        self.update_pixmap()

    def reset(self):
        self.long = 92.954818
        self.width = 55.989698
        self.zoom = 0.001
        self.pt = False
        self.get_image()
        self.update_pixmap()
        self.image.setFocus()
        self.address.setText('')
        self.search_label.setText('')

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.update_pixmap()
        
        self.button_scheme = QPushButton('Схема', self)
        self.button_scheme.resize(60, 30)
        self.button_scheme.move(605, 0)
        self.button_scheme.clicked.connect(self.change_layer)
        
        self.button_satellite = QPushButton('Спутник', self)
        self.button_satellite.resize(60, 30)
        self.button_satellite.move(675, 0)
        self.button_satellite.clicked.connect(self.change_layer)
        
        self.button_hybrid = QPushButton('Гибрид', self)
        self.button_hybrid.resize(60, 30)
        self.button_hybrid.move(745, 0)
        self.button_hybrid.clicked.connect(self.change_layer)

        self.search_button = QPushButton('Поиск', self)
        self.search_button.resize(200, 30)
        self.search_button.move(605, 80)
        self.search_button.clicked.connect(self.search)

        self.search_label = QLineEdit(self)
        self.search_label.resize(200, 30)
        self.search_label.move(605, 40)

        self.reset_button = QPushButton('Сброс поискового результата', self)
        self.reset_button.resize(200, 30)
        self.reset_button.move(605, 120)
        self.reset_button.clicked.connect(self.reset)

        self.address = QLabel(self)
        self.address.resize(200, 50)
        self.address.move(605, 120)
        self.address.setWordWrap(True)

        self.error = QLabel(self)
        self.error.resize(200, 30)
        self.error.move(605, 160)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        step = 0.001
        if event.key() == Qt.Key_PageUp and self.zoom > 50:
            self.zoom += 0.001
        elif event.key() == Qt.Key_PageDown and self.zoom > 0.001:
            self.zoom -= 0.001
        elif event.key() == Qt.Key_Left and self.long < 170:
            self.long -= step
        elif event.key() == Qt.Key_Right and self.long < 170:
            self.long += step
        elif event.key() == Qt.Key_Up and self.width < 100:
            self.width += step
        elif event.key() == Qt.Key_Down and self.width < 100:
            self.width -= step
        self.get_image()
        self.update_pixmap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp = Map()
    mp.show()
    sys.exit(app.exec())
