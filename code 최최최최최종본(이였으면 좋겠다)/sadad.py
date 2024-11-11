import asyncio
import socketio
import json
import base64

sio = socketio.Client()

@sio.event
async def input(data):
    print(data.image)
    print(data.filter)
    print(data.number)

    with open(r"C:\\Users\\user\Desktop\\Obsidian\\trick-or-picture\background\\image.jpg", "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        await sio.emit('output', base64_image) # {"Image":base64_image}?


def main():
    sio.connect('ws://192.168.1.85:8000/ws');
    sio.wait()

if __name__ == "__main__":
    asyncio.run(main())








async def request_image():
    uri = "ws://192.168.1.85:8000/ws"  # Go 웹소켓 서버의 IP 주소와 포트로 변경

    # 웹소켓 연결
    async with websockets.connect(uri) as websocket:
        with open(r"C:\Users\user\Desktop\Obsidian\trick-or-picture\background\image.jpg", "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            # 요청 데이터 생성
            request_data = {    
                "command": "request",
                "user_number": 0,
                "id": "frame_1",
                "base64Img": "data:image/jpg:base64," + base64_image,
            }

            # JSON 형식으로 직렬화 후 서버로 전송
            await websocket.send(json.dumps(request_data))
            print(f"> 요청 전송: {request_data}")

            # 서버로부터 응답 받기
            response = await websocket.recv()
            print(f"< 서버 응답: {response}")

            response_data = json.loads(response)
            print(response_data)
            return response_data


async def main():
    # 두 함수 호출
    response_data = await request_image()
    print("Response from request_image:", response_data)

# asyncio 이벤트 루프 실행
if __name__ == "__main__":
    asyncio.run(main())
