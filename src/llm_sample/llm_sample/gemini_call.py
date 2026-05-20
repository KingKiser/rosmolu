import rclpy
from rclpy.node import Node
from llm_interface.srv import GeminiQuery
from turtlesim.srv import TeleportRelative
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup #멀티 스레드 
import json
import re
from google import genai
from google.genai import types

class GeminiTurtlesimNode(Node):
    def __init__(self):
        super().__init__('gemini_call') # 노드 이름을 실행 로그와 맞춤
        self.callback_group = ReentrantCallbackGroup()
        
        default_script = (
            "너는 ROS 2 터틀심 로봇 제어기야. 사용자의 자연어 명령을 분석해서 "
            "이동 거리(linear)와 회전 각도(angular)를 결정해줘. "
            "반드시 다음 JSON 형식으로만 대답해. 다른 말은 절대 하지마: "
            "{\"linear\": float, \"angular\": float}"
        )
        self.declare_parameter('system_script', default_script)
        self.system_instruction = self.get_parameter('system_script').value


        # 1. Gemini 클라이언트 설정
        self.api_key = '' # 실제 키를 입력하세요
        self.client = genai.Client(api_key=self.api_key)
        self.history = [] #대화 내역 저장

        # 2. 터틀심 서비스 클라이언트 생성
        self.turtle_client = self.create_client(
            TeleportRelative, 
            '/turtle1/teleport_relative',
            callback_group=self.callback_group
        )
        
        # 3. 외부 인터페이스 서비스 서버 생성
        self.srv = self.create_service(
            GeminiQuery, 
            'gemini_response', 
            self.callback,
            callback_group=self.callback_group
        )
        self.get_logger().info('Gemini Turtlesim 제어 노드가 준비되었습니다.')

    async def callback(self, request, response): #멀티 스레드 함수
        self.get_logger().info(f'명령 수신: {request.prompt}')
        
        try:
            # Gemini에게 명령 전달
            user_message = types.Content(role="user", parts=[types.Part.from_text(text=request.prompt)])
            self.history.append(user_message)

            res = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents = self.history,
                config=types.GenerateContentConfig(
                    system_instruction= self.system_instruction,
                    temperature=0.0
                )
            )
            
            # 답변에서 JSON 추출
            raw_text = res.text
            json_str = re.search(r'\{.*\}', raw_text, re.DOTALL).group()
            cmd_data = json.loads(json_str)
            
            linear_v = float(cmd_data.get('linear', 0.0))
            angular_v = float(cmd_data.get('angular', 0.0))

            # 터틀심 서비스 호출 (await 사용하여 대기)
            self.get_logger().info(f'터틀심 이동 실행: linear={linear_v}, angular={angular_v}')
            turtle_req = TeleportRelative.Request()
            turtle_req.linear = linear_v
            turtle_req.angular = angular_v
            
            # 여기서 await를 해야 실제 이동 완료 후 다음 단계로 넘어갑니다.
            await self.turtle_client.call_async(turtle_req)
            
            response.success = True
            response.response = f"성공적으로 이동했습니다: {json_str}"
            
        except Exception as e:
            self.get_logger().error(f'제어 중 오류 발생: {e}')
            response.success = False
            response.response = f"실패: {str(e)}"
            
        return response

def main(args=None):
    rclpy.init(args=args)
    node = GeminiTurtlesimNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()