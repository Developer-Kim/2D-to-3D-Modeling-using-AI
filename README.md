# Coffee is Venti Project
**물체의 여러 각도 2D 이미지를 기반으로 SfM 기술과 딥러닝을 통해 사진에서 필요한 물체를 인식하고 물체의 3D 모델링을 하는 프로젝트**  
**Recognizes objects in a photo and performs 3D modeling of objects through deep learning using SfM technology as a stereo image of objects**

## Introduction
<img src="https://user-images.githubusercontent.com/39071723/82830703-6bbbd400-9ef1-11ea-8d84-ee1b5baaa4c5.gif" width="700" height="470"></img>  
<img src="https://user-images.githubusercontent.com/39071723/82747322-bd217180-9dd2-11ea-80ce-0b73be7bf63f.png" width="700" height="370"></img>  
이 프로그램의 구성도이다. 먼저 사진 촬영을 통하여 수집한 이미지 데이터들을 [MaskRCNN](https://github.com/matterport/Mask_RCNN)을 통해 특정 객체를 인식하고 이미지 세그멘테이션 작업을 수행한다. 결과물을 OpenCV를 활용하여 특정 물체의  Mask를 만들고 [OpenMVG](https://github.com/openMVG/openMVG)에 넣어주면 불필요한 부분이 제거된 객체의 Point Cloud를 얻어낼 수 있다. 그 후 OpenMVG에서 OpenMVS 과정으로 넘어갈 때 undistort image 를 만드는데, 이 또한 OpenCV로 배경이 제거된 사진을 만들고 기존 사진을 대체하여 불필요한 부분이 제거된 undistort image 를 만들 수 있다. 이를 토대로 [OpenMVS](https://github.com/cdcseacave/openMVS)에서 Densify, Mesh, Texture 과정을 수행하여 최종적으로 깔끔한 3D 모델을 얻을 수 있다.  

See the complete [Documentation](https://github.com/ES-Justin-Kim/2D-to-3D-Modeling-using-AI/wiki) on wiki.  

<img src="https://user-images.githubusercontent.com/39071723/82821801-ac125680-9edf-11ea-878f-bdc4590d83c8.png" width="150" height="150"></img>  

Scan the QR code and check the result

## Site
<img src="https://user-images.githubusercontent.com/39071723/82827828-be45c200-9eea-11ea-8a28-0684ded73b14.gif" width="700" height="370"></img>

Click here -> www.coffeeisventi.site

## Build
See the [Building](https://github.com/ES-Justin-Kim/2D-to-3D-Modeling-using-AI/wiki/Building) wiki page.

## Example
See the [Usage](https://github.com/ES-Justin-Kim/2D-to-3D-Modeling-using-AI/wiki/Usage) wiki page.

## License
See the [Copyright](https://github.com/ES-Justin-Kim/2D-to-3D-Modeling-using-AI/tree/develop/COPYRIGHT.md) file.

## Dissertation
See the [Dissertation](https://github.com/Developer-Kim/2D-to-3D-Modeling-using-AI/blob/master/Dissertation.doc) file.

## Contact
* Hyeon Su Jeong - mses1572@naver.com  
* Kang Wook Lee - zu7342@naver.com  
* Jeong Hwan Kim - dkakdfd@naver.com  
* Ji Won Park - since1909@naver.com
