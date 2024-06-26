"""Server script for the chat application."""

import asyncio

from utils import print_color, color_text
from config import HOST, PORT


clients = dict()


async def send_all(message, writer, exclude_self=False):
    for other_writer in clients.keys():
        try:
            if other_writer == writer:
                if exclude_self:
                    continue

                else:
                    sender = "You"

            else:
                sender = clients[writer]

            other_writer.write(message.format(sender).encode())
            await other_writer.drain()

        except Exception as e:
            print_color("red", f"Error sending to client {other_writer.get_extra_info('peername')}: {e}")
            clients.pop(other_writer)


async def handle_client(reader, writer):
    client_addr = writer.get_extra_info('peername')[1]
    
    welcome_message = f"\033[38;5;121m\n<<< Welcome to the server! >>>\033[0m\n\nConnected clients: {list(clients.values())}\n".encode()
    writer.write(welcome_message)
    await writer.drain()
    
    clients[writer] = f"Client{len(clients) + 1}"
    joined = color_text("green", f"*** {clients[writer]} joined the server.")
    
    print(joined, f"(PORT: {client_addr})")
    await send_all(joined, writer, exclude_self=True)

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                left = color_text("red", "*** {0} left the server.")
                print(left.format(clients[writer]), f"(PORT: {client_addr})")
                
                await send_all(left, writer)
                break

            message = "<{0}> " + data.decode()
            print(message.format(clients[writer]))

            await send_all(message, writer)
            await asyncio.sleep(0.1)


    finally:
        clients.pop(writer)
        writer.close()


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print_color("cyan", f"Server started at {HOST}:{PORT}\n")

    async with server:
        while True:
            await asyncio.sleep(0.1) # Tick


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print_color("red", "Server shutting down...\n")
