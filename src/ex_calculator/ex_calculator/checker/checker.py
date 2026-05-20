# Copyright 2021 OROCA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from action_msgs.msg import GoalStatus
#액션 피드백의 모듈을 넣음 골에 대한 작업 상태 피드백
from ros_study_msgs.action import ArithmeticChecker
#인터페이스
from rclpy.action import ActionClient
#액션 클라이언트
from rclpy.node import Node


class Checker(Node):

    def __init__(self):
        super().__init__('checker') #노드 이름 설정
        self.arithmetic_action_client = ActionClient(
          self,
          ArithmeticChecker,
          'arithmetic_checker') #액션 이름 설정

    def send_goal_total_sum(self, goal_sum):
        #골보내는 함수
        wait_count = 1
        while not self.arithmetic_action_client.wait_for_server(timeout_sec=0.1):
            if wait_count > 3:
                self.get_logger().warning('Arithmetic action server is not available.')
                return False
            wait_count += 1
        goal_msg = ArithmeticChecker.Goal()
        #골 float 형
        goal_msg.goal_sum = (float)(goal_sum)
        self.send_goal_future = self.arithmetic_action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.get_arithmetic_action_feedback)
        #멀티스레드 골에 대한 멀티 스레드
        self.send_goal_future.add_done_callback(self.get_arithmetic_action_goal)
        return True

    def get_arithmetic_action_goal(self, future):
        goal_handle = future.result()
        #result에 대한 스레드 
        if not goal_handle.accepted:
            self.get_logger().warning('Action goal rejected.')
            return
        self.get_logger().info('Action goal accepted.')
        self.action_result_future = goal_handle.get_result_async()
        #리설트에 대한 스레드
        self.action_result_future.add_done_callback(self.get_arithmetic_action_result)

    def get_arithmetic_action_feedback(self, feedback_msg):
        action_feedback = feedback_msg.feedback.formula
        #string list
        self.get_logger().info('Action feedback: {0}'.format(action_feedback))

    def get_arithmetic_action_result(self, future):
        action_status = future.result().status
        action_result = future.result().result
        #
        if action_status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Action succeeded!')
            self.get_logger().info(
                'Action result(all formula): {0}'.format(action_result.all_formula))
            self.get_logger().info(
                'Action result(total sum): {0}'.format(action_result.total_sum))
        else:
            self.get_logger().warning(
                'Action failed with status: {0}'.format(action_status))
