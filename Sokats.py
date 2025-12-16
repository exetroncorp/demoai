import asyncio
import websockets

async def hello(websocket):
    # This runs when a client connects
    print("Client connected!") 
    name = await websocket.recv() # Wait for client to send something
    print(f"Server received: {name}")
    
    greeting = f"Hello {name}, from Debian 12!"
    await websocket.send(greeting) # Send response back
    print(f"Server sent: {greeting}")

async def main():
    # Bind to 0.0.0.0 so the container accepts outside connections
    async with websockets.serve(hello, "0.0.0.0", 8765):
        print("WebSocket Server started on port 8765...")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
