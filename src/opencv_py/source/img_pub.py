import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImagePublisher(Node):
    def __init__(self):
        super().__init__("image_publisher")
        self.declare_and_fetch_parameters()
        self.bridge = CvBridge()
        self.publisher = self.create_publisher(Image, "original_image", 10)
        self.setup_timer()

    def declare_and_fetch_parameters(self):
        """Declare and fetch the image path parameter."""
        self.declare_parameter("image_path", "")
        image_path_param = (
            self.get_parameter("image_path").get_parameter_value().string_value
        )
        if not image_path_param:
            self.get_logger().error(
                "No image path provided. Use '--ros-args -p image_path:=<path_to_image>'"
            )
            rclpy.shutdown()
        self.image_path = image_path_param

    def setup_timer(self):
        """Set up a timer to publish images at regular intervals."""
        self.timer = self.create_timer(0.1, self.publish_image)

    def publish_image(self):
        """Read an image from file and publish it."""
        cv_image = cv2.imread(self.image_path)
        if cv_image is None:
            self.get_logger().error(f"Failed to load image from {self.image_path}")
            return

        ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
        self.publisher.publish(ros_image)
        self.get_logger().info(
            f"Published image: {self.image_path} with shape {cv_image.shape}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
