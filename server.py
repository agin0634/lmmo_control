import asyncio
import websockets
import json

connected_clients = {}

async def handle_client(websocket, path):
    client_id = websocket.remote_address[0] + ":" + str(websocket.remote_address[1])
    connected_clients[client_id] = websocket
    print(f"Client connected: {client_id}")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            parts = message.split(" ", 1)
            if len(parts) == 2:
                client_ip = parts[0]
                command_to_execute = parts[1]
                target_websocket = connected_clients.get(client_ip)
                if target_websocket:
                    print(f"Sending command to client: {client_ip}")
                    await target_websocket.send(json.dumps({"action": "execute", "command": command_to_execute}))
                else:
                    print(f"Client {client_ip} not found.")
            else:
                print("Invalid command format. Use 'client_ip command'.")
    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection closed for {client_id}")
    finally:
        del connected_clients[client_id]

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("WebSocket server started at localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
