# rosmolu
집중반 수업에서 진행한 박승휘 개발 코드 모음
hough 변환 파일에 AI 모델 mediapipe를 응용하여 사람의 얼굴을 발견하면 몰?루 이미지를 덮어 씌운다.
파라메터를 변경하여 덮어 씌우는 이미지를 바꿀 수 있다
(hough_transform에 해당 코드 넣음 근데 내가 모델이나 이미지 경로를 절대경로로 박았는데
문제는 이 프로젝트 이름이 해당 절대경로와 이름이 다름 ㅋ 
알아서 프로젝트 이름을 rosmolu -> ros2_ws로 바꾸고 colcon build해서 쓸것)


또한 로그 추적의 샘플로 ex_calculator에서 로그를 추가해 로그에서 함수 추적이 가능하게 만들었다
샘플로 오브젝트 디텍션 모델을 ROS에 얻고, 해당 모델을 활용하는 코드도 있으며 오브젝트 디텍션 모델은
git main에 참고

-------2025.04.19----

cpp로 pubsub, excaculator 구현 완
기존 파이썬 패키지와도 연동이 됨(상속 구조도 최대한 비슷하게 만들어서 두 코드를 비교하면서 사용가능)
원래 cpp_excalculator도 변태적으로 로그 남겨서 수업때 쓸려고 했는데 그건 수업 때 학생들이 하게 할거임 ㅋㅋ
hangman cpp버전은 학생 실습용을 할거임 ㅋㅋㅋ

-------2025.12.26----

google AI studio ros2 연동 api -key는 개인것으로 쓸것
결제 계정 연동해야지 gemini 측에서 엑세스됨
간단하게 터틀심 움직이게만 해놨고 스크립트 수정 필요
로봇 사양에 맞게 스크립트를 만들어서 출력 사양을 고정 시키면 자연어로 로봇 제어가 가능하게 되는 원리임
간단하게 서비스랑 인터페이스만 만들었으니 나머지는 알아서 해야지 
터틀봇 움직이고 로봇팔 움직이는 것까지 내가 해줄 순 없잖어
참고로 스레드 충돌이슈도 있어서 그것도 코드 넣음

-------2026.02.05----

딱히 중요한 이슈는 아닌데 Window 환경에서 Docker로 ROS2를 셋팅하고 구동 시 LangChain 비동기 이슈가 발생하는걸 확인했다
근데 Window 환경이라서 거기다 ROS2 돌리는 인간이 없겠지만 간단하게 수업하려고 Docker에 돌려보니 알고 말았고 디버깅해야 했다.
다른데 Docker 컨테이너에서도 동일 이슈가 발생하는지는 몰?루라서 제미나이에 물어보니 WSL의 자원 할당 이슈와 DDS 추상화
파이썬의 **GIL(Global Interpreter Lock) 라고 한다.
결론은 ROS2는 리눅스에서 돌려라

-------2026.02.05----


도커 파일도 추가했다

git clone https://github.com/KingKiser/rosmolu.git

cd rosmolu/docker
docker build -t my_ros_env .
docker run -it my_ros_env

참고로 윈도우에서 rqt나 gazebo 돌릴려면 xlaunch 설치해야 한다 자세한 내용은
https://with-rl.tistory.com/entry/Windows%EC%97%90%EC%84%9C-Docker%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%B4-ROS2-Gazebo-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0
이 링크 참고

참고로 윈도우에서 도커로 ROS2 돌리면 외부로 DDS 안 붙는다 
인바운드 규칙이니 방화벽이니 뭐니 뚫어서 쓰는게 가능한거 같지만
어쨌든 혼자 공부할 때나 쓸것

-------2026.04.11----

미디어 파이프 api 변경 이슈로 아래 버전을 설치해야 함 코드 수정은 귀찮

python3 -m pip uninstall -y mediapipe

python3 -m pip install --user mediapipe==0.10.21
