import rclpy
from rclpy.node import Node
from ros_study_msgs.srv import MySrv

class MyServiceClient(Node):

    def __init__(self):
        super().__init__('my_service_client')
        self.cli = self.create_client(MySrv, 'my_service')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        self.req = MySrv.Request()
        self.req.num = 3.14

        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    node = MyServiceClient()

    rclpy.spin_until_future_complete(node, node.future)
    if node.future.result() is not None:
        node.get_logger().info(f"Result: {node.future.result().res}")
    else:
        node.get_logger().error('Service call failed')
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
