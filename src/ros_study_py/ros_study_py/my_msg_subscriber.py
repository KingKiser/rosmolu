import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from ros_study_msgs.msg import MyMsg

class MyMsgSubscriber(Node):

    def __init__(self):
        super().__init__('my_msg_subscriber')
        qos_profile = QoSProfile(depth=10)
        self.subscription = self.create_subscription(
            MyMsg,
            'MyMsg',
            self.listener_callback,
            qos_profile
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.num}')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MyMsgSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
