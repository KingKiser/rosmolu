import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import argparse

class ImageConverter(Node):
    def __init__(self, r, g, b):
        super().__init__('image_converter')
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.get_img_cb,
            10)
        self.img_pub = self.create_publisher(Image, 'image_converter', 10)
        self.bridge = CvBridge()
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def get_img_cb(self, msg):
        cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        cv_img[:, :, 0] = np.clip(cv_img[:, :, 0] + self.b, 0, 255)
        cv_img[:, :, 1] = np.clip(cv_img[:, :, 1] + self.g, 0, 255)
        cv_img[:, :, 2] = np.clip(cv_img[:, :, 2] + self.r, 0, 255)
        img_msg = self.bridge.cv2_to_imgmsg(cv_img, encoding="bgr8")
        self.img_pub.publish(img_msg)

def main(args=None):
    parser = argparse.ArgumentParser(description='Adjust image color channels.')
    parser.add_argument('r', type=float, help='Red channel adjustment')
    parser.add_argument('g', type=float, help='Green channel adjustment')
    parser.add_argument('b', type=float, help='Blue channel adjustment')
    parsed_args = parser.parse_args()

    rclpy.init(args=args)
    node = ImageConverter(parsed_args.r, parsed_args.g, parsed_args.b)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


#ros2 run your_package imageconverter 30 20 -10