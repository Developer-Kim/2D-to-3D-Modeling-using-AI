#include <iostream>
#include <fstream>
#include <iomanip>

using namespace std;

int main(){
    string t;
    cout << "저장할 경로 입력 : ";
    cin >> t;

    ofstream of(t);
    string s = "temple0";
    
    cout << "사진 범위 설정(x ~ y)" << endl;
    cout << "두 가지 숫자 입력: ";
    int x,y;
    cin >> x >> y;

    for(int i=x; i<=y;i++){
        of << s << std::setw(3) << std::setfill('0') << i << ".png";
        if(i != y) of << "\n";
    }

    return 0;
}