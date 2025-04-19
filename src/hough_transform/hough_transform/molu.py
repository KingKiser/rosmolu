import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import mediapipe as mp
import cv2

def overlay_image(background, overlay, x, y, w, h):
    """배경 위에 오버레이 이미지를 특정 위치(x, y)에 덮어씌우기"""
    overlay_resized = cv2.resize(overlay, (w, h), interpolation=cv2.INTER_AREA)

    # 채널 분리
    overlay_rgb = overlay_resized[:, :, :3]  # RGB
    overlay_alpha = overlay_resized[:, :, 3] / 255.0  # Alpha

    # 배경과 오버레이 합성
    for c in range(3):  # RGB 채널 반복
        background[y:y+h, x:x+w, c] = (
            overlay_alpha * overlay_rgb[:, :, c] +
            (1 - overlay_alpha) * background[y:y+h, x:x+w, c]
        )


class Molu(Node):
    def __init__(self):
        super().__init__('molu_node')
        self.subscription = self.create_subscription(
            Image, 
            '/image_raw', 
            self.image_callback, 
            10)
        self.img_pub = self.create_publisher(Image, 'molu', 10)
        self.subscription  # Prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.bridge = CvBridge()

        # Load YOLOv8 model
      #  self.model = YOLO('/home/rokey/Downloads/yolov8_forros/yolov8n.pt')  # 욜로 로드

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8") #영상 넣는 코드
        mp_drawing = mp.solutions.drawing_utils
        mp_face_detection = mp.solutions.face_detection
        img_path = '/home/seonghwi/ros2_ws/src/config/' + self.get_parameter('pathconfig').get_parameter_value().string_value
        #img_path = '/home/rokey/ros2_ws/src/config/20.png'

        overlay_img =  cv2.imread(img_path, cv2.IMREAD_UNCHANGED) #이미지 경로 
        
        with mp_face_detection.FaceDetection(model_selection = 0, min_detection_confidence = 0.7) as face_detection:
            results = face_detection.process(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)) #얘가 얼굴을 찾아 주는구나
            if results.detections:
                    for detection in results.detections:
                        bboxC = detection.location_data.relative_bounding_box
                        ih, iw, _ = cv_img.shape
                        x, y, w, h = int(bboxC.xmin *iw), int(bboxC.ymin *ih), int(bboxC.width *iw), int(bboxC.height *ih)
                        # 좌표 범위 확인
                        x = max(0, x)
                        y = max(0, y)
                        w = min(w, iw - x)  # 얼굴 영역 너비 초과 방지
                        h = min(h, ih - y)  # 얼굴 영역 높이 초과 방지



                        #img = mosaic(img, x, y, w, h, rate = 15)
                        overlay_image(cv_img, overlay_img, x, y, w, h)
        # Publish the annotated image
            img_msg = self.bridge.cv2_to_imgmsg(overlay_img, encoding="bgr8") #인식영역을 영상에 넣음
            self.img_pub.publish(img_msg) #인식영역이 들어간 영상 송출

def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the YOLOv8 node
    node = Molu()

    # Spin the node so the callback function is called
    rclpy.spin(node)

    # Destroy the node explicitly
    node.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()

if __name__ == '__main__':
    main()
