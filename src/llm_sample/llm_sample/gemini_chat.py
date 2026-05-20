import rclpy
from rclpy.node import Node
from llm_interface.srv import GeminiQuery
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from google import genai
from google.genai import types # 메시지 타입 정의를 위해 추가

class GeminiServiceNode(Node):

    def __init__(self):
        super().__init__('llm_sample')
        self.callback_group = ReentrantCallbackGroup()
        
        # API 설정
        self.api_key = ''
        self.client = genai.Client(api_key=self.api_key)
        
        # 1. 대화 내역을 저장할 리스트 초기화
        self.history = []
        
        # (선택 사항) 시스템 지침: 챗봇의 성격 정의
        self.system_instruction = "너는 ROS 2 로봇의 인공지능 비서야. 친절하고 간결하게 답변해줘."

        self.srv = self.create_service(
            GeminiQuery, 
            'gemini_response', 
            self.callback,
            callback_group=self.callback_group
        )
        self.get_logger().info('Gemini Chatbot Service Node Started')

    def callback(self, request, response):
        self.get_logger().info(f'--- 요청 수신: {request.prompt} ---')
        
        try:
            # 2. 현재 요청을 히스토리에 추가
            # google-genai SDK는 role과 parts 구조를 가집니다.
            user_message = types.Content(role="user", parts=[types.Part.from_text(text=request.prompt)])
            self.history.append(user_message)

            self.get_logger().info('제미나이 API 호출 중 (문맥 포함)...')
            
            # 3. 전체 히스토리를 contents 파라미터로 전달
            res = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=self.history, # 단일 prompt 대신 전체 history 전달
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction, # 시스템 지침 추가
                    max_output_tokens=500,
                )
            )
            
            # 4. 모델의 답변을 히스토리에 추가 (다음에 기억하기 위함)
            model_text = res.text
            model_message = types.Content(role="model", parts=[types.Part.from_text(text=model_text)])
            self.history.append(model_message)

            # 5. 응답 설정
            response.success = True
            response.response = model_text
            
            # 6. 대화 내역이 너무 길어지면 토큰 절약을 위해 오래된 내역 삭제 (최근 10턴 유지)
            if len(self.history) > 20: # 질문+답변 합쳐서 20개
                self.history = self.history[-20:]

            self.get_logger().info(f"답변 전송 완료: {model_text[:30]}...")
            
        except Exception as e:
            self.get_logger().error(f'서비스 처리 중 오류 발생: {e}')
            response.success = False
            response.response = f"에러 발생: {str(e)}"
            
        # [중요 수정] 리턴값은 response.response가 아니라 response 객체 전체여야 합니다.
        return response

def main(args=None):
    rclpy.init(args=args)
    node = GeminiServiceNode()
    
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