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

import rclpy #로스 모듈 들어감
from rclpy.executors import MultiThreadedExecutor
#ros에서 지원해주는 멀티 스레드 모듈

from ex_calculator.calculator.calculator import Calculator
#같은 폴더에 있는 cal .py에 있는 Calculator 클래스 주입


def main(args=None):
    rclpy.init(args=args)
    try:
        calculator = Calculator() #클래스 들어감
        executor = MultiThreadedExecutor(num_threads=4)
        #스레드 4개
        executor.add_node(calculator)
        try:
            executor.spin()
        except KeyboardInterrupt:
            calculator.get_logger().info('Keyboard Interrupt (SIGINT)')
        finally:
            executor.shutdown()
            calculator.arithmetic_action_server.destroy()
            calculator.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
