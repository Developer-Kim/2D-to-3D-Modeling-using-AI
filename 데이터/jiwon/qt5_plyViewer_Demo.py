# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0 jeong hwan kim
#
# WARNING! All changes made in this file will be lost!
import os
import subprocess
import sys
import pptk
import numpy as np
import plyfile
from wmctrl import Window
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QRect
from subprocess import call
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QApplication

# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/home/jiwon/openMVG_Build/Linux-x86_64-RELEASE"
# Indicate the openMVG camera sensor width directory
CAMERA_SENSOR_WIDTH_DIRECTORY = "/home/jiwon/openMVG/src/software/SfM" + "/../../openMVG/exif/sensor_width_database"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(879, 737)
        

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(680, 550, 191, 71))
        self.pushButton.clicked.connect(self.start_button)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 630, 191, 71))
        #버튼이벤트 연결
        self.pushButton_2.clicked.connect(self.exit_button)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Create combobox and add items.
        self.comboBox = QComboBox(MainWindow)
        self.comboBox.setGeometry(QRect(680, 10, 100, 30)) #x좌표,y좌표,가로길이,세로길이
        self.comboBox.setObjectName(("comboBox"))
        self.comboBox.addItem("PyQt")
        self.comboBox.addItem("Qt")
        self.comboBox.addItem("Python")
        self.comboBox.addItem("Example")

        #메인 창에 pptk viewer 띄우기
        #widget = QtWidgets.QWidget(MainWindow)
        self.layout = QtWidgets.QGridLayout(self.centralwidget)
        #MainWindow.setCentralWidget(self.centralwidget)
        data = plyfile.PlyData.read('scene_dense.ply')['vertex']

        xyz = np.c_[data['x'], data['y'], data['z']]
        rgb = np.c_[data['red'], data['green'], data['blue']]
        self.v = pptk.viewer(xyz)
        self.v.set(point_size=0.0005)
        self.v.attributes(rgb / 255.)
        #self.v.wait()
        viwerWinID_str = subprocess.getoutput("wmctrl -l | grep -i viewer | awk '{print $1}'") #get window id in str
        print(viwerWinID_str)
        viwerWinID_int = int(viwerWinID_str, 16)    # str to int
        print(viwerWinID_int)
        viwerWinID = viwerWinID_int + 0x200         # int to hex
        print(viwerWinID)
        self.window = QtGui.QWindow.fromWinId(0x06600004)    
        self.windowcontainer = QWidget.createWindowContainer(self.window, self.centralwidget)
        self.layout.addWidget(self.windowcontainer, 0, 0)
        
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "START"))
        self.pushButton_2.setText(_translate("MainWindow", "EXIT"))

    
    def start_button(self):
        print("==============================tutorial_demo.py 실행==============================")
        tutorial_demo_py()
        print("==============================tutorial_demo.py 완료==============================")
        print("==============================openMVG_main_openMVG2openMVS 실행==============================")
        os.chdir("/Users/hwan/Desktop/openMVG_Build/Darwin-x86_64-RELEASE/Release")
        os.system("./openMVG_main_openMVG2openMVS -i /Users/hwan/Desktop/openMVG_Build/software/SfM/tutorial_out_3/reconstruction_global/sfm_data.bin -o /Users/hwan/Desktop/openMVS_build/bin/scene.mvs -d /Users/hwan/Desktop/openMVS_build/bin/scene_undistorted_images")
        print("==============================openMVG_main_openMVG2openMVS 완료==============================")
        print("==============================DensifyPointCloud 실행==============================")
        os.chdir("/Users/hwan/Desktop/openMVS_build/bin")
        os.system("./DensifyPointCloud scene.mvs")
        print("==============================DensifyPointCloud 완료==============================")
        print("==============================ReconstructMesh 실행==============================")
        os.system("./ReconstructMesh scene_dense.mvs")
        print("==============================ReconstructMesh 완료==============================")
        print("==============================RefineMesh 실행==============================")
        os.system("./RefineMesh scene_dense_mesh.mvs --max-face-area 16")
        print("==============================RefineMesh 완료==============================")
        print("==============================TextureMesh 실행==============================")
        os.system("./TextureMesh scene_dense_mesh_refine.mvs")
        print("==============================TextureMesh 완료==============================")
        
    def exit_button(self):
        print("종료")
        sys.exit()
        
        
if __name__ == "__main__":
    def tutorial_demo_py():
        def get_parent_dir(directory):
            return os.path.dirname(directory)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        input_eval_dir = os.path.abspath("/Users/hwan/Desktop/openMVG_Build/software/SfM/ImageDataset_SceauxCastle")
        # Checkout an OpenMVG image dataset with Git
        if not os.path.exists(input_eval_dir):
          pImageDataCheckout = subprocess.Popen([ "git", "clone", "https://github.com/openMVG/ImageDataset_SceauxCastle.git" ])
          pImageDataCheckout.wait()

        output_eval_dir = os.path.join(get_parent_dir(input_eval_dir), "tutorial_out_3")
        input_eval_dir = os.path.join(input_eval_dir, "images")
        if not os.path.exists(output_eval_dir):
          os.mkdir(output_eval_dir)

        input_dir = input_eval_dir
        output_dir = output_eval_dir
        print ("Using input dir  : ", input_dir)
        print ("      output_dir : ", output_dir)

        matches_dir = os.path.join(output_dir, "matches")
        camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")

        # Create the ouput/matches folder if not present
        if not os.path.exists(matches_dir):
          os.mkdir(matches_dir)

        print ("1. Intrinsics analysis")
        pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params, "-c", "3"] )
        pIntrisics.wait()

        print ("2. Compute features")
        pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"), "-p", "HIGH", "-i", matches_dir+"/sfm_data.json", "-o", matches_dir,"-f", "1", "-m", "SIFT", "-n" , "4"] )
        pFeatures.wait()

        print ("2. Compute matches")
        pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-f", "1", "-n", "ANNL2", "-r", ".8"] )
        pMatches.wait()

        reconstruction_dir = os.path.join(output_dir,"reconstruction_sequential")
        print ("3. Do Incremental/Sequential reconstruction") #set manually the initial pair to avoid the prompt question
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
        pRecons.wait()

        print ("5. Colorize Structure")
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
        pRecons.wait()

        print ("4. Structure from Known Poses (robust triangulation)")
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
        pRecons.wait()

        # Reconstruction for the global SfM pipeline
        # - global SfM pipeline use matches filtered by the essential matrices
        # - here we reuse photometric matches and perform only the essential matrix filering
        print ("2. Compute matches (for the global SfM Pipeline)")
        pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-r", "0.8", "-g", "e"] )
        pMatches.wait()

        reconstruction_dir = os.path.join(output_dir,"reconstruction_global")
        print ("3. Do Global reconstruction")
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_GlobalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
        pRecons.wait()

        print ("5. Colorize Structure")
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
        pRecons.wait()

        print ("4. Structure from Known Poses (robust triangulation)")
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
        pRecons.wait()
        
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
