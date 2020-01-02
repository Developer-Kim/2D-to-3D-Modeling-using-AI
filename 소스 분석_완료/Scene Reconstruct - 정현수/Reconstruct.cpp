#define CERES_FOUND true
#include <opencv2/sfm.hpp>
#include <opencv2/viz.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/core.hpp>
#include <iostream>
#include <fstream>
using namespace std;
using namespace cv;
using namespace cv::sfm;
static void help() {
  // 생성된 파일 실행 방법 : ./[실행할 파일] [사진목록이 들어있는 텍스트] [f: 거리] [cx: 바라볼 x위치] [cy: 바라볼 y위치] 
  cout
      << "\n------------------------------------------------------------------------------------\n"
      << " This program shows the multiview reconstruction capabilities in the \n"
      << " OpenCV Structure From Motion (SFM) module.\n"
      << " It reconstruct a scene from a set of 2D images \n"
      << " Usage:\n"
      << "        example_sfm_scene_reconstruction <path_to_file> <f> <cx> <cy>\n"
      << " where: path_to_file is the file absolute path into your system which contains\n"
      << "        the list of images to use for reconstruction. \n"
      << "        f  is the focal length in pixels. \n"
      << "        cx is the image principal point x coordinates in pixels. \n"
      << "        cy is the image principal point y coordinates in pixels. \n"
      << "------------------------------------------------------------------------------------\n\n"
      << endl;
}
// 경로를 읽고 files 벡터에 읽은 텍스트 문서의 문자열들 저장. (문자열들은 사진 목록들)
static int getdir(const string _filename, vector<String> &files)
{
  // _filename은 argv[1], files는 images_path 벡터를 main에서 받아옴.
  ifstream myfile(_filename.c_str());

  if (!myfile.is_open()) {
    cout << "Unable to read file: " << _filename << endl;
    exit(0);
  } 
  else {
    /*  
          [ temple 폴더 안 ] 
                    1. 관련된 사진들  
                    2. 사진들의 이름목록이 있는 txt 파일 
                    ex)  temple0001.png
                           temple0002.png
                           temple0003.png

          _filename: /home/jeong/Code/temple/temple.txt
          path_to_file: /home/jeong/Code/temple 

          line_str 에 txt에 있는 목록들을 한 줄 씩 읽고
          files 벡터에  /home/jeong/Code/temple/temple0001.png 와 같이 재조합해서 main에 보냄.
    */
    size_t found = _filename.find_last_of("/\\");
    
    cout << _filename << endl;
    cout << _filename.substr(0, found) << endl;
    string line_str, path_to_file = _filename.substr(0, found);
    while ( getline(myfile, line_str) )
      files.push_back(path_to_file+string("/")+line_str);
  }
  return 1;
}
int main(int argc, char* argv[])
{
  // Read input parameters
  if ( argc != 5 )
  {
    help();
    exit(0);
  }
  // argv[1] 인자로 얻어온 경로와 getdir에서 이미지의 경로를 전달받을 images_paths를 전달.
  vector<String> images_paths;
  getdir( argv[1], images_paths );

  // Build intrinsics
  // float형태로 저장 - f: 거리, cx: 관찰자 x위치, cy: 관찰자 y위치
  float f  = atof(argv[2]),
        cx = atof(argv[3]), cy = atof(argv[4]);
  
  // 3*3 매트릭스 형성 후, f만큼 확/축소, cx/cy로 위치 이동할 변환 매트릭스 생성
  Matx33d K = Matx33d( f, 0, cx,
                       0, f, cy,
                       0, 0,  1);

  bool is_projective = true;
  vector<Mat> Rs_est, ts_est, points3d_estimated;
  /*
  reconstruct(): 자동 보정을 수행하는 동안 2D 통신에서 3D 점을 재구성.

  공식문서: https://docs.opencv.org/3.4.1/da/db5/group__reconstruction.html  - 4/4 번째

  void cv::sfm::reconstruct	(	const std::vector< String > 	images,
                                            OutputArray 	Rs,
                                            OutputArray   Ts,
                                            OutputArray 	points3d,
                                            InputOutputArray 	K,
                                            bool 	is_projective = false )

  [ 인자목록 ]
    > images: 이미지 경로가 들어있는 string 벡터
    > Ps: 카메라의 3x3 회전 출력 벡터.
    > Ts: 카메라의 3x1 변환 출력 벡터.
    > points3d: 추정 된 3d 포인트를 가진 출력 배열.
    > K: 초기 추측으로 사용되는 입력 매개 변수.  (회전/변환 매트릭스 대입)
    > is_projective: 참이면, 카메라는 투영이어야합니다.
  */
  reconstruct(images_paths, Rs_est, ts_est, K, points3d_estimated, is_projective);

  // Print output
  cout << "\n----------------------------\n" << endl;
  cout << "Reconstruction: " << endl;
  cout << "============================" << endl;
  cout << "Estimated 3D points: " << points3d_estimated.size() << endl;
  cout << "Estimated cameras: " << Rs_est.size() << endl;
  cout << "Refined intrinsics: " << endl << K << endl << endl;
  cout << "3D Visualization: " << endl;
  cout << "============================" << endl;

  // 3d 점을 출력하기 위한 Viz 초기 화면설정
  viz::Viz3d window("Coordinate Frame");
             window.setWindowSize(Size(500,500));
             window.setWindowPosition(Point(150,150));
             window.setBackgroundColor(); // black by default
 
  // Create the pointcloud
  cout << "Recovering points  ... ";
  
  // recover estimated points3d
  vector<Vec3f> point_cloud_est;

  // reconstruct함수에 의해 추정된 포인트 points3d_estimated 벡터로 
  // point_cloud_est 벡터에 Vec3f 형태로 대입.
  for (int i = 0; i < points3d_estimated.size(); ++i)
    point_cloud_est.push_back(Vec3f(points3d_estimated[i]));
  cout << "[DONE]" << endl;
  cout << "Recovering cameras ... ";

  /*
    Affine3d : 아핀행렬 ( 회전/변환 행렬 ) - 4*4 매트릭스
    
    cv::Affine3< T >::Affine3	(	const Mat3 & 	R,
                                                const Vec3 & 	t = Vec3::all(0) )	

    공식문서: https://docs.opencv.org/master/dd/d99/classcv_1_1Affine3.html - Affine3() [3/6]
    
    [ 인자 목록 ]
    R: 3*3 회전 행렬
    t:  3*1 변환 행렬
  */

  // path에 Affine3d 형식으로 reconstruct에서 얻은 Rs_est(회전행렬), ts_est(변환행렬)로 변환 후 대입
  vector<Affine3d> path;
  for (size_t i = 0; i < Rs_est.size(); ++i)
    path.push_back(Affine3d(Rs_est[i],ts_est[i]));
  cout << "[DONE]" << endl;
  
  // 포인트 클라우드 점이 존재하면 
  if ( point_cloud_est.size() > 0 )
  {
    cout << "Rendering points   ... ";

    /*
        WCloud(): 3D 포인트 클라우드

        공식문서: https://docs.opencv.org/3.4/db/d82/classcv_1_1viz_1_1WCloud.html - WCloud() [2/4]

        cv::viz::WCloud::WCloud	(	InputArray 	cloud,
                                                    const Color & 	color = Color::white() )

      	[ 인자 목록 ]
        cloud: 유형이 될 수있는 클라우드 포인트 Set - CV_32FC3, CV_32FC4, CV_64FC3, CV_64FC4.
        color: 전체 클라우드의 단일 색깔 
    */

    // point cloud를 시각적으로 볼 수 있게 함.
    viz::WCloud cloud_widget(point_cloud_est, viz::Color::green());
    window.showWidget("point_cloud", cloud_widget);
    cout << "[DONE]" << endl;
  }
  else
  {
    cout << "Cannot render points: Empty pointcloud" << endl;
  }
  if ( path.size() > 0 )
  {
    /*
        WTrajectory(): 프레임은 영향을받지 않습니다. 주어진 경로의 궤적을 다음과 같이 표시합니다.
        PATH : 경로를 나타내는 폴리 라인을 표시합니다.
        Frame : 각 포즈에서 좌표 프레임을 표시합니다.
        PATH & FRAMES : 폴리 라인과 좌표 프레임을 모두 표시합니다.
        
        공식문서: https://docs.opencv.org/3.1.0/d0/da3/classcv_1_1viz_1_1WTrajectory.html



          cv::viz::WTrajectory::WTrajectory	(	InputArray 	path,
                                                                   int 	display_mode = WTrajectory::PATH,
                                                                   double 	scale = 1.0,
                                                                   const Color & 	color = Color::white() )	

          path: 궤적에 대한 포즈 목록(Affine3d)
          display_mode: 디스플레이 모드. PATH, FRAMES 및 BOTH가 될 수 있습니다.
          scale: 프레임의 스케일. 폴리 라인은 영향을받지 않습니다.
          color: 경로를 나타내는 폴리 라인의 색상입니다.

        ==========================================================================

          viz::WTrajectoryFrustums(): 궤적의 각 포즈에서 경로를 표시합니다.

          공식문서: https://docs.opencv.org/3.1.0/da/d80/classcv_1_1viz_1_1WTrajectoryFrustums.html - [1/2]

          cv::viz::WTrajectoryFrustums::WTrajectoryFrustums	(	InputArray 	path,
                                                                                                const Matx33d & 	K,
                                                                                                double 	scale = 1.,
                                                                                                const Color & 	color = Color::white())	
      
          path: 궤적에 대한 포즈 목록(Affine3d)
          K:  카메라의 고유 매트릭스
          scale: 절두체의  크기
          color: 경로를 나타내는 폴리 라인의 색상입니다.
    */

   // 카메라 렌더링
    cout << "Rendering Cameras  ... ";
    window.showWidget("cameras_frames_and_lines", viz::WTrajectory(path, viz::WTrajectory::BOTH, 0.1, viz::Color::green()));
    window.showWidget("cameras_frustums", viz::WTrajectoryFrustums(path, K, 0.1, viz::Color::yellow()));
    window.setViewerPose(path[0]);
    cout << "[DONE]" << endl;
  }
  else
  {
    cout << "Cannot render the cameras: Empty path" << endl;
  }
  cout << endl << "Press 'q' to close each windows ... " << endl;
  window.spin();
  return 0;
}