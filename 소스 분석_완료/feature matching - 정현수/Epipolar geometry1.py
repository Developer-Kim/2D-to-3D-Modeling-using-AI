import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('E://r.jpg', 0)  # queryimage # left image
img2 = cv2.imread('E://l.jpg', 0)  # trainimage # right image

# SIFT의 키포인트, 디스크립터들을 계산하는 함수를 제공
sift = cv2.xfeatures2d.SIFT_create()    

# GrayImg에서 키포인트와 디스크립터를 한번에 계산하고 리턴
# 키포인트 : 특징들
# 디스크립터 : 특징점의 주변 특성을 이용해 해당 특징점을 표현하는 벡터를 만들어 이미지에서 같은 특징점을 매칭하거나 추출 할 때 사용
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN 기반 Matcher, 알고리즘을 수행하기 위해 2개 Dictionary 필요.
# FLANN parameters 설정
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=100) # 특성 매치를 위한 반복 횟수

# FLANN 기반 매칭 객체 생성
flann = cv2.FlannBasedMatcher(index_params, search_params)
# KNN 매칭 수행 - k=2 는 2번째로 가까운 매칭 결과까지 리턴
# matches는 2개의 결과가 들어있는 리스트가 됌.
matches = flann.knnMatch(des1, des2, k=2)

good = []
pts1 = []
pts2 = []

factor = 0.8

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    # 1순위 거리(m)가 2순위 거리(n) * factor 만큼 더 가까운 값만을 사용
    if m.distance < factor * n.distance:
        good.append(m)
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)
pts1 = np.int32(pts1)
pts2 = np.int32(pts2)

# 스테레오 비전을 위한 Fundamental 매트릭스 구함.
# 인자로는 1, 2번째 사진들의 포인트, 방법
# F는 Fundamental 매트릭스.
# mask는 N 요소의 출력 배열로, 모든 요소는 특이치의 경우 0으로, 다른 점의 경우 1로 설정됩니다. 
# 배열은 RANSAC 및 LMedS 메소드에서만 계산됩니다. 다른 방법의 경우 모두 1로 설정됩니다.
# 계산 된 기본 행렬은 지정된 점들에 해당하는 에피폴라 선을 찾는 computeCorrespondEpilines()에 전달가능. 
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)

# We select only inlier points
pts1 = pts1[mask.ravel() == 1]
pts2 = pts2[mask.ravel() == 1]


def drawlines(img1, img2, lines, pts1, pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r, c = img1.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)

    return img1, img2


# 오른쪽 이미지 (두 번째 이미지)의 점에 해당하는 에피라인 찾기
# 왼쪽 이미지에 선 그리기
# computeCorrespondEpilines 인자(포인트(N*1 or 1*N), 점을 포함할 이미지 인덱스, Fundamental Matrix
# 왼쪽 이미지는 오른쪽 이미지의 인덱스(2)를 대입
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
lines1 = lines1.reshape(-1, 3)
img5, img6 = drawlines(img1, img2, lines1, pts1, pts2)

# 오른쪽 이미지는 왼쪽 이미지의 인덱스(1)를 대입
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
lines2 = lines2.reshape(-1, 3)
img3, img4 = drawlines(img2, img1, lines2, pts2, pts1)

plt.subplot(121), plt.imshow(img5)
plt.subplot(122), plt.imshow(img3)
plt.show()
