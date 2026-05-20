import rclpy
from rclpy.node import Node
from llm_interface.srv import GeminiQuery
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup # 1. 추가
from google import genai

class GeminiServiceNode(Node):

    def __init__(self):
        super().__init__('llm_sample')
        # ReentrantCallbackGroup 설정 (병렬 처리 허용)
        self.callback_group = ReentrantCallbackGroup() # 2. 추가
        
        self.api_key = ''
        self.client = genai.Client(api_key=self.api_key)
        #self.model = genai.GenerativeModel('gemini-2.0-flash') 
        # 서비스 생성 시 callback_group 지정
        self.srv = self.create_service(
            GeminiQuery, 
            'gemini_response', 
            self.callback,
            callback_group=self.callback_group # 3. 중요!
        )
        self.get_logger().info('Gemini Service Node Started')

    def callback(self, request, response):
        self.get_logger().info('--- 서비스 요청 수신 ---')
        
        
        try:
            self.get_logger().info('제미나이 API 호출 중...')
            
            res = self.client.models.generate_content(model = 'gemini-2.0-flash', contents = request.prompt)
            response.success = True
            response.response = res.text
            if res.text:
                self.get_logger().info(f"답변: {res.text}")
            self.get_logger().info('답변 수신 및 전송 완료!')
            
        except Exception as e:
            self.get_logger().error(f'서비스 처리 중 오류 발생: {e}')
            response.success = False
            response.response = f"에러 발생: {str(e)}"
            
        return response.response

def main(args=None):
    rclpy.init(args=args)
    node = GeminiServiceNode()
    
    # 멀티스레드 실행기 적용
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