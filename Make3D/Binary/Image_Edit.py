import cv2
import os
from shutil import copyfile

def Not_Mask_Delete(input_dir):
    mask_list = set()           # 마스크 리스트
    no_mask_list = set()        # 마스크가 없는 사진 리스트

    #=====================================
    # 마스크 사진이 없는 사진들 리스트 뽑아오기
    #=====================================
    file_list = os.listdir(input_dir)
    for str_ in file_list:
        if "." in str_:
            if "_mask" in str_:
                mask_list.add(str_)
            else:
                if str_[-4] == '.':
                    extension = str_[-4:]
                str_ = str_[:-4] + "_mask.png"
                no_mask_list.add(str_)                    

    lst = list(no_mask_list - mask_list)

    # 없는 사진들을 삭제
    for i in range(len(lst)):
        lst[i] = ''.join(lst[i][:-9]) + extension
        os.remove(os.path.join(input_dir, lst[i]))


def White_Change(input_dir, ChangeWhite_dir):
    file_list = os.listdir(input_dir)

    mask_list = set()           # 마스크 리스트
    no_mask_list = set()        # 마스크가 없는 사진 리스트

    #=====================================
    # 마스크 사진이 없는 사진들 리스트 뽑아오기
    #=====================================
    for str_ in file_list:
        if "." in str_:
            if "_mask" in str_:
                mask_list.add(str_)
            else:
                if str_[-4] == '.':
                    extension = str_[-4:]
                str_ = str_[:-4] + "_mask.png"
                no_mask_list.add(str_)

    lst = list(no_mask_list - mask_list)

    for i in range(len(lst)):
        lst[i] = ''.join(lst[i][:-9]) + extension
    lst = set(lst)
    
    for str_ in file_list:
        path = os.path.join(input_dir, str_)

        #============================================
        #           배경이 하얀색인 사진 뽑아오기
        #============================================
        if "_mask" in str_:
            # 컬러 사진 로드
            color_dir = os.path.join(input_dir,str_[:-9] + extension)
            img = cv2.imread(color_dir)
            # 마스크 사진 로드
            mask = cv2.imread(path, 0)
            
            # 이미지, 마스크 Shape
            i_height, i_width = img.shape[0], img.shape[1]
            m_height, m_width = mask.shape
            
            # 마스크 사진과 컬러 사진 크기 동일할 시.
            if m_height == i_height and m_width == i_width: 

                # 마스크를 적용시킨 하얀색 배경 사진 뽑아오기
                img_white = ~mask
                img_white = cv2.cvtColor(img_white, cv2.COLOR_GRAY2BGR)
            
                # 비트마스크를 적용
                res = cv2.bitwise_and(img, img, mask = mask)
                
                # 가중치를 적용하여 배경이 제거된 하얀색 배경 추출.
                weighted_img = cv2.add(res, img_white)
                
                # 경로 지정
                mask_png = os.path.join(ChangeWhite_dir, str_[:-9] + extension)
                print(mask_png)
                # 사진 Write
                cv2.imwrite(mask_png, weighted_img)

        else:
            if str_ in lst:
                copyfile(os.path.join(input_dir, str_), os.path.join(ChangeWhite_dir, str_)) 


def Rotation(img):
    height, width = img.shape[0], img.shape[1]
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
    rotated_mat = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))

    return rotated_mat