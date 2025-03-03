# hangman_game/progress_action_server.py

import rclpy
from rclpy.node import Node
from hangman_interfaces.action import GameProgress
from hangman_interfaces.msg import Progress
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
import time
import threading


class ProgressActionServer(Node):

    def __init__(self):
        super().__init__("progress_action_server")
        self._action_server = ActionServer(
            self, GameProgress, "game_progress", self.execute_callback
        )
        self.current_progress = Progress()
        self.progress_received_event = threading.Event()

        # Subscribe to the 'progress' topic to get game updates
        self.subscription = self.create_subscription(
            Progress, "progress", self.progress_callback, 10
        )
        self.subscription  # prevent unused variable warning

        self.get_logger().info("Action Server Initialized")
        self.get_logger().info(f"GAME OVER: {self.current_progress.game_over}")
        self.get_logger().info(f"WON: {self.current_progress.won}")

    def progress_callback(self, msg):
        self.current_progress = msg
        self.get_logger().info(
            f"Progress updated: {self.current_progress.current_state}"
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info("Action Server: Received goal request")
        feedback_msg = GameProgress.Feedback()
        update_rate = 1.0  # seconds

        while not self.current_progress.game_over:
            # Publish feedback
            feedback_msg.game_over = self.current_progress.game_over
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(
                f"Current State: {self.current_progress.current_state}"
            )
            self.get_logger().info(
                f"Attempts Left: {self.current_progress.attempts_left}"
            )

            # Sleep to wait for next update
            time.sleep(update_rate)

            # Check if the goal has been canceled
            # if goal_handle.is_cancel_requested:
            #     self.get_logger().info('Action Server: Goal canceled')
            #     goal_handle.canceled()
            #     return GameProgress.Result()

        # Game is over
        result = GameProgress.Result()
        result.game_over = self.current_progress.game_over
        result.won = self.current_progress.won

        if self.current_progress.won:
            self.get_logger().info("Action Server: Congratulations! You won!")
        else:
            self.get_logger().info("Action Server: Game Over. You lost.")

        goal_handle.succeed()
        self.get_logger().info("Action Server: Goal succeeded")
        return result


def main(args=None):
    rclpy.init(args=args)
    action_server = ProgressActionServer()

    # Use MultiThreadedExecutor to allow concurrent callbacks
    executor = MultiThreadedExecutor()
    executor.add_node(action_server)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        action_server.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
