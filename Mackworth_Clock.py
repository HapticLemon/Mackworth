import sys
from datetime import datetime
from datetime import timedelta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from random import randint

# Aplicación basada en el experimento clásico del reloj de Mackworth.
# TODO : Montar algún sistema de checks para escoger la duración de la prueba.

class App(QWidget):
    eventos_producidos = 0
    eventos_contados = 0
    hora_actual = datetime.now()
    hora_final = hora_actual + timedelta(minutes=1)
    timer = QTimer()

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)  # these values change where the main window is placed
        self.title = 'Test de atención'
        self.initUI()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)


    # Definición de la ventana y sus componentes.
    #
    def initUI(self):


        self.setGeometry(500, 500, 510, 150)
        self.setWindowTitle('Icon')

        self.qbtn = QPushButton('Event', self)
        self.qbtn.setGeometry(QtCore.QRect(400, 50, 100, 50))
        self.qbtn.clicked.connect(self.buttonClicked)

        # Definición del LCD que usaré para el contador de eventos detectados.
        self.raisedDisplay = QLCDNumber(self)
        self.raisedDisplay.setGeometry(QtCore.QRect(200, 50, 100, 50))
        self.raisedDisplay.setSegmentStyle(QLCDNumber.Flat)
        self.raisedDisplay.setDigitCount(3)
        self.raisedDisplay.display('0')

        # Definición del LCD que usaré para el contador de eventos detectados.
        self.detectedDisplay = QLCDNumber(self)
        self.detectedDisplay.setGeometry(QtCore.QRect(300, 50, 100, 50))
        self.detectedDisplay.setSegmentStyle(QLCDNumber.Flat)
        self.detectedDisplay.setDigitCount(3)
        self.detectedDisplay.display('0')

        # Definición del LCD que usaré para el reloj.
        self.timeDisplay = QLCDNumber(self)
        self.paleta = self.timeDisplay.palette()
        back = self.timeDisplay.backgroundRole()
        fore = self.timeDisplay.foregroundRole()
        self.paleta.setColor(back, Qt.black)
        self.paleta.setColor(fore, Qt.green)
        self.timeDisplay.setPalette(self.paleta)
        self.timeDisplay.setAutoFillBackground(True)

        self.timeDisplay.setGeometry(QtCore.QRect(10, 50, 200, 50))
        self.timeDisplay.setSegmentStyle(QLCDNumber.Flat)
        self.timeDisplay.setDigitCount(8)
        self.timeDisplay.display('00:00:00')

        self.show()

    # Cada vez que pulsamos el botón se incrementa el contador de eventos
    # detectados al tiempo que la etiqueta queda actualizada.
    #
    def buttonClicked(self):
        sender = self.sender()
        self.eventos_contados += 1
        self.detectedDisplay.display(self.eventos_contados)

    # El tiempo de proceso ha terminado, así que se muestran los eventos
    # ocurridos.
    # TODO : Mostrar un mensaje indicando si los contadores coinciden.
    # TODO : Desactivar el botón de Evento.
    #
    def muestraResultado(self):
        self.raisedDisplay.display(self.eventos_producidos)
        self.timer.stop()

    # Actualiza la etiqueta de tiempo. Hay una posibilidad entre 10 de que
    # el reloj se "pare" durante un segundo, precisamente el evento que debe
    # detectarse.
    #
    def updateTime(self):
        # Comprobamos si es la hora de terminar con el proceso.
        self.hora_actual = datetime.now()
        if (self.hora_actual >= self.hora_final):
            muestraResultado()

        if (randint(0, 9) == 0):
            # Restamos un segundo de la hora. El efecto es que queda "congelada"
            dt_delta = datetime.now() - timedelta(seconds=1)
            time = dt_delta.time().strftime("%H:%M:%S")
            self.eventos_producidos += 1
            print(self.eventos_producidos)
        else :
            # Se calcula la hora normal.
            dt = datetime.now()
            time = dt.time().strftime("%H:%M:%S")

        # Antes actualizaba etiqueta, ahora actualizo el LCD.
        self.timeDisplay.display(time)

def main():
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()