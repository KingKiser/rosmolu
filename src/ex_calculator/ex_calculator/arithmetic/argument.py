import random

from ros_study_msgs.msg import ArithmeticArgument
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from rclpy.logging import LoggingSeverity #로그 레벌 설정해주는 함수가 들어있는 라이브러리

class Argument(Node):

    def __init__(self):
        super().__init__('argument')
        self.get_logger().set_level(LoggingSeverity.INFO) #로그 레벌 설정 함수
        self.get_logger().info('Argument init set start')

        self.declare_parameter('qos_depth', 10)
        qos_depth = self.get_parameter('qos_depth').value #10이 들어간다
        self.get_logger().info(f'qos_depth set {qos_depth}') #qos_depth에 뭐가 들어갔는지 로그로 확인가능

        self.declare_parameter('min_random_num', 0)
        self.min_random_num = self.get_parameter('min_random_num').value
        self.get_logger().info(f'min_random_num set {self.min_random_num}')

        self.declare_parameter('max_random_num', 9)
        self.max_random_num = self.get_parameter('max_random_num').value
        self.get_logger().info(f'max_random_num set {self.max_random_num}')

        self.add_on_set_parameters_callback(self.update_parameter)
        self.get_logger().info(f'add_on_set_parameters_callback on')

        QOS_RKL10V = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
            durability=QoSDurabilityPolicy.VOLATILE)
        self.get_logger().info('QOS_RKL10V get QoSProfile')

        self.arithmetic_argument_publisher = self.create_publisher(
            ArithmeticArgument,
            'arithmetic_argument',
            QOS_RKL10V)
        self.timer = self.create_timer(1.0, self.publish_random_arithmetic_arguments)
        self.get_logger().info('publish topic : arithmetic_argument_publisher')
        self.get_logger().info('end init')

    def publish_random_arithmetic_arguments(self):
        self.get_logger().info('start publish_random_arithmetic_arguments')
        msg = ArithmeticArgument()
        msg.stamp = self.get_clock().now().to_msg()
        msg.argument_a = float(random.randint(self.min_random_num, self.max_random_num))
        msg.argument_b = float(random.randint(self.min_random_num, self.max_random_num))
        self.arithmetic_argument_publisher.publish(msg)
        self.get_logger().info(f'Published argument a: {msg.argument_a}')
        self.get_logger().info(f'Published argument b: {msg.argument_b}')

    def update_parameter(self, params):
        self.get_logger().info('start update_parameter')
        for param in params:
            if param.name == 'min_random_num' and param.type_ == Parameter.Type.INTEGER:
                self.min_random_num = param.value
                self.get_logger().info(f'self.min_random_num = {self.min_random_num}')
            elif param.name == 'max_random_num' and param.type_ == Parameter.Type.INTEGER:
                self.max_random_num = param.value
                self.get_logger().info(f'self.max_random_num = {self.max_random_num}')
        return SetParametersResult(successful=True)
        #여기에 로그 남기면 안됨 return에서 함수 끝

def main(args=None):
    rclpy.init(args=args)
    try:
        argument = Argument()
        try:
            rclpy.spin(argument)
        except KeyboardInterrupt:
            argument.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            argument.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
