import os

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_srvs.srv import Empty


class ImageConverter(Node):
    def __init__(self):
        super().__init__('image_converter')

        # Subscribe to the image topic
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10)

        # Create a service to save images
        self.create_service(Empty, 'save_image', self.save_image_callback)
        self.get_logger().info("Service 'save_image' is ready. Call the service to save the image.")

        # Initialize variables
        self.bridge = CvBridge()
        self.img_counter = 0
        self.latest_img = None

        # Prepare the directory to save images
        self.save_path = os.path.join(os.path.expanduser("~"), "saved_images")
        os.makedirs(self.save_path, exist_ok=True)

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        self.latest_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")

    def save_image_callback(self, request, response):
        if self.latest_img is not None:
            # Save the latest image
            img_filename = os.path.join(self.save_path, f"image_{self.img_counter}.png")
            cv2.imwrite(img_filename, self.latest_img)
            self.get_logger().info(f"Saved image: {img_filename}")
            self.img_counter += 1
        else:
            self.get_logger().warn("No image received yet.")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ImageConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

#ros2 service call /save_image std_srvs/srv/Empty