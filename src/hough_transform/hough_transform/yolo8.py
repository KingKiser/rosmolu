import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO

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
        cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8") #영상 넣는 코드
        
        # Perform object detection using YOLOv8
        results = self.model(cv_img) #욜로 모델에 영상 넣음
        
        # Visualize detections on the image
        annotated_img = results[0].plot() # 인식 영역 만들어줌

        # Publish the annotated image
        img_msg = self.bridge.cv2_to_imgmsg(annotated_img, encoding="bgr8") #인식영역을 영상에 넣음
        self.img_pub.publish(img_msg) #인식영역이 들어간 영상 송출

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
