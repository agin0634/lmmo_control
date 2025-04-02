import asyncio
import websockets
import json
import subprocess

async def connect_to_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to server")
        try:
            async for message in websocket:
                data = json.loads(message)
                action = data.get("action")
                command = data.get("command")

                if action == "execute" and command:
                    print(f"Executing command: {command}")
                    try:
                        if command.startswith("start "):
                            executable_path = command[6:]
                            process = subprocess.Popen([executable_path])
                        else:
                            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            stdout, stderr = process.communicate()
                            if stdout:
                                print(f"Command output: {stdout.decode()}")
                            if stderr:
                                print(f"Command error: {stderr.decode()}")
                    except Exception as e:
                        print(f"Error executing command: {e}")
                else:
                    print(f"Received message: {message}")
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed by server")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(connect_to_server())
