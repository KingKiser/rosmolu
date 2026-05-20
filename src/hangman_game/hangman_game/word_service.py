# hangman_game/word_service.py

import rclpy
from rclpy.node import Node
from hangman_interfaces.srv import CheckLetter
from hangman_interfaces.msg import Progress
from std_msgs.msg import String
import random


class WordService(Node):

    def __init__(self):
        super().__init__("word_service")
        self.service = self.create_service(
            CheckLetter, "check_letter", self.check_letter_callback
        )
        self.subscription = self.create_subscription(
            String, "letter_topic", self.letter_callback, 10
        )
        self.progress_publisher = self.create_publisher(Progress, "progress", 10)

        data = Progress()
        data.current_state = ""
        data.attempts_left = 20
        data.game_over = False
        data.won = False
        self.progress_publisher.publish(data)

        self.current_letter = ""
        #self.word_list = ["python", "hangman", "robot", "ros", "interface"]
        self.declare_parameter('word_list', ["python", "hangman", "robot", "ros", "interface"])
        self.word_list  = self.get_parameter('word_list').get_parameter_value().string_array_value
        self.get_logger().info(f"{self.word_list}")
        self.word = random.choice(self.word_list)
        self.word_state = ["_"] * len(self.word)
        self.get_logger().info(f"The word has {len(self.word)} letters.")
        self.attempts_left = 20  # Max attempts

    def letter_callback(self, msg):
        self.current_letter = msg.data

    def check_letter_callback(self, request, response):
        letter = self.current_letter
        if letter in self.word:
            for idx, char in enumerate(self.word):
                if char == letter:
                    self.word_state[idx] = letter
            response.is_correct = True
            response.message = "Correct!"
        else:
            self.attempts_left -= 1
            response.is_correct = False
            response.message = "WRONG"
        response.updated_word_state = "".join(self.word_state)
        self.get_logger().info(f"Received letter: {letter}")
        self.get_logger().info(f"Current word state: {response.updated_word_state}")

        # Publish progress
        progress_msg = Progress()
        progress_msg.current_state = response.updated_word_state
        progress_msg.attempts_left = self.attempts_left
        progress_msg.game_over = "_" not in self.word_state or self.attempts_left <= 0
        progress_msg.won = "_" not in self.word_state
        self.progress_publisher.publish(progress_msg)

        return response


def main(args=None):
    rclpy.init(args=args)
    word_service = WordService()
    rclpy.spin(word_service)
    word_service.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
