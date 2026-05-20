# hangman_game/user_input.py

import rclpy
from rclpy.node import Node
from hangman_interfaces.srv import CheckLetter
import threading


class UserInput(Node):

    def __init__(self):
        super().__init__("user_input")
        self.cli = self.create_client(CheckLetter, "check_letter")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting...")
        self.req = CheckLetter.Request()
        self.get_logger().info("Press Enter to check the current letter.")
        threading.Thread(target=self.input_thread, daemon=True).start()

    def input_thread(self):
        while True:
            input("Press Enter to input the current letter.")
            self.send_request()

    def send_request(self):
        future = self.cli.call_async(self.req)
        # future.add_done_callback(self.callback_future)

    # def callback_future(self, future):
    #     response = future.result()
    #     self.get_logger().info(f'{response.message}')
    #     self.get_logger().info(f'Word State: {response.updated_word_state}')


def main(args=None):
    rclpy.init(args=args)
    user_input = UserInput()
    rclpy.spin(user_input)
    user_input.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
