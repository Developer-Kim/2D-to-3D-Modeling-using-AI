import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import ssl
import cv2

context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context

# Root directory of the project
ROOT_DIR = os.path.abspath("./Mask_RCNN")
print(ROOT_DIR)

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.visualize import display_images

# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "detect/car/"))  # To find local version
import car

# plt.show()
# plt.savefig('result.png',dpi=300)

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_car_0030.h5")
# Download COCO trained weights from Releases if needed
#if not os.path.exists(COCO_MODEL_PATH):
#    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.abspath("./Images_car")

class InferenceConfig(car.CarConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['bg','car']



def Make_Mask():
    #=====================================
    #       사진의 마스크를 만들고 저장
    #=====================================

    file_names = next(os.walk(IMAGE_DIR))[2]
    for name in file_names:
        image = skimage.io.imread(os.path.join(IMAGE_DIR, name))

        # Run detection
        results = model.detect([image], verbose=1)

        # 해당 이미지의 mask 좌표를 얻어오고, 재조합
        r = results[0]

        lists = dict()
        for i in range(0, len(r['masks'])):
            data = [pos for pos, val in enumerate(r['masks'][i]) if val == True]
            if len(data) != 0:
                lists[i] = data

        pos = list()
        for i in lists:
                for j in lists[i]:
                    pos.append([i,j])

        pos = np.array(pos, np.int32)

        # 해당 이미지의 좌표를 통해 mask 제작
        img = np.zeros((image.shape[1],image.shape[0]),np.uint8)
        img = cv2.polylines(img, [pos], False, (255, 255, 255), 1)

        # 마스크를 좌우반전 및 로테이션 작업을 통해 기존의 사진과 일치시킴
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_flip = cv2.flip(img_rgb, 1) # 1은 좌우 반전, 0은 상하 반전입니다.

        height, width, _ = img_flip.shape
        image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, 90, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0,0])
        abs_sin = abs(rotation_mat[0,1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w/2 - image_center[0]
        rotation_mat[1, 2] += bound_h/2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rotated_mat = cv2.warpAffine(img_flip, rotation_mat, (bound_w, bound_h))

        # 사진 저장
        mask_png = IMAGE_DIR+"/Mask/"+ name[:-4]+"_mask.png"
        cv2.imwrite(mask_png, rotated_mat)
