import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2  # OpenCV 사용
import mediapipe as mp #얼굴찾기


#def overlay_image(background, overlay, x, y, w, h):
 #   """배경 위에 오버레이 이미지를 특정 위치(x, y)에 덮어씌우기"""
  #  overlay_resized = cv2.resize(overlay, (w, h), interpolation=cv2.INTER_AREA) #오버레이 이미지 크기 재정의

    # 채널 분리
   # overlay_rgb = overlay_resized[:, :, :3]  # RGB
    #overlay_alpha = overlay_resized[:, :, 3] / 255.0  # Alpha

    # 배경과 오버레이 합성
    #for c in range(3):  # RGB 채널 반복
     #   background[y:y+h, x:x+w, c] = (
      #      overlay_alpha * overlay_rgb[:, :, c] +
       #     (1 - overlay_alpha) * background[y:y+h, x:x+w, c]
        #)
def overlay_image(background, overlay, x, y, w, h):
    """배경 위에 오버레이 이미지를 특정 위치(x, y)에 덮어씌우기"""
    overlay_resized = cv2.resize(overlay, (w, h), interpolation=cv2.INTER_AREA)  # 오버레이 이미지 크기 재정의

    # 채널 분리
    overlay_rgb = overlay_resized[:, :, :3]  # RGB
    overlay_alpha = overlay_resized[:, :, 3] / 255.0  # Alpha

    # 좌표와 크기 검증
    if y + h > background.shape[0]:  # 높이가 초과할 경우
        h = background.shape[0] - y
    if x + w > background.shape[1]:  # 너비가 초과할 경우
        w = background.shape[1] - x
    if h <= 0 or w <= 0:
        return  # 유효하지 않은 영역은 스킵

    # 배경과 오버레이 합성
    for c in range(3):  # RGB 채널 반복
        background[y:y+h, x:x+w, c] = (
            overlay_alpha[:h, :w] * overlay_rgb[:h, :w, c] +
            (1 - overlay_alpha[:h, :w]) * background[y:y+h, x:x+w, c]
        )


class molu(Node):
    def __init__(self):
        super().__init__('molu_node')
        self.declare_parameter('pathconfig', 'molu.png')
        self.subscription = self.create_subscription(
            Image, 
            '/image_raw', 
            self.image_callback, 
            10)
        self.img_pub = self.create_publisher(Image, 'molu_yaml', 10)
        self.subscription  # Prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.bridge = CvBridge()

        # Load YOLOv8 model

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")  # 영상 변환
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        img_path = '/home/rokey/ros2_ws/src/config/' + self.get_parameter('pathconfig').get_parameter_value().string_value
        
        overlay_img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)  # PNG 이미지 (투명 배경 지원)

        # Perform object detection using YOLOv8
        with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7) as face_detection:

            results = face_detection.process(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
            if results.detections:
                    for detection in results.detections:
                        bboxC = detection.location_data.relative_bounding_box
                        ih, iw, _ = cv_img.shape
                        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                        
                        # 좌표 범위 확인
                        x = max(0, x)
                        y = max(0, y)
                        w = min(w, iw - x)  # 얼굴 영역 너비 초과 방지
                        h = min(h, ih - y)  # 얼굴 영역 높이 초과 방지

                        # 얼굴 영역에 모자이크 적용
                        overlay_image(cv_img, overlay_img, x, y, w, h)

        # Publish the processed image
        img_msg = self.bridge.cv2_to_imgmsg(cv_img, encoding="bgr8")  # 영상 변환
        self.img_pub.publish(img_msg)  # 영상 송출

def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the YOLOv8 node
    node = molu()

    # Spin the node so the callback function is called
    rclpy.spin(node)

    # Destroy the node explicitly
    node.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()

if __name__ == '__main__':
    main()