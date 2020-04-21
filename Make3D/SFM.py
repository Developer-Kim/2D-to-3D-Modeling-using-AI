#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# This file is part of OpenMVG (Open Multiple View Geometry) C++ library.

# Python implementation of the bash script written by Romuald Perrot
# Created by @vins31
# Modified by Pierre Moulon
#
# this script is for easy use of OpenMVG
#
# usage : python openmvg.py image_dir output_dir
#
# image_dir is the input directory where images are located
# output_dir is where the project must be saved
#
# if output_dir is not present script will create it
#

# Indicate the openMVG binary directory
#OPENMVG_SFM_BIN = "/home/jeong/Install/openMVG_Build/Linux-x86_64-RELEASE"

# Indicate the openMVG camera sensor width directory
#CAMERA_SENSOR_WIDTH_DIRECTORY = "/home/jeong/Install/openMVG/src/software/SfM" + "/../../openMVG/exif/sensor_width_database"

import os
import subprocess
import sys
import cv2
import numpy as np

if len(sys.argv) < 2:
    print ("Usage %s image_dir output_dir" % sys.argv[0])
    sys.exit(1)

program_dir = os.getcwd()
input_dir = os.path.join(program_dir, "Image")
output_dir = sys.argv[1]

OPENMVG_SFM_BIN = os.path.join(program_dir, "Binary")
CAMERA_SENSOR_WIDTH_DIRECTORY = os.path.join(program_dir, "Camera")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")

ChangeWhite_dir = os.path.join(output_dir, "ChangeWhite")
matches_dir = os.path.join(output_dir, "matches")
reconstruction_dir = os.path.join(output_dir, "reconstruction_sequential")
Scene_dir = os.path.join(output_dir,"Scene")

print ("Program dir : ", program_dir)
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)

# Create the ouput/matches folder if not present
if not os.path.exists(output_dir):
  os.mkdir(output_dir)
if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)

print ("1. Intrinsics analysis")
pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params] )
pIntrisics.wait()

print ("2. Compute features")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-m", "SIFT"] )
pFeatures.wait()

print ("3. Compute matches")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir] )
pMatches.wait()

# Create the reconstruction if not present
if not os.path.exists(reconstruction_dir):
    os.mkdir(reconstruction_dir)
   

# Create the ChangeBlack if not present
file_list = os.listdir(input_dir)
if not os.path.exists(ChangeWhite_dir):
    os.mkdir(ChangeWhite_dir)
    
for str in file_list:
    path = input_dir + str
    if "_mask" in str:
        color_dir = input_dir + str[:-9] + ".jpg"
        
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
   

print ("4. Do Sequential/Incremental reconstruction")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
pRecons.wait()

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


pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "DensifyPointCloud"), "--resolution-level", "2",  reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(Scene_dir,"scene.mvs")] )
pRecons.wait()


#  [   "Densify point cloud",
#                 os.path.join(OPENMVS_BIN,"DensifyPointCloud"),
#                 ["--resolution-level", "2", "scene.mvs", "-w","%mvs_dir%"]],
#             [   "Reconstruct the mesh",
#                 os.path.join(OPENMVS_BIN,"ReconstructMesh"),
#                 ["-d", "6", "scene_dense.mvs", "-w","%mvs_dir%"]],
#             [   "Refine the mesh",
#                 os.path.join(OPENMVS_BIN,"RefineMesh"),
#                 ["--resolution-level", "2", "--max-face-area", "16", "scene_dense_mesh.mvs", "-w","%mvs_dir%"]],
#             [   "Texture the mesh",
#                 os.path.join(OPENMVS_BIN,"TextureMesh"),
#                 ["--resolution-level", "2", "scene_dense_mesh_refine.mvs", "-w","%mvs_dir%"]]
#             ]
