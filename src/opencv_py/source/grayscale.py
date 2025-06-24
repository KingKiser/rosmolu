import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2  # OpenCV 사용



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
class ImageConvertor(Node):
    def __init__(self):
        super().__init__('image_grayscale')
        self.subscription = self.create_subscription(
            Image, 
            '/image_raw', #topic name
            self.image_callback, 
            10)
        self.img_pub = self.create_publisher(Image, 'image_gray', 10)
        self.subscription  # Prevent unused variable warning

        # Used to convert between ROS and OpenCV images
        self.bridge = CvBridge()

        # Load YOLOv8 model
    def image_callback(self, msg):
        #self.get_logger().info('---')
    
        cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        img_gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        '''
        cv2.imshow("grayscale", img_gray)
        
        cv2.waitKey(1)
        '''
        img_msg = self.bridge.cv2_to_imgmsg(img_gray)
        self.img_pub.publish(img_msg)

def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the YOLOv8 node
    node = ImageConvertor()

    # Spin the node so the callback function is called
    rclpy.spin(node)

    # Destroy the node explicitly
    node.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown()

if __name__ == '__main__':
    main()