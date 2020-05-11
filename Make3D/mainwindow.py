# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!

import os
import subprocess
import sys
#import pptk
import math
import string
import numpy as np
#import plyfile
import cv2
#from wmctrl import Window
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

#option Dictionary 
# ex option["features"]["-m"] = SIFT
option = dict()
option["features"] = dict()
option["matches"] = dict()
option["seq"] = dict()
option["densify"] = dict()
option["mesh"] = dict()
option["refine"] = dict()
option["texture"] = dict()


program_dir = os.getcwd()
input_dir = os.path.join(program_dir, "Image")
ChangeWhite_dir = ""
matches_dir = ""
reconstruction_dir = ""
Scene_dir = ""
output_dir = ""

OPENMVG_SFM_BIN = os.path.join(program_dir, "Binary")
CAMERA_SENSOR_WIDTH_DIRECTORY = os.path.join(program_dir, "Camera")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 781, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.v1_widget = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.v1_widget.setObjectName("v1_widget")
        self.btn_outputPath = QtWidgets.QPushButton(self.v1_widget)
        self.btn_outputPath.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.btn_outputPath.setObjectName("btn_outputPath")
        self.comboBox = QtWidgets.QComboBox(self.v1_widget)
        self.comboBox.setGeometry(QtCore.QRect(590, 10, 181, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout_1.addWidget(self.v1_widget)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 70, 781, 431))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.v2_widget = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        self.v2_widget.setObjectName("v2_widget")

        #Compute Features options
        self.groupBox_computeFeatures = QtWidgets.QGroupBox(self.v2_widget)
        self.groupBox_computeFeatures.setGeometry(QtCore.QRect(590, 10, 181, 411))
        self.groupBox_computeFeatures.setObjectName("groupBox_computeFeatures")
        self.radioBtn_SIFT = QtWidgets.QRadioButton(self.groupBox_computeFeatures)
        self.radioBtn_SIFT.setGeometry(QtCore.QRect(20, 50, 112, 23))
        self.radioBtn_SIFT.setObjectName("radioBtn_SIFT")
        self.DescriberMethodGroup = QtWidgets.QButtonGroup(MainWindow)
        self.DescriberMethodGroup.setObjectName("DescriberMethodGroup")
        self.DescriberMethodGroup.addButton(self.radioBtn_SIFT)
        self.DescriberMethod = QtWidgets.QLabel(self.groupBox_computeFeatures)
        self.DescriberMethod.setGeometry(QtCore.QRect(10, 30, 161, 17))
        self.DescriberMethod.setObjectName("DescriberMethod")
        self.radioBtn_AKAZE_FLOAT = QtWidgets.QRadioButton(self.groupBox_computeFeatures)
        self.radioBtn_AKAZE_FLOAT.setGeometry(QtCore.QRect(20, 70, 131, 23))
        self.radioBtn_AKAZE_FLOAT.setObjectName("radioBtn_AKAZE_FLOAT")
        self.DescriberMethodGroup.addButton(self.radioBtn_AKAZE_FLOAT)
        self.radioBtn_AKAZE_MLDE = QtWidgets.QRadioButton(self.groupBox_computeFeatures)
        self.radioBtn_AKAZE_MLDE.setGeometry(QtCore.QRect(20, 90, 141, 23))
        self.radioBtn_AKAZE_MLDE.setObjectName("radioBtn_AKAZE_MLDE")
        self.DescriberMethodGroup.addButton(self.radioBtn_AKAZE_MLDE)
        self.Upright = QtWidgets.QLabel(self.groupBox_computeFeatures)
        self.Upright.setGeometry(QtCore.QRect(10, 130, 161, 17))
        self.Upright.setObjectName("Upright")
        self.radioBtn_0 = QtWidgets.QRadioButton(self.groupBox_computeFeatures)
        self.radioBtn_0.setGeometry(QtCore.QRect(20, 150, 112, 23))
        self.radioBtn_0.setObjectName("radioBtn_0")
        self.UprightGroup = QtWidgets.QButtonGroup(MainWindow)
        self.UprightGroup.setObjectName("UprightGroup")
        self.UprightGroup.addButton(self.radioBtn_0)
        self.radioBtn_1 = QtWidgets.QRadioButton(self.groupBox_computeFeatures)
        self.radioBtn_1.setGeometry(QtCore.QRect(20, 170, 112, 23))
        self.radioBtn_1.setObjectName("radioBtn_1")
        self.UprightGroup.addButton(self.radioBtn_1)
        self.Preset = QtWidgets.QLabel(self.groupBox_computeFeatures)
        self.Preset.setGeometry(QtCore.QRect(10, 200, 161, 17))
        self.Preset.setObjectName("Preset")
        self.radioBtn_NORMAL = QtWidgets.QRadioButton(self.groupBox_computeFeatures)
        self.radioBtn_NORMAL.setGeometry(QtCore.QRect(20, 220, 112, 23))
        self.radioBtn_NORMAL.setObjectName("radioBtn_NORMAL")
        self.PresetGroup = QtWidgets.QButtonGroup(MainWindow)
        self.PresetGroup.setObjectName("PresetGroup")
        self.PresetGroup.addButton(self.radioBtn_NORMAL)
        self.radioBtn_HIGH = QtWidgets.QRadioButton(self.groupBox_computeFeatures)
        self.radioBtn_HIGH.setGeometry(QtCore.QRect(20, 240, 112, 23))
        self.radioBtn_HIGH.setObjectName("radioBtn_HIGH")
        self.PresetGroup.addButton(self.radioBtn_HIGH)
        self.radioBtn_ULTRA = QtWidgets.QRadioButton(self.groupBox_computeFeatures)
        self.radioBtn_ULTRA.setGeometry(QtCore.QRect(20, 260, 112, 23))
        self.radioBtn_ULTRA.setObjectName("radioBtn_ULTRA")
        self.PresetGroup.addButton(self.radioBtn_ULTRA)

        #Compute Matches options
        self.groupBox_computeMathes = QtWidgets.QGroupBox(self.v2_widget)
        self.groupBox_computeMathes.setGeometry(QtCore.QRect(590, 10, 181, 411))
        self.groupBox_computeMathes.setObjectName("groupBox_computeMathes")
        self.groupBox_computeMathes.setVisible(False)
        self.radioBtn_08 = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_08.setGeometry(QtCore.QRect(20, 50, 112, 23))
        self.radioBtn_08.setObjectName("radioBtn_08")
        self.RatioGroup = QtWidgets.QButtonGroup(MainWindow)
        self.RatioGroup.setObjectName("RatioGroup")
        self.RatioGroup.addButton(self.radioBtn_08)
        self.Ratio = QtWidgets.QLabel(self.groupBox_computeMathes)
        self.Ratio.setGeometry(QtCore.QRect(10, 30, 161, 17))
        self.Ratio.setObjectName("Ratio")
        self.radioBtn_06 = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_06.setGeometry(QtCore.QRect(20, 70, 131, 23))
        self.radioBtn_06.setObjectName("radioBtn_06")
        self.RatioGroup.addButton(self.radioBtn_06)
        self.GeometricModel = QtWidgets.QLabel(self.groupBox_computeMathes)
        self.GeometricModel.setGeometry(QtCore.QRect(10, 100, 161, 17))
        self.GeometricModel.setObjectName("GeometricModel")
        self.radioBtn_f = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_f.setGeometry(QtCore.QRect(20, 120, 112, 23))
        self.radioBtn_f.setObjectName("radioBtn_f")
        self.GeometricModelGroup = QtWidgets.QButtonGroup(MainWindow)
        self.GeometricModelGroup.setObjectName("GeometricModelGroup")
        self.GeometricModelGroup.addButton(self.radioBtn_f)
        self.radioBtn_e = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_e.setGeometry(QtCore.QRect(20, 140, 112, 23))
        self.radioBtn_e.setObjectName("radioBtn_e")
        self.GeometricModelGroup.addButton(self.radioBtn_e)
        self.NearestMatching = QtWidgets.QLabel(self.groupBox_computeMathes)
        self.NearestMatching.setGeometry(QtCore.QRect(10, 190, 161, 17))
        self.NearestMatching.setObjectName("NearestMatching")
        self.radioBtn_AUTO = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_AUTO.setGeometry(QtCore.QRect(20, 210, 112, 23))
        self.radioBtn_AUTO.setObjectName("radioBtn_AUTO")
        self.NearestMatchingGroup = QtWidgets.QButtonGroup(MainWindow)
        self.NearestMatchingGroup.setObjectName("NearestMatchingGroup")
        self.NearestMatchingGroup.addButton(self.radioBtn_AUTO)
        self.radioBtn_BRUTEFORCEL2 = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_BRUTEFORCEL2.setGeometry(QtCore.QRect(20, 230, 141, 23))
        self.radioBtn_BRUTEFORCEL2.setObjectName("radioBtn_BRUTEFORCEL2")
        self.NearestMatchingGroup.addButton(self.radioBtn_BRUTEFORCEL2)
        self.radioBtn_ANNL2 = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_ANNL2.setGeometry(QtCore.QRect(20, 250, 112, 23))
        self.radioBtn_ANNL2.setObjectName("radioBtn_ANNL2")
        self.NearestMatchingGroup.addButton(self.radioBtn_ANNL2)
        self.radioBtn_h = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_h.setGeometry(QtCore.QRect(20, 160, 112, 23))
        self.radioBtn_h.setObjectName("radioBtn_h")
        self.GeometricModelGroup.addButton(self.radioBtn_h)
        self.radioBtn_CASCADHEASHINGL2 = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_CASCADHEASHINGL2.setGeometry(QtCore.QRect(20, 270, 181, 41))
        self.radioBtn_CASCADHEASHINGL2.setObjectName("radioBtn_CASCADHEASHINGL2")
        self.NearestMatchingGroup.addButton(self.radioBtn_CASCADHEASHINGL2)
        self.radioBtn_FASTCASCADEHASHINGL2 = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_FASTCASCADEHASHINGL2.setGeometry(QtCore.QRect(20, 310, 181, 41))
        self.radioBtn_FASTCASCADEHASHINGL2.setObjectName("radioBtn_FASTCASCADEHASHINGL2")
        self.NearestMatchingGroup.addButton(self.radioBtn_FASTCASCADEHASHINGL2)
        self.radioBtn_BRUTEFORCEHAMMING = QtWidgets.QRadioButton(self.groupBox_computeMathes)
        self.radioBtn_BRUTEFORCEHAMMING.setGeometry(QtCore.QRect(20, 350, 141, 41))
        self.radioBtn_BRUTEFORCEHAMMING.setObjectName("radioBtn_BRUTEFORCEHAMMING")
        self.NearestMatchingGroup.addButton(self.radioBtn_BRUTEFORCEHAMMING)
        
        #Sequential Reconstruction Options
        self.groupBox_sequential = QtWidgets.QGroupBox(self.v2_widget)
        self.groupBox_sequential.setGeometry(QtCore.QRect(590, 10, 181, 411))
        self.groupBox_sequential.setObjectName("groupBox_sequential")
        self.groupBox_sequential.setVisible(False)
        self.radioBtn_ALL = QtWidgets.QRadioButton(self.groupBox_sequential)
        self.radioBtn_ALL.setGeometry(QtCore.QRect(20, 50, 111, 41))
        self.radioBtn_ALL.setObjectName("radioBtn_ALL")
        self.RefineIntrinsics = QtWidgets.QLabel(self.groupBox_sequential)
        self.RefineIntrinsics.setGeometry(QtCore.QRect(10, 30, 161, 17))
        self.RefineIntrinsics.setObjectName("RefineIntrinsics")
        self.radioBtn_NONE = QtWidgets.QRadioButton(self.groupBox_sequential)
        self.radioBtn_NONE.setGeometry(QtCore.QRect(20, 90, 131, 23))
        self.radioBtn_NONE.setObjectName("radioBtn_NONE")
        self.radioBtn_FOCAL_LENGTH = QtWidgets.QRadioButton(self.groupBox_sequential)
        self.radioBtn_FOCAL_LENGTH.setGeometry(QtCore.QRect(20, 110, 141, 51))
        self.radioBtn_FOCAL_LENGTH.setObjectName("radioBtn_FOCAL_LENGTH")
        self.radioBtn_PRINCIPAL_POINT = QtWidgets.QRadioButton(self.groupBox_sequential)
        self.radioBtn_PRINCIPAL_POINT.setGeometry(QtCore.QRect(20, 160, 112, 51))
        self.radioBtn_PRINCIPAL_POINT.setObjectName("radioBtn_PRINCIPAL_POINT")
        self.radioBtn_DISTORTION = QtWidgets.QRadioButton(self.groupBox_sequential)
        self.radioBtn_DISTORTION.setGeometry(QtCore.QRect(20, 220, 112, 41))
        self.radioBtn_DISTORTION.setObjectName("radioBtn_DISTORTION")
        self.RefineIntrinsicsGroup = QtWidgets.QButtonGroup(MainWindow)
        self.RefineIntrinsicsGroup.setObjectName("RefineIntrinsicsGroup")   
        self.RefineIntrinsicsGroup.addButton(self.radioBtn_ALL)
        self.RefineIntrinsicsGroup.addButton(self.radioBtn_NONE)
        self.RefineIntrinsicsGroup.addButton(self.radioBtn_DISTORTION)
        self.RefineIntrinsicsGroup.addButton(self.radioBtn_PRINCIPAL_POINT)
        self.RefineIntrinsicsGroup.addButton(self.radioBtn_FOCAL_LENGTH)


        #MVG to MVS
        self.groupBox_MvgToMvs = QtWidgets.QGroupBox(self.v2_widget)
        self.groupBox_MvgToMvs.setGeometry(QtCore.QRect(590, 10, 181, 411))
        self.groupBox_MvgToMvs.setObjectName("groupBox_MvgToMvs")
        self.groupBox_MvgToMvs.setVisible(False)
        self.lbl_non = QtWidgets.QLabel(self.groupBox_MvgToMvs)
        self.lbl_non.setGeometry(QtCore.QRect(10, 30, 161, 17))
        self.lbl_non.setObjectName("lbl_non")

        #Densify Point Cloud
        self.groupBox_densifyPointCloud = QtWidgets.QGroupBox(self.v2_widget)
        self.groupBox_densifyPointCloud.setGeometry(QtCore.QRect(590, 10, 181, 411))
        self.groupBox_densifyPointCloud.setObjectName("groupBox_densifyPointCloud")
        self.groupBox_densifyPointCloud.setVisible(False)
        self.ResolutionLevel = QtWidgets.QLabel(self.groupBox_densifyPointCloud)
        self.ResolutionLevel.setGeometry(QtCore.QRect(10, 30, 161, 41))
        self.ResolutionLevel.setObjectName("ResolutionLevel")
        self.radioBtn_RL_1 = QtWidgets.QRadioButton(self.groupBox_densifyPointCloud)
        self.radioBtn_RL_1.setGeometry(QtCore.QRect(20, 80, 112, 23))
        self.radioBtn_RL_1.setObjectName("radioBtn_RL_1")
        self.radioBtn_RL_2 = QtWidgets.QRadioButton(self.groupBox_densifyPointCloud)
        self.radioBtn_RL_2.setGeometry(QtCore.QRect(20, 100, 131, 23))
        self.radioBtn_RL_2.setObjectName("radioBtn_RL_2")
        self.radioBtn_RL_3 = QtWidgets.QRadioButton(self.groupBox_densifyPointCloud)
        self.radioBtn_RL_3.setGeometry(QtCore.QRect(20, 120, 131, 23))
        self.radioBtn_RL_3.setObjectName("radioBtn_RL_3")
        self.DensifyResolutionGroup = QtWidgets.QButtonGroup(MainWindow)
        self.DensifyResolutionGroup.setObjectName("DensifyResolutionGroup")   
        self.DensifyResolutionGroup.addButton(self.radioBtn_RL_1)
        self.DensifyResolutionGroup.addButton(self.radioBtn_RL_2)
        self.DensifyResolutionGroup.addButton(self.radioBtn_RL_3)

        #Reconstruct Mesh
        self.groupBox_reconstructMesh = QtWidgets.QGroupBox(self.v2_widget)
        self.groupBox_reconstructMesh.setGeometry(QtCore.QRect(590,10, 181, 411))
        self.groupBox_reconstructMesh.setObjectName("groupBox_reconstructMesh")
        self.groupBox_reconstructMesh.setVisible(False)
        self.radioBtn_minPoint_25f = QtWidgets.QRadioButton(self.groupBox_reconstructMesh)
        self.radioBtn_minPoint_25f.setGeometry(QtCore.QRect(20, 60, 112, 23))
        self.radioBtn_minPoint_25f.setObjectName("radioBtn_minPoint_25f")
        self.mimPointDistance = QtWidgets.QLabel(self.groupBox_reconstructMesh)
        self.mimPointDistance.setGeometry(QtCore.QRect(10, 30, 161, 21))
        self.mimPointDistance.setObjectName("mimPointDistance")
        self.radioBtn_minPoint_6 = QtWidgets.QRadioButton(self.groupBox_reconstructMesh)
        self.radioBtn_minPoint_6.setGeometry(QtCore.QRect(20, 80, 161, 23))
        self.radioBtn_minPoint_6.setObjectName("radioBtn_minPoint_6")
        self.MinPointGroup = QtWidgets.QButtonGroup(MainWindow)
        self.MinPointGroup.setObjectName("MinPointGroup")   
        self.MinPointGroup.addButton(self.radioBtn_minPoint_25f)
        self.MinPointGroup.addButton(self.radioBtn_minPoint_6)

        #Refine Mesh
        self.groupBox_refineMesh = QtWidgets.QGroupBox(self.v2_widget)
        self.groupBox_refineMesh.setGeometry(QtCore.QRect(590, 10, 181, 411))
        self.groupBox_refineMesh.setObjectName("groupBox_refineMesh")
        self.groupBox_refineMesh.setVisible(False)
        self.ResolutionLevel_2 = QtWidgets.QLabel(self.groupBox_refineMesh)
        self.ResolutionLevel_2.setGeometry(QtCore.QRect(10, 30, 161, 41))
        self.ResolutionLevel_2.setObjectName("ResolutionLevel_2")
        self.radioBtn_RL_4 = QtWidgets.QRadioButton(self.groupBox_refineMesh)
        self.radioBtn_RL_4.setGeometry(QtCore.QRect(20, 80, 112, 23))
        self.radioBtn_RL_4.setObjectName("radioBtn_RL_4")
        self.ResolutionGroup = QtWidgets.QButtonGroup(MainWindow)
        self.ResolutionGroup.setObjectName("ResolutionGroup")   
        self.ResolutionGroup.addButton(self.radioBtn_RL_4)
        self.radioBtn_RL_5 = QtWidgets.QRadioButton(self.groupBox_refineMesh)
        self.radioBtn_RL_5.setGeometry(QtCore.QRect(20, 100, 131, 23))
        self.radioBtn_RL_5.setObjectName("radioBtn_RL_5")
        self.ResolutionGroup.addButton(self.radioBtn_RL_5)
        self.radioBtn_RL_6 = QtWidgets.QRadioButton(self.groupBox_refineMesh)
        self.radioBtn_RL_6.setGeometry(QtCore.QRect(20, 120, 131, 23))
        self.radioBtn_RL_6.setObjectName("radioBtn_RL_6")
        self.ResolutionGroup.addButton(self.radioBtn_RL_6)
        self.MaxFaceArea = QtWidgets.QLabel(self.groupBox_refineMesh)
        self.MaxFaceArea.setGeometry(QtCore.QRect(10, 150, 161, 31))
        self.MaxFaceArea.setObjectName("MaxFaceArea")
        self.radioBtn_MaxFace_32 = QtWidgets.QRadioButton(self.groupBox_refineMesh)
        self.radioBtn_MaxFace_32.setGeometry(QtCore.QRect(20, 220, 131, 23))
        self.radioBtn_MaxFace_32.setObjectName("radioBtn_MaxFace_32")
        self.MaxFaceAreaGroup = QtWidgets.QButtonGroup(MainWindow)
        self.MaxFaceAreaGroup.setObjectName("MaxFaceAreaGroup")
        self.MaxFaceAreaGroup.addButton(self.radioBtn_MaxFace_32)
        self.radioBtn_MaxFace_64 = QtWidgets.QRadioButton(self.groupBox_refineMesh)
        self.radioBtn_MaxFace_64.setGeometry(QtCore.QRect(20, 180, 112, 23))
        self.radioBtn_MaxFace_64.setObjectName("radioBtn_MaxFace_64")
        self.MaxFaceAreaGroup.addButton(self.radioBtn_MaxFace_64)
        self.radioBtn_MaxFace_16 = QtWidgets.QRadioButton(self.groupBox_refineMesh)
        self.radioBtn_MaxFace_16.setGeometry(QtCore.QRect(20, 200, 112, 23))
        self.radioBtn_MaxFace_16.setObjectName("radioBtn_MaxFace_16")
        self.MaxFaceAreaGroup.addButton(self.radioBtn_MaxFace_16)
        self.MeshFile = QtWidgets.QLabel(self.groupBox_refineMesh)
        self.MeshFile.setGeometry(QtCore.QRect(10, 240, 161, 31))
        self.MeshFile.setObjectName("MeshFile")

        #Texture Mesh
        self.groupBox_textureMesh = QtWidgets.QGroupBox(self.v2_widget)
        self.groupBox_textureMesh.setGeometry(QtCore.QRect(590, 10, 181, 411))
        self.groupBox_textureMesh.setObjectName("groupBox_textureMesh")
        self.groupBox_textureMesh.setVisible(False)
        self.TextureMesh = QtWidgets.QLabel(self.groupBox_textureMesh)
        self.TextureMesh.setGeometry(QtCore.QRect(10, 30, 161, 41))
        self.TextureMesh.setObjectName("TextureMesh")
        self.radioBtn_RL_7 = QtWidgets.QRadioButton(self.groupBox_textureMesh)
        self.radioBtn_RL_7.setGeometry(QtCore.QRect(20, 80, 112, 23))
        self.radioBtn_RL_7.setObjectName("radioBtn_RL_7")
        self.radioBtn_RL_8 = QtWidgets.QRadioButton(self.groupBox_textureMesh)
        self.radioBtn_RL_8.setGeometry(QtCore.QRect(20, 100, 131, 23))
        self.radioBtn_RL_8.setObjectName("radioBtn_RL_8")
        self.radioBtn_RL_9 = QtWidgets.QRadioButton(self.groupBox_textureMesh)
        self.radioBtn_RL_9.setGeometry(QtCore.QRect(20, 120, 131, 23))
        self.radioBtn_RL_9.setObjectName("radioBtn_RL_9")
        self.TextureResolutionGroup = QtWidgets.QButtonGroup(MainWindow)
        self.TextureResolutionGroup.setObjectName("TextureResolutionGroup")   
        self.TextureResolutionGroup.addButton(self.radioBtn_RL_7)
        self.TextureResolutionGroup.addButton(self.radioBtn_RL_8)
        self.TextureResolutionGroup.addButton(self.radioBtn_RL_9)

    
        self.verticalLayout_2.addWidget(self.v2_widget)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 499, 781, 51))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        #self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticafile_listlLayoutWidget_3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.v3_widget = QtWidgets.QWidget(self.verticalLayoutWidget_3)
        self.v3_widget.setObjectName("v3_widget")
        self.btn_start = QtWidgets.QPushButton(self.v3_widget)
        self.btn_start.setGeometry(QtCore.QRect(648, 10, 121, 31))
        self.btn_start.setObjectName("btn_start")
        self.btn_previous = QtWidgets.QPushButton(self.v3_widget)
        self.btn_previous.setGeometry(QtCore.QRect(510, 10, 131, 31))
        self.btn_previous.setObjectName("btn_previous")
        self.verticalLayout_3.addWidget(self.v3_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #start 버튼 이벤트
        self.btn_start.clicked.connect(self.startPipline)
        #comboBox 이벤트
        self.comboBox.currentIndexChanged.connect(lambda: self.comboBoxFunc(MyWindow))
        #output path Dialog
        self.btn_outputPath.clicked.connect(lambda:self.outputDialogFunc(MyWindow))
        #radio button 이벤트
        self.DescriberMethodGroup.buttonClicked.connect(lambda: self.selectOptionFunc("features","-m"))
        self.UprightGroup.buttonClicked.connect(lambda: self.selectOptionFunc("features","-u"))
        self.PresetGroup.buttonClicked.connect(lambda: self.selectOptionFunc("features","-p"))

        self.RatioGroup.buttonClicked.connect(lambda: self.selectOptionFunc("matches","-r"))
        self.GeometricModelGroup.buttonClicked.connect(lambda: self.selectOptionFunc("matches","-g"))
        self.NearestMatchingGroup.buttonClicked.connect(lambda: self.selectOptionFunc("matches","-n"))
        self.RefineIntrinsicsGroup.buttonClicked.connect(lambda: self.selectOptionFunc("seq", "-f"))
        self.DensifyResolutionGroup.buttonClicked.connect(lambda: self.selectOptionFunc("densify", "--resolution-level"))
        self.MinPointGroup.buttonClicked.connect(lambda: self.selectOptionFunc("mesh", "-d"))
        self.ResolutionGroup.buttonClicked.connect(lambda: self.selectOptionFunc("refine", "--resolution-level"))
        self.MaxFaceAreaGroup.buttonClicked.connect(lambda: self.selectOptionFunc("refine", "--max-face-area"))
        self.TextureResolutionGroup.buttonClicked.connect(lambda: self.selectOptionFunc("texture", "--resolution-level"))

    def startPipline(self):
        print ("1. Intrinsics analysis")
        pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params] )
        pIntrisics.wait()

        #====================================================================
        # Features 옵션 설정
        param = list([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"), "-i", matches_dir+"/sfm_data.json", "-o", matches_dir])

        for op in option["features"]:
            param.append(op)
            param.append(option["features"][op])

        print ("2. Compute features")
        pFeatures = subprocess.Popen( param )
        pFeatures.wait()

        #====================================================================
        # 특징점 캡쳐
        pFeature_dir = os.path.join(output_dir, "FeatureImage")
        if not os.path.exists(pFeature_dir):
            os.mkdir(pFeature_dir)

        param = list([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_exportKeypoints"), "-i", matches_dir+"/sfm_data.json", "-d", matches_dir, "-o", pFeature_dir])

        pFeatures_Capture = subprocess.Popen( param )
        pFeatures_Capture.wait()

        #====================================================================
        # Matches 옵션 설정

        param = list([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"), "-i", matches_dir+"/sfm_data.json", "-o", matches_dir])

        for op in option["matches"]:
            param.append(op)
            param.append(option["matches"][op])

        print ("3. Compute matches")
        pMatches = subprocess.Popen( param )
        pMatches.wait()

        #====================================================================
        # 매칭점 캡쳐
        pMatches_dir = os.path.join(output_dir, "MatchImage")
        if not os.path.exists(pMatches_dir):
            os.mkdir(pMatches_dir)

        param = list([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_exportMatches"), "-i", matches_dir+"/sfm_data.json", "-d", matches_dir, "-m", matches_dir + "/matches.putative.bin", "-o", pMatches_dir])

        pMatches_Capture = subprocess.Popen( param )
        pMatches_Capture.wait()

        # Create the reconstruction if not present
        if not os.path.exists(reconstruction_dir):
            os.mkdir(reconstruction_dir)

        # Create the ChangeBlack if not present
        file_list = os.listdir(input_dir)
        if not os.path.exists(ChangeWhite_dir):
            os.mkdir(ChangeWhite_dir)
        
        for str in file_list:
            path = input_dir + "/" + str
            if "_mask" in str:
                color_dir = input_dir + "/" + str[:-9] + ".jpg"
                print(color_dir)
                mask = cv2.imread(path, 0)
                img = cv2.imread(color_dir)
                
                m_height, m_width = mask.shape
                i_height, i_width, _ = img.shape
                
                if m_height == i_height and m_width == i_width: 
                    # 마스크를 적용시킨 하얀색 배경 사진
                    #matrix = cv2.getRotationMatrix2D((i_width/2, i_height/2), 90, 1)

                    #dst = cv2.warpAffine(img, matrix, (i_width, i_height))
                    #i = i_width/2 - i_height/2
                    #M = np.float32([[1, 0, -i], [0, 1, i]])
                    #img_translation = cv2.warpAffine(dst, M, (i_height, i_width))
                    img_white = ~mask
                    img_white = cv2.cvtColor(img_white, cv2.COLOR_GRAY2BGR)
                
                    res = cv2.bitwise_and(img, img, mask = mask)
                    
                    weighted_img = cv2.add(res, img_white)
                    
                    mask_png = ChangeWhite_dir + "/" + str[:-9] + ".jpg"
                    
                    cv2.imwrite(mask_png, weighted_img)
        

        #====================================================================
        # Sequential 옵션 설정

        param = list([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"), "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir])

        for op in option["seq"]:
            param.append(op)
            param.append(option["seq"][op])


        print ("4. Do Sequential/Incremental reconstruction")
        pRecons = subprocess.Popen( param )
        pRecons.wait()

        #====================================================================
        # 나머지

        print ("5. Colorize Structure")
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
        pRecons.wait()

        # optional, compute final valid structure from the known camera poses
        print ("6. Structure from Known Poses (robust triangulation)")
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-f", os.path.join(matches_dir, "matches.f.bin"), "-o", os.path.join(reconstruction_dir,"robust.bin")] )
        pRecons.wait()

        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/robust.bin", "-o", os.path.join(reconstruction_dir,"robust_colorized.ply")] )
        pRecons.wait()

        if not os.path.exists(Scene_dir):
            os.mkdir(Scene_dir)
        
        pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2openMVS"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(Scene_dir,"scene.mvs")] )
        pRecons.wait()
        #====================================================================

    def selectOptionFunc(self, pipNum, signal):
        if pipNum == "features":
            if signal == "-m":
                option[pipNum][signal] = self.DescriberMethodGroup.checkedButton().text()
            elif signal == "-u":
                option[pipNum][signal] = self.UprightGroup.checkedButton().text()
            elif signal == "-p":
                option[pipNum][signal] = self.PresetGroup.checkedButton().text()
            print(option["features"])
        elif pipNum == "matches":
            if signal == "-r":
                option[pipNum][signal] = self.RatioGroup.checkedButton().text()
            elif signal == "-g":
                option[pipNum][signal] = self.GeometricModelGroup.checkedButton().text()
            elif signal == "-n":
                option[pipNum][signal] = self.NearestMatchingGroup.checkedButton().text()
            print(option["matches"])
        elif pipNum == "seq":
            if signal == "-f":
                option[pipNum][signal] = self.RefineIntrinsicsGroup.checkedButton().text()
            print(option["seq"])
        elif pipNum == "densify":
            if signal == "--resolution-level":
                option[pipNum][signal] = self.DensifyResolutionGroup.checkedButton().text()
            print(option["densify"])
        elif pipNum == "mesh":
            if signal == "-d":
                option[pipNum][signal] = self.MinPointGroup.checkedButton().text()
            print(option["mesh"])
        elif pipNum == "refine":
            if signal == "--resolution-level":
                option[pipNum][signal] = self.ResolutionGroup.checkedButton().text()
            elif signal == "--max-face-area":
                option[pipNum][signal] = self.MaxFaceAreaGroup.checkedButton().text()
            print(option["refine"])
        elif pipNum == "texture":
            if signal == "--resolution-level":
                option[pipNum][signal] = self.TextureResolutionGroup.checkedButton().text()
            print(option["texture"])

            
    def outputDialogFunc(self, MyWindow):
        global output_dir, ChangeWhite_dir, matches_dir, reconstruction_dir, Scene_dir
        #QFileDialog.getOpenFileName()
        output_dir = str(QFileDialog.getExistingDirectory(self.centralwidget))
        ChangeWhite_dir = os.path.join(output_dir, "ChangeWhite")
        matches_dir = os.path.join(output_dir, "matches")
        reconstruction_dir = os.path.join(output_dir, "reconstruction_sequential")
        Scene_dir = os.path.join(output_dir,"Scene")

        print("!!"+output_dir)
        # Create the ouput/matches folder if not present
        if not os.path.exists(matches_dir):
            os.mkdir(matches_dir)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_outputPath.setText(_translate("MainWindow", "Output Path"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Compute Features"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Compute Matches"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Reconstruction (Sequential)"))
        self.comboBox.setItemText(3, _translate("MainWindow", "========================"))
        self.comboBox.setItemText(4, _translate("MainWindow", "OpenMVG to OpenMVS"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Densify Point Cloud"))
        self.comboBox.setItemText(6, _translate("MainWindow", "Reconstruct Mesh"))
        self.comboBox.setItemText(7, _translate("MainWindow", "Refine Mesh"))
        self.comboBox.setItemText(8, _translate("MainWindow", "Texture Mesh"))
        self.groupBox_computeFeatures.setTitle(_translate("MainWindow", "Options"))
        self.radioBtn_SIFT.setText(_translate("MainWindow", "SIFT"))
        self.DescriberMethod.setText(_translate("MainWindow", "Describer Method ( -m )"))
        self.radioBtn_AKAZE_FLOAT.setText(_translate("MainWindow", "AKAZE_FLOAT"))
        self.radioBtn_AKAZE_MLDE.setText(_translate("MainWindow", "AKAZE_MLDB"))
        self.Upright.setText(_translate("MainWindow", "Upright ( -u )"))
        self.radioBtn_0.setText(_translate("MainWindow", "0"))
        self.radioBtn_1.setText(_translate("MainWindow", "1"))
        self.Preset.setText(_translate("MainWindow", "Preset ( -p )"))
        self.radioBtn_NORMAL.setText(_translate("MainWindow", "NORMAL"))
        self.radioBtn_HIGH.setText(_translate("MainWindow", "HIGH"))
        self.radioBtn_ULTRA.setText(_translate("MainWindow", "ULTRA"))
        self.groupBox_computeMathes.setTitle(_translate("MainWindow", "Options"))
        self.radioBtn_08.setText(_translate("MainWindow", "0.8"))
        self.Ratio.setText(_translate("MainWindow", "Ratio ( -r )"))
        self.radioBtn_06.setText(_translate("MainWindow", "0.6"))
        self.GeometricModel.setText(_translate("MainWindow", "Geometric Model ( -g )"))
        self.radioBtn_f.setText(_translate("MainWindow", "Fundamental"))
        self.radioBtn_e.setText(_translate("MainWindow", "Essential"))
        self.NearestMatching.setText(_translate("MainWindow", "Nearest Matching ( -n )"))
        self.radioBtn_AUTO.setText(_translate("MainWindow", "AUTO"))
        self.radioBtn_BRUTEFORCEL2.setText(_translate("MainWindow", "BRUTEFORCEL2"))
        self.radioBtn_ANNL2.setText(_translate("MainWindow", "ANNL2"))
        self.radioBtn_h.setText(_translate("MainWindow", "Homography"))
        self.radioBtn_CASCADHEASHINGL2.setText(_translate("MainWindow", "CASCAD\n"
"HEASHINGL2"))
        self.radioBtn_FASTCASCADEHASHINGL2.setText(_translate("MainWindow", "FASTCASCADE\n"
"HASHINGL2"))
        self.radioBtn_BRUTEFORCEHAMMING.setText(_translate("MainWindow", "BRUTEFORCE\n"
"HAMMING"))
        self.groupBox_sequential.setTitle(_translate("MainWindow", "Options"))
        self.radioBtn_ALL.setText(_translate("MainWindow", "ADJUST_ALL"))
        self.RefineIntrinsics.setText(_translate("MainWindow", "Refine Instrinsics ( -f )"))
        self.radioBtn_NONE.setText(_translate("MainWindow", "NONE"))
        self.radioBtn_FOCAL_LENGTH.setText(_translate("MainWindow", "ADJUST_\n"
"FOCAL_LENGTH"))
        self.radioBtn_PRINCIPAL_POINT.setText(_translate("MainWindow", "ADJUST_\n"
"PRINCIPAL_\n"
"POINT"))
        self.radioBtn_DISTORTION.setText(_translate("MainWindow", "ADJUST_\n"
"DISTORTION"))

        self.groupBox_MvgToMvs.setTitle(_translate("MainWindow", "Options"))
        self.lbl_non.setText(_translate("MainWindow", "NONE"))
        self.groupBox_densifyPointCloud.setTitle(_translate("MainWindow", "Options"))
        self.ResolutionLevel.setText(_translate("MainWindow", "Resolution-Level\n"
"(Image Scale Down)"))
        self.radioBtn_RL_1.setText(_translate("MainWindow", "1"))
        self.radioBtn_RL_2.setText(_translate("MainWindow", "2"))
        self.radioBtn_RL_3.setText(_translate("MainWindow", "3"))
        self.groupBox_reconstructMesh.setTitle(_translate("MainWindow", "Options"))
        self.radioBtn_minPoint_25f.setText(_translate("MainWindow", "2.5f"))
        self.mimPointDistance.setText(_translate("MainWindow", "Min-Point-Distance"))
        self.radioBtn_minPoint_6.setText(_translate("MainWindow", "6"))
        self.groupBox_refineMesh.setTitle(_translate("MainWindow", "Options"))
        self.ResolutionLevel_2.setText(_translate("MainWindow", "Resolution-Level\n"
"(Image Scale Down)"))
        self.radioBtn_RL_4.setText(_translate("MainWindow", "1"))
        self.radioBtn_RL_5.setText(_translate("MainWindow", "2"))
        self.radioBtn_RL_6.setText(_translate("MainWindow", "3"))
        self.MaxFaceArea.setText(_translate("MainWindow", "Max-Face-Area"))
        self.radioBtn_MaxFace_32.setText(_translate("MainWindow", "32"))
        self.radioBtn_MaxFace_64.setText(_translate("MainWindow", "64"))
        self.radioBtn_MaxFace_16.setText(_translate("MainWindow", "16"))
        self.MeshFile.setText(_translate("MainWindow", "Mesh File"))
        self.groupBox_textureMesh.setTitle(_translate("MainWindow", "Options"))
        self.TextureMesh.setText(_translate("MainWindow", "Resolution-Level\n"
"(Image Scale Down)"))
        self.radioBtn_RL_7.setText(_translate("MainWindow", "1"))
        self.radioBtn_RL_8.setText(_translate("MainWindow", "2"))
        self.radioBtn_RL_9.setText(_translate("MainWindow", "3"))
        self.btn_start.setText(_translate("MainWindow", "Start"))
        self.btn_previous.setText(_translate("MainWindow", "Previous"))

    def comboBoxFunc(self, MyWindow):
        #Compute Features
        if self.comboBox.currentIndex() == 0:
            #옵션 창 변경
            self.groupBox_computeFeatures.setVisible(True)
            self.groupBox_computeMathes.setVisible(False)
            self.groupBox_sequential.setVisible(False)
            self.groupBox_MvgToMvs.setVisible(False)
            self.groupBox_densifyPointCloud.setVisible(False)
            self.groupBox_reconstructMesh.setVisible(False)
            self.groupBox_refineMesh.setVisible(False)
            self.groupBox_textureMesh.setVisible(False)
        #Compute Matches
        elif self.comboBox.currentIndex() == 1:
            self.groupBox_computeFeatures.setVisible(False)
            self.groupBox_computeMathes.setVisible(True)
            self.groupBox_sequential.setVisible(False)
            self.groupBox_MvgToMvs.setVisible(False)
            self.groupBox_densifyPointCloud.setVisible(False)
            self.groupBox_reconstructMesh.setVisible(False)
            self.groupBox_refineMesh.setVisible(False)
            self.groupBox_textureMesh.setVisible(False)
        #Sequential Reconstruction
        elif self.comboBox.currentIndex() == 2:
            self.groupBox_computeFeatures.setVisible(False)
            self.groupBox_computeMathes.setVisible(False)
            self.groupBox_sequential.setVisible(True)
            self.groupBox_MvgToMvs.setVisible(False)
            self.groupBox_densifyPointCloud.setVisible(False)
            self.groupBox_reconstructMesh.setVisible(False)
            self.groupBox_refineMesh.setVisible(False)
            self.groupBox_textureMesh.setVisible(False)
        #MVG to MVS
        elif self.comboBox.currentIndex() == 4:
            self.groupBox_computeFeatures.setVisible(False)
            self.groupBox_computeMathes.setVisible(False)
            self.groupBox_sequential.setVisible(False)
            self.groupBox_MvgToMvs.setVisible(True)
            self.groupBox_densifyPointCloud.setVisible(False)
            self.groupBox_reconstructMesh.setVisible(False)
            self.groupBox_refineMesh.setVisible(False)
            self.groupBox_textureMesh.setVisible(False)
        #Densify Point Cloud
        elif self.comboBox.currentIndex() == 5:
            self.groupBox_computeFeatures.setVisible(False)
            self.groupBox_computeMathes.setVisible(False)
            self.groupBox_sequential.setVisible(False)
            self.groupBox_MvgToMvs.setVisible(False)
            self.groupBox_densifyPointCloud.setVisible(True)
            self.groupBox_reconstructMesh.setVisible(False)
            self.groupBox_refineMesh.setVisible(False)
            self.groupBox_textureMesh.setVisible(False)
        #Reconstruct Mesh
        elif self.comboBox.currentIndex() == 6:
            self.groupBox_computeFeatures.setVisible(False)
            self.groupBox_computeMathes.setVisible(False)
            self.groupBox_sequential.setVisible(False)
            self.groupBox_MvgToMvs.setVisible(False)
            self.groupBox_densifyPointCloud.setVisible(False)
            self.groupBox_reconstructMesh.setVisible(True)
            self.groupBox_refineMesh.setVisible(False)
            self.groupBox_textureMesh.setVisible(False)
        #Refine Mesh
        elif self.comboBox.currentIndex() == 7:
            self.groupBox_computeFeatures.setVisible(False)
            self.groupBox_computeMathes.setVisible(False)
            self.groupBox_sequential.setVisible(False)
            self.groupBox_MvgToMvs.setVisible(False)
            self.groupBox_densifyPointCloud.setVisible(False)
            self.groupBox_reconstructMesh.setVisible(False)
            self.groupBox_refineMesh.setVisible(True)
            self.groupBox_textureMesh.setVisible(False)
        #Texture Mesh
        elif self.comboBox.currentIndex() == 8:
            self.groupBox_computeFeatures.setVisible(False)
            self.groupBox_computeMathes.setVisible(False)
            self.groupBox_sequential.setVisible(False)
            self.groupBox_MvgToMvs.setVisible(False)
            self.groupBox_densifyPointCloud.setVisible(False)
            self.groupBox_reconstructMesh.setVisible(False)
            self.groupBox_refineMesh.setVisible(False)
            self.groupBox_textureMesh.setVisible(True)
        
        self.groupBox_computeFeatures.update()
        self.groupBox_computeMathes.update()
        self.groupBox_sequential.update()
        self.groupBox_MvgToMvs.update()
        self.groupBox_densifyPointCloud.update()
        self.groupBox_reconstructMesh.update()
        self.groupBox_refineMesh.update()
        self.groupBox_textureMesh.update()
        #self.show()

        #self.setupUi(MyWindow)
        #MyWindow.show()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #data = plyfile.PlyData.read('scene_dense.ply')['vertex']
        #xyz = np.c_[data['x'], data['y'], data['z']]
        #rgb = np.c_[data['red'], data['green'], data['blue']]
        #self.v = pptk.viewer(xyz)
        #self.v.set(point_size=0.0005)
        #self.v.attributes(rgb / 255.)

        self.ui = Ui_MainWindow()
        self.startSetupUI()

    def startSetupUI(self):
        self.ui.setupUi(self)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    MainWindow = MyWindow()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())
