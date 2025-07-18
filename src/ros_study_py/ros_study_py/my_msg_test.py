import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from ros_study_msgs.msg import MyMsg


class my_msg_test(Node):

    def __init__(self):
        super().__init__('my_msg_test')
        qos_profile = QoSProfile(depth=10)
        self.publisher_ = self.create_publisher(MyMsg, 'MyMsg', qos_profile)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        msg = MyMsg()
        msg.num = self.i
        self.publisher_.publish(msg)
        self.get_logger().info(str(self.i))
        #로그를 찍는 함수
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    my_msg_test_publisher = my_msg_test()

    rclpy.spin(my_msg_test_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    my_msg_test_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()