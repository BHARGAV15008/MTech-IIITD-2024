from queue import Queue
from threading import Thread
from src.HMAC.HMAC_Core import HMACClient
from src.SeedGeneration.SeedGeneration_Core import SeedGenerator
from colors import Colors  # Import the color configuration

DEBUG = True


def print_msg(who: str, message: str, color: str = Colors.RESET) -> None:
    """
    Function to print debug messages. Prints the message only if the DEBUG flag is set to True.

    Args:
        who (str): Identifier of the message sender.
        message (str): Message to print.
        color (str): Color code for the message.
    """
    if DEBUG:
        print(f"{color}[{who}] {message}{Colors.RESET}\n")


def client(client_socket: Queue, server_socket: Queue):
    main_seed = SeedGenerator(phrase="job").generate()
    obj = HMACClient(algorithm="sha256", secret=main_seed, symbol_count=1)

    server_socket.put(main_seed)

    if client_socket.get() == obj.encrypt_message(''):
        message = input(f"{Colors.YELLOW}Enter a message: {Colors.RESET}")
        server_socket.put(obj.encrypt_message_by_chunks(message))
        print_msg('client', f'client sent message {message}', Colors.YELLOW)

        if client_socket.get() == obj.encrypt_message(message):
            print_msg('client', f'server has decrypt message: {message}', Colors.GREEN)


def server(server_socket: Queue, client_socket: Queue):
    main_seed = server_socket.get()
    obj = HMACClient(algorithm="sha256", secret=main_seed, symbol_count=1)

    client_socket.put(obj.encrypt_message(''))

    msg = server_socket.get()
    print_msg('server', f'msg encrypted {msg}', Colors.YELLOW)

    try:
        msg_raw = obj.decrypt_message_by_chunks(msg)
        print_msg('server', f'msg raw {msg_raw}', Colors.GREEN)
        client_socket.put(obj.encrypt_message(msg_raw))
    except Exception as e:
        print_msg('server', f"Error decrypting message: {e}", Colors.RED)


def main():
    client_socket, server_socket = Queue(), Queue()
    threads = [
        Thread(target=client, args=(client_socket, server_socket)),
        Thread(target=server, args=(server_socket, client_socket))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
