# Importieren der erforderlichen Module
import sys  # Modul zum Zugriff auf Systemfunktionen
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QListWidget, QMessageBox  # Import von Klassen und Funktionen aus PyQt5-Modulen
import cv2  # OpenCV-Bibliothek für Bildverarbeitung
import numpy as np  # Bibliothek für numerische Berechnungen
import moviepy.editor as mp  # MoviePy-Bibliothek zum Bearbeiten von Videos

# Liste der verfügbaren Effekte und Auflösungen
effects = ["Schwarz-Weiß", "Spiegel", "Negativ", "Sepia", "Kacheln", "Glow", "Film Grain", "Noise", "Vignette", "Distortion"]  # Liste der verfügbaren Videoeffekte
resolutions = ["VGA: 640×480", "XGA: 1024×768", "HD-ready: 1280×720", "Full-HD: 1920×1080", "UHD-4k: 3840×2160"]  # Liste der verfügbaren Auflösungen

# Definition der Hauptklasse für den Video-Editor
class VideoEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Methode zur Initialisierung der Benutzeroberfläche
    def initUI(self):
        self.setWindowTitle('Video-Editor by Ralf Krümmel')  # Festlegen des Fenstertitels

        # Erstellen von Widgets für die Benutzeroberfläche
        self.video_label = QLabel('Wähle ein Video aus:')  # Label für die Auswahl des Videos
        self.video_path = QLineEdit()  # Eingabefeld für den Dateipfad des Videos
        self.video_browse_button = QPushButton('Durchsuchen...')  # Schaltfläche zum Durchsuchen des Dateisystems
        self.video_browse_button.clicked.connect(self.browseVideo)  # Verknüpfung der Schaltfläche mit einer Methode

        self.effect_label = QLabel('Wähle einen CGI-Effekt aus:')  # Label für die Auswahl des Effekts
        self.effect_list = QListWidget()  # Listbox für die Auswahl des Effekts
        self.effect_list.addItems(effects)  # Hinzufügen der Effekte zur Listbox

        self.resolution_label = QLabel('Wähle eine Auflösung aus:')  # Label für die Auswahl der Auflösung
        self.resolution_list = QListWidget()  # Listbox für die Auswahl der Auflösung
        self.resolution_list.addItems(resolutions)  # Hinzufügen der Auflösungen zur Listbox

        self.speed_label = QLabel('Eingabe der Geschwindigkeit (langsamer mit - davor und schneller ohne - davor. Werte zwischen -10 und +10):')  # Label für die Eingabe der Geschwindigkeit
        self.speed_input = QLineEdit()  # Eingabefeld für die Geschwindigkeit

        self.kacheln_label = QLabel('Eingabe der Farbwerte für Kachel-Effekt 0.1 0.6 0.2 (falls ausgewählt):')  # Label für die Eingabe der Farbwerte
        self.kacheln_input = QLineEdit()  # Eingabefeld für die Farbwerte

        self.apply_button = QPushButton('Anwenden')  # Schaltfläche zum Anwenden der Effekte
        self.apply_button.clicked.connect(self.applyEffect)  # Verknüpfung der Schaltfläche mit einer Methode

        self.cancel_button = QPushButton('Abbrechen')  # Schaltfläche zum Abbrechen
        self.cancel_button.clicked.connect(self.close)  # Verknüpfung der Schaltfläche mit der Schließmethode des Fensters

        # Anordnung der Widgets mit Layout-Managern
        vbox = QVBoxLayout()  # Vertikales Layout für das Hauptfenster
        vbox.addWidget(self.video_label)  # Hinzufügen des Videolabels zum Layout
        hbox_video = QHBoxLayout()  # Horizontales Layout für die Videodateiauswahl
        hbox_video.addWidget(self.video_path)  # Hinzufügen des Pfad-Eingabefelds zum Layout
        hbox_video.addWidget(self.video_browse_button)  # Hinzufügen der Durchsuchen-Schaltfläche zum Layout
        vbox.addLayout(hbox_video)  # Hinzufügen des horizontalen Layouts zum Hauptlayout
        vbox.addWidget(self.effect_label)  # Hinzufügen des Effektlabels zum Hauptlayout
        vbox.addWidget(self.effect_list)  # Hinzufügen der Effektauswahl zur Hauptlayout
        vbox.addWidget(self.resolution_label)  # Hinzufügen des Auflösungslabels zum Hauptlayout
        vbox.addWidget(self.resolution_list)  # Hinzufügen der Auflösungsauswahl zur Hauptlayout
        vbox.addWidget(self.speed_label)  # Hinzufügen des Geschwindig

        vbox.addWidget(self.speed_input)
        vbox.addWidget(self.kacheln_label)
        vbox.addWidget(self.kacheln_input)
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.apply_button)
        hbox_buttons.addWidget(self.cancel_button)
        vbox.addLayout(hbox_buttons)

        self.setLayout(vbox)

    def browseVideo(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Video Files (*.mp4 *.avi)")
        if fileName:
            self.video_path.setText(fileName)

    def applyEffect(self):
        video_path = self.video_path.text()
        effect = self.effect_list.currentItem().text()
        resolution = self.resolution_list.currentItem().text()
        speed = self.speed_input.text()
        kacheln_values = self.kacheln_input.text()

        if video_path and effect and resolution:
            new_clip = apply_effect(video_path, effect, resolution, speed, kacheln_values)
            new_video = video_path.split(".")[0] + "_" + effect + ".mp4"
            new_clip.write_videofile(new_video)
            self.showPopup("Das neue Video wurde gespeichert als " + new_video)
        else:
            self.showPopup("Bitte wählen Sie ein Video, einen Effekt und eine Auflösung aus.")

    def showPopup(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.exec_()

def glow_effect(img):
    blur = cv2.GaussianBlur(255 - img, (0, 0), 1, 1)
    img_glow = cv2.addWeighted(img, 2.5, blur, -0.5, 2)
    return img_glow

def film_grain_effect(img):
    grain = np.random.normal(0, 3.6, img.shape)
    img_grain = np.clip(img + grain, 0, 255)
    return img_grain.astype(np.uint8)

def noise_effect(img):
    noise = np.random.normal(0, 2.05, img.shape)
    img_noise = np.clip(img + noise, 0, 255)
    return img_noise.astype(np.uint8)

def vignette_effect(img):
    rows, cols = img.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, 200)
    kernel_y = cv2.getGaussianKernel(rows, 200)
    kernel = kernel_y * kernel_x.T
    mask = kernel / np.linalg.norm(kernel)
    img_vignette = img * mask
    return img_vignette.astype(np.uint8)

def distortion(img):
    height, width = img.shape[:2]
    map_x, map_y = np.indices((height, width), dtype=np.float32)
    map_x = 2*map_x/(width-1) - 1
    map_y = 2*map_y/(height-1) - 1
    r, theta = cv2.cartToPolar(map_x, map_y)
    r[r < 1] = r[r < 1]**1.5
    map_x, map_y = cv2.polarToCart(r, theta)
    map_x = ((map_x + 1)*width - 1)/2
    map_y = ((map_y + 1)*height - 1)/2
    distorted_img = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return distorted_img

def apply_effect(video, effect, resolution, speed, kacheln_values=None):
    clip = mp.VideoFileClip(video)
    if effect == "Schwarz-Weiß":
        clip = clip.fx(mp.vfx.blackwhite)
    elif effect == "Spiegel":
        clip = clip.fx(mp.vfx.mirror_x)
    elif effect == "Negativ":
        clip = clip.fx(mp.vfx.invert_colors)
    elif effect == "Sepia":
        clip = clip.fl_image(sepia)
    elif effect == "Kacheln":
        clip = clip.fl_image(lambda image: kacheln(image, kacheln_values))
    elif effect == "Glow":
        clip = clip.fl_image(lambda image: glow_effect(image))
    elif effect == "Film Grain":
        clip = clip.fl_image(lambda image: film_grain_effect(image))
    elif effect == "Noise":
        clip = clip.fl_image(lambda image: noise_effect(image))
    elif effect == "Vignette":
        clip = clip.fl_image(lambda image: vignette_effect(image))
    elif effect == "Distortion":
        clip = clip.fl_image(lambda image: distortion(image))
    if speed:
        speed = float(speed)
        if speed < 0:
            clip = clip.fx(mp.vfx.speedx, 1 - abs(speed)/10)
        else:
            clip = clip.fx(mp.vfx.speedx, 1 + speed/10)
    resolution = resolution.split(": ")[1].split("×")
    clip = clip.resize(height=int(resolution[1]), width=int(resolution[0]))
    return clip

def sepia(image):
    sepia_image = np.dot(image[...,:3], [[0.769, 0.189, 0.0],
                                         [0.686, 0.189, 0.0],
                                         [0.272, 0.543, 0.131]])
    sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
    return sepia_image

def kacheln(image, values):
    kacheln_values = np.array(values.split(' '), dtype=float)
    kacheln_image = np.dot(image[...,:3], kacheln_values)
    kacheln_image = np.clip(kacheln_image, 0, 255 ).astype(np.uint8)
    return kacheln_image

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = VideoEditor()
    editor.show()
    sys.exit(app.exec_())

