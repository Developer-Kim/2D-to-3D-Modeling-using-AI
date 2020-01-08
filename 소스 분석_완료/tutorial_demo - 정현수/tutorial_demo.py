#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# This file is part of OpenMVG (Open Multiple View Geometry) C++ library.

# Python script to launch OpenMVG SfM tools on an image dataset
#
# usage : python tutorial_demo.py
#

# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/home/hyeonsu/Code/Library/openMVG/build/Linux-x86_64-RELEASE"

# /home/hyeonsu/Code/Library/openMVG/build/openMVG/exif/sensor_width_database/ 가 실질적인 경로.
# Indicate the openMVG camera sensor width directory
CAMERA_SENSOR_WIDTH_DIRECTORY = "/home/hyeonsu/Code/Library/openMVG/src/software/SfM" + "/../../openMVG/exif/sensor_width_database"

import os
import subprocess
import sys

def get_parent_dir(directory):
    return os.path.dirname(directory) # 입력받은 파일/디렉터리의 경로를 반환합니다. 한 단계 이전으로. 

# 경로를 파일이 있는 곳으로 지정
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# os.chdir를 통해 지정된 곳을 바탕으로
# /home/hyeonsu/Code/Library/openMVG/build/software/SfM/ImageDataset_SceauxCastle
input_eval_dir = os.path.abspath("./ImageDataset_SceauxCastle")

# Checkout an OpenMVG image dataset with Git
# OpenMVG 이미지 데이터셋인 input_eval_dir이 존재하지 않으면, 깃을 통해서 다운로드 받아옴.
if not os.path.exists(input_eval_dir):
  pImageDataCheckout = subprocess.Popen([ "git", "clone", "https://github.com/openMVG/ImageDataset_SceauxCastle.git" ])
  pImageDataCheckout.wait()

# os.path.join: 해당 OS 형식에 맞도록 입력 받은 경로를 연결합니다.
# 위에 get_parent_dir(input_eval_dir)을 통해 입력받은 경로의 한단계 이전경로를 반환해주고 tutorial_out과 합침.
# /home/hyeonsu/Code/Library/openMVG/build/software/SfM/tutorial_out
output_eval_dir = os.path.join(get_parent_dir(input_eval_dir), "tutorial_out")

# /home/hyeonsu/Code/Library/openMVG/build/software/SfM/ImageDataset_SceauxCastle/images
input_eval_dir = os.path.join(input_eval_dir, "images")

# output_eval_dir: 결과값
# input_eval_dir: 입력값

if not os.path.exists(output_eval_dir):
  os.mkdir(output_eval_dir)

input_dir = input_eval_dir
output_dir = output_eval_dir
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)

# /home/hyeonsu/Code/Library/openMVG/build/software/SfM/tutorial_out/matches/
matches_dir = os.path.join(output_dir, "matches")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")

# Create the ouput/matches folder if not present
if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)


# /home/hyeonsu/Code/Library/openMVG/build/Linux-x86_64-RELEASE/
# 이 경로에 바이너리 파일이 들어있어서 이것들을 이용하면 됌.


########################################################################
#                   1. 카메라 내부 파라미터 분석
########################################################################

# openMVG_main_SfMInit_ImageListing -i [] -d [] -o []
# 
#        [-i|–imageDirectory]  - 넣을 이미지 디렉터리
#        [-d|–sensorWidthDatabase] openMVG/src/openMVG/exif/sensor_width_database/sensor_width_camera_database.txt      - 카메라 센서 width 데이터베이스 경로
#        [-o|–outputDirectory]  - 출력할 디렉터리(matches)
#

# Optional parameters:
#
#        [-f|–focal] (value in pixels)                         - 거리
#        [-k|–intrinsics] Kmatrix: “f;0;ppx;0;f;ppy;0;0;1”     - K 매트릭스
#        [-c|–camera_model] Camera model type:                 - 카메라 모델 타입
#            1: Pinhole
#            2: Pinhole radial 1
#            3: Pinhole radial 3 (default)
#        [-g|–group_camera_model]                              - 그룹 카메라 모델
#            0-> each view have it’s own camera intrinsic parameters
#            1-> (default) view can share some camera intrinsic parameters

# Example
# $ openMVG_main_SfMInit_ImageListing -d /home/user/Dev/openMVG/src/openMVG/exif/sensor_width_database/sensor_width_camera_database.txt -i /home/user/Dataset/ImageDataset_SceauxCastle/images -o /home/user/Dataset/ImageDataset_SceauxCastle/matches
#
# If you have installed OpenMVG on your machine your could do:
# $ openMVG_main_SfMInit_ImageListing -d /usr/share/openMVG/sensor_width_camera_database.txt -i /home/user/Dataset/ImageDataset_SceauxCastle/images -o /home/user/Dataset/ImageDataset_SceauxCastle/matches
#
print ("1. Intrinsics analysis")
pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params, "-c", "3"] )
pIntrisics.wait()


