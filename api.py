import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]
class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.long = 92.954818
        self.width = 55.989698
        self.zoom = 0.001
        self.type = "map"
        self.get_image()
        self.initUI()

    def ll(self):
        return str(self.long) + "," + str(self.width)

    def spn(self):
        return str(self.zoom) + "," + str(self.zoom)

    def get_image(self):
        map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l={type}".format(ll=self.ll(), spn=self.spn(),
                                                                                        type=self.type)
        response = requests.get(map_request)
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

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.update_pixmap()

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
