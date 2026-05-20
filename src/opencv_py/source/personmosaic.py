import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2

def apply_mosaic(img, x, y, w, h, rate):
    """모자이크 적용 함수"""
    roi = img[y:y+h, x:x+w]  # ROI 설정
    roi = cv2.resize(roi, (w // rate, h // rate))  # 축소
    roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_AREA)  # 다시 확대
    img[y:y+h, x:x+w] = roi  # 원본 이미지에 적용
    return img

class YOLOv8Node(Node):
    def __init__(self):
        super().__init__('yolov8_node')
        self.subscription = self.create_subscription(
            Image, 
            '/image_raw', 
            self.image_callback, 
            10)
        self.img_pub = self.create_publisher(Image, 'image_yolo', 10)
        self.subscription  # Prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.bridge = CvBridge()

        # Load YOLOv8 model
        self.model = YOLO('/home/seonghwi/Downloads/yolov8_forros/yolov8n.pt')  # 욜로 로드

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")  # 영상 변환

        # Perform object detection using YOLOv8
        results = self.model(cv_img)  # 욜로 모델에 영상 입력

        # Get detections
        for result in results[0].boxes:  # YOLO 탐지 결과 순회
                cls = int(result.cls[0])  # 클래스 ID
                x1, y1, x2, y2 = map(int, result.xyxy[0])  # 바운딩 박스 좌표
                
                if self.model.names[cls] == "person":  # 클래스가 "person"인지 확인
                    cv_img = apply_mosaic(cv_img, x1, y1, x2-x1, y2-y1, rate = 15)
            
        # Publish the processed image
        img_msg = self.bridge.cv2_to_imgmsg(cv_img, encoding="bgr8")  # 영상 변환
        self.img_pub.publish(img_msg)  # 영상 송출

def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the YOLOv8 node
    node = YOLOv8Node()

    # Spin the node so the callback function is called
    rclpy.spin(node)

    # Destroy the node explicitly
    node.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()

if __name__ == '__main__':
    main()