########################################################################
#                   2-1. 특징 검출
########################################################################

# $ openMVG_main_ComputeFeatures -i [..\matches\sfm_data.json] -o [...\matches]
#
#        [-i|–input_file]
#            a SfM_Data file  - 카메라 내부 파라미터 분석할 때 나온 matches 폴더의 sfm_data.json(초점이 미리 적혀진 txt 파일)
#        [-o|–outdir path]
#            path were image description will be stored  -  이미지 디스크립션을 저장할 위치 지정

# Optional parameters:
#
#        [-f|–force: 데이터를 강제로 다시 계산]
#            0: (default) 이전에 계산한 데이터 다시 로드(프로세스 삭제 및 계속 계산하려는 경우 유용)
#            1: 명령줄 매개 변수를 변경한 경우 유용하며, 강제로 다시 계산하고 다시 저장할 수 있다.

#        [-m|–describerMethod]
#            이미지의 디스크립터를 뽑는데 사용됨:
#                SIFT: (default),
#                AKAZE_FLOAT: AKAZE with floating point descriptors,
#                AKAZE_MLDB: AKAZE with binary descriptors.

#        [-u|–upright]
#            Upright 기능 사용 여부
#                0: (default, rotation invariance)
#                1: extract upright feature (orientation angle = 0°)

#        [-p|–describerPreset]
#            Image_describer 구성을 제어하는 데 사용:    (+) 이것에 따라 디스크립터 수가 결정되는 듯함. 높을수록 시간이 많이 걸림
#                NORMAL,
#                HIGH,
#                ULTRA: !!Can be time consuming!!


# /sfm_data.json : txt 파일을 설명자 이미지 매개 변수에 연결. ( 초점이 미리 적혀진 txt 파일 )
# 특징 검출
print ("2. Compute features")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-m", "SIFT", "-f" , "1"] )
pFeatures.wait()


########################################################################
#                   2-2. 특징 매칭
########################################################################

# $ openMVG_main_ComputeMatches -i [..\matches\sfm_data.json] -o [...\matches]

#        [-i|–input_file]
#            a SfM_Data file  -  카메라 내부 파라미터 분석할 때 나온 matches 폴더의 sfm_data.json(초점이 미리 적혀진 txt 파일)
#        [-o|–out_dir path]
#            path were putative and geometric matches will be stored   - 추정 및 기하학적 매칭정보를 저장할 위치

# Optional parameters:
#
        # [-f|–force: 데이터를 강제로 다시 계산]
        #     0: (default) 이전에 계산한 데이터 다시 로드(프로세스 삭제 및 계속 계산하려는 경우 유용)
        #    1: 명령줄 매개 변수를 변경한 경우 유용하며, 강제로 다시 계산하고 다시 저장할 수 있다.

        # [-r|-ratio]
        #     (가장 가까운 이웃 거리 비율, 기본값은 0.8로 설정).
        #         0.6을 사용하는 것이 더 제한적입니다. => 오탐지를 줄입니다.

        # [-g|-geometric_model]
        #    광도 추정 일치에서 강력한 추정에 사용되는 모델 유형
        #         f: Fundamental matrix filtering
        #         e: Essential matrix filtering
        #         h: Homography matrix filtering

        # [-n|–nearest_matching_method]
        #     AUTO: 지역 유형에서 자동 선택,
        #     스칼라 기반 디스크립터의 경우 다음을 사용할 수 있습니다.
        #         BRUTEFORCEL2: 스칼라 기반 영역 설명자와 일치하는 BruteForce L2
        #         ANNL2: 스칼라 기반 영역 설명자에 대한 가장 가까운 이웃 L2 일치
        #         CASCADEHASHINGL2: L2 캐스케이드 해싱 매칭,
        #         FASTCASCADEHASHINGL2: (default).
        #             미리 계산된 해시 영역이 있는 L2 캐스케이드 해싱 (CASCADEHASHINGL2보다 빠르지만 더 많은 메모리 사용)
        #     이진기반 디스크립터일 때 사용해야 함:
        #         BRUTEFORCEHAMMING: 이진 기반 영역 설명자를위한 BruteForce Hamming 일치

        # [-v|–video_mode_matching]
        #     (X 이미지의 겹침과 일치하는 시퀀스)
        #         X: with match 0 with (1->X), ...]
        #         2: will match 0 with (1,2), 1 with (2,3), ...
        #         3: will match 0 with (1,2,3), 1 with (2,3,4), ...]
        
        # [-l|–pair_list]
        #     명시적으로 비교해야하는 뷰 쌍을 나열하는 파일

