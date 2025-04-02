import asyncio
import websockets
import json

async def control_panel():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to server. Enter commands in the format 'client_ip command':")
        try:
            while True:
                command = input()
                if command:
                    await websocket.send(command)
                    response = await websocket.recv()
                    print(f"Received: {response}")
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed by server")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(control_panel())
