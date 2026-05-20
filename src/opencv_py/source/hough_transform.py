import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class HoughTransform(Node):
    def __init__(self):
        super().__init__("hough_transform")
        self.method = (
            self.declare_parameter("method", "").get_parameter_value().string_value
        )
        self.bridge = CvBridge()
        self.subscriber = self.create_subscription(
            Image, "original_image", self.process_image, 10
        )
        self.publisher = self.create_publisher(Image, "hough_transform", 10)
        if not self.method:
            self.get_logger().error(
                "No method provided. Use '--ros-args -p method:=<method>'"
            )
            rclpy.shutdown()

    def process_image(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        if self.method == "circle":
            processed_image = self.detect_circles(cv_image)
        elif self.method == "line":
            processed_image = self.detect_lines(cv_image)
        else:
            self.get_logger().error(f"Invalid method: {self.method}")
            return
        self.publisher.publish(
            self.bridge.cv2_to_imgmsg(processed_image, encoding="bgr8")
        )

    def detect_circles(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(
            cv2.GaussianBlur(gray, (9, 9), 2),
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=50,
            param2=37,
            minRadius=80,
            maxRadius=100,
        )
        if circles is not None:
            for x, y, r in np.round(circles[0, :]).astype("int"):
                cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                cv2.circle(img, (x, y), 2, (0, 0, 255), 12)
        return img

    def detect_lines(self, img):
        edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 200)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, None, 20, 2)
        if lines is not None:
            for x1, y1, x2, y2 in lines[:, 0]:
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
        return img


def main(args=None):
    rclpy.init(args=args)
    node = HoughTransform()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