# 매칭
print ("2. Compute matches")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-f", "1", "-n", "ANNL2"] )
pMatches.wait()


########################################################################
#                   3. Reconstruction
########################################################################

# $ openMVG_main_IncrementalSfM -i Dataset/matches/sfm_data.json -m Dataset/matches/ -o Dataset/out_Incremental_Reconstruction/
        # [-i|–input_file]
        #     a SfM_Data file  -  카메라 내부 파라미터 분석할 때 나온 matches 폴더의 sfm_data.json(초점이 미리 적혀진 txt 파일)
        # [-m|–matchdir]
        #     path were geometric matches were stored   -  matches의 폴더
        # [-o|–outdir]
        #     path where the output data will be stored  - output 데이터가 저장될 위치


# Optional parameters:

#         [-a|–initialPairA NAME]
#             the filename image to use (i.e. 100_7001.JPG)

#         [-b|–initialPairB NAME]
#             the filename image to use (i.e. 100_7002.JPG)

#         [-c|–camera_model]
#             알 수없는 내장 뷰에 사용될 카메라 모델 유형:
#                 1: Pinhole
#                 2: Pinhole radial 1
#                 3: Pinhole radial 3 (default)
#                 4: Pinhole radial 3 + tangential 2
#                 5: Pinhole fisheye

#         [-f|–refineIntrinsics]

#             사용자는 상수 / 변수로 간주 될 매개 변수를 정확하게 제어하고 '|'연산자를 사용하여 결합 할 수 있습니다.

#             ADJUST_ALL -> 기존 매개 변수를 모두 수정(default)
#             NONE -> 내장 파라미터는 일정하게 유지됩니다
#             ADJUST_FOCAL_LENGTH -> 초점 거리만 수정
#             ADJUST_PRINCIPAL_POINT -> 주요 지점만 수정
#             ADJUST_DISTORTION -> 왜곡 계수만 수정 (있는 경우)
#             ‘|’ 옵션을 결합할 수 있음:
#                 ADJUST_FOCAL_LENGTH|ADJUST_PRINCIPAL_POINT -> 초점 거리와 기본 위치를 정합니다
#                 ADJUST_FOCAL_LENGTH|ADJUST_DISTORTION -> 초점 거리와 왜곡 계수를 수정합니다 (있는 경우).
#                 ADJUST_PRINCIPAL_POINT|ADJUST_DISTORTION -> 주요 점 위치 및 왜곡 계수를 수정합니다 (있는 경우).


# Reconstruction
# 결과물을 reconstruction_sequential에 담음.
reconstruction_dir = os.path.join(output_dir,"reconstruction_sequential")
print ("3. Do Incremental/Sequential reconstruction") #set manually the initial pair to avoid the prompt question
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
pRecons.wait()


########################################################################
#                   5. Reconstruction
########################################################################

# a. 색상이 없는 트랙 ID를 나열
# b. 가장 많이 본 뷰 ID 목록
# c. 뷰를 보는 트랙에 색을 칠함
# d. 채색되지 않은 트랙이 남을 때까지 a.로 이동

# 정보 및 사용법
# 응용 프로그램은 sfm_data.json 파일에서 실행되도록 설계되었습니다.
# sfm_data 파일에는 다음이 포함되어야합니다.
# 정의된 내장 함수 및 카메라 포즈가 있는 유효한 뷰(선택적인 기존 구조)

# $ openMVG_main_ComputeSfM_DataColor -i Dataset/out_Reconstruction/sfm_data.json -o Dataset/out_Reconstruction/sfm_data_color.ply

        # [-i|–input_file]
        #     a SfM_Data file  -  reconstruciotn_sequential 결과물이 나온 곳에 존재하는 sfm_data.bin( 정의된 내장 함수 및 카메라 포즈가 있는 유효한 뷰(선택적인 기존 구조) )
        # [-o|–output_file]
        #     output scene with updated landmarks color  - 업데이트 된 랜드 마크 색상으로 출력 장면인 파일


# 색깔 
print ("5. Colorize Structure")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons.wait()

########################################################################
#                   4. 삼각 측량
########################################################################

# 이 응용 프로그램은 해당 형상을 계산하고 알려진 카메라의 본질과 자세의 기하학적 구조에 따라 강력하게 삼각측량한다.

# 정보 및 사용법
# 응용 프로그램은 sfm_data.json 파일에서 실행되도록 설계되었습니다.
# sfm_data 파일에는 다음이 포함되어야합니다.
# 정의된 내장 함수 및 카메라 포즈가 있는 유효한 뷰(선택적인 기존 구조)

        # [-i|–input_file]
        #     유효한 내장 함수와 포즈 및 선택적 구조를 가진 SfM_Data 파일 -  reconstruciotn_sequential 결과물이 나온 곳에 존재하는 sfm_data.bin
        # [-m|–matchdir]
        #     path were image descriptions were stored   -   이미지의 디스크립션이 저장된 경로
        # [-o|–outdir]
        #     path where the updated scene data will be stored   -  업데이트 된 장면 데이터가 저장 될 경로


# Optional parameters:

#         [-f|–match_file]
#             매치 파일의 경로(매치 파일 쌍이 나열되어 사용됨)
#         [-p|–pair_file]
#             페어 파일에 대한 경로(이 페어만 구조를 계산하는 것으로 간주됨) 페어 파일은 뷰 인덱스의 목록이며, 각 라인에 하나의 페어임
#         [-b|–bundle_adjustment]
#             장면에서 번들 조정을 수행(기본적으로 OFF)
#         [-r|–residual_threshold]
#             삼각 분할에 대해 고려되는 최대 픽셀 재 투사 오류 (기본적으로 4.0)


# Triangulation
print ("4. Structure from Known Poses (robust triangulation)")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons.wait()






########################################################################
#                   2-2. 글로벌 특징 매칭
########################################################################

# Reconstruction for the global SfM pipeline
# - global SfM pipeline use matches filtered by the essential matrices
# - here we reuse photometric matches and perform only the essential matrix filering
print ("2. Compute matches (for the global SfM Pipeline)")
# pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-f", "1", "-n", "ANNL2"] )
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", matches_dir+"/sfm_data.json", "-o", matches_dir, "-r", "0.8", "-g", "e"] )
pMatches.wait()

########################################################################
#                   3. 글로벌 reconstruction
########################################################################


# $ openMVG_main_GlobalSfM -i Dataset/matches/sfm_data.json -m Dataset/matches/ -o Dataset/out_Global_Reconstruction/

        # [-i|–input_file]
        #     a SfM_Data file   -   카메라 내부 파라미터 분석할 때 나온 matches 폴더의 sfm_data.json(초점이 미리 적혀진 txt 파일)
        # [-m|–matchdir]
        #     path were geometric matches were stored  -   matches의 폴더
        # [-o|–outdir]
        #     path where the output data will be stored   -  reconstruction 한 뒤 저장할 데이터 경로

# Optional parameters:

#         [-r|–rotationAveraging]
#             1: L1 회전 평균화 _ [Chatterjee]
#             2: (default) L2 회전 평균화 _ [Martinec]

#         [-t|–translationAveraging]
#             1: (default) L1 translation 평균 _[GlobalACSfM]
#             2: L2 translation 평균_[Kyle2014]
#             3: (default) SoftL1 최소화 _[GlobalACSfM]

#         [-f|–refineIntrinsics]

#             사용자는 상수 / 변수로 간주 될 매개 변수를 정확하게 제어하고 '|'연산자를 사용하여 결합 할 수 있습니다.

#             ADJUST_ALL -> 기존 매개 변수를 모두 수정(default)
#             NONE -> 내장 파라미터는 일정하게 유지됩니다
#             ADJUST_FOCAL_LENGTH -> 초점 거리만 수정
#             ADJUST_PRINCIPAL_POINT -> 주요 지점만 수정
#             ADJUST_DISTORTION -> 왜곡 계수만 수정 (있는 경우)
#             ‘|’ 옵션을 결합할 수 있음:
#                 ADJUST_FOCAL_LENGTH|ADJUST_PRINCIPAL_POINT -> 초점 거리와 기본 위치를 정합니다
#                 ADJUST_FOCAL_LENGTH|ADJUST_DISTORTION -> 초점 거리와 왜곡 계수를 수정합니다 (있는 경우).
#                 ADJUST_PRINCIPAL_POINT|ADJUST_DISTORTION -> 주요 점 위치 및 왜곡 계수를 수정합니다 (있는 경우).


# 저장할 reconstruction_global 경로 지정.
reconstruction_dir = os.path.join(output_dir,"reconstruction_global")
print ("3. Do Global reconstruction")
# pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_GlobalSfM"),  "-i", matches_dir+"/sfm_data.json", "-m", matches_dir, "-o", reconstruction_dir] )
pRecons.wait()


print ("5. Colorize Structure")
# pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", reconstruction_dir+"/sfm_data.bin", "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons.wait()

print ("4. Structure from Known Poses (robust triangulation)")
# pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons.wait()


