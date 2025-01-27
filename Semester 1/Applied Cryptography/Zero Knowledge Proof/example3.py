from src.ZeroKnowledge.ZeroKnowledge_Core import ZeroKnowledge
from src.ZeroKnowledge.ZeroKnowledge_Models import ZeroKnowledgeSignature, ZeroKnowledgeData
from queue import Queue
from threading import Thread
from src.HMAC.HMAC_Core import HMACClient
from src.SeedGeneration.SeedGeneration_Core import SeedGenerator
from colors import Colors  # Import the color configuration
import json

DEBUG = True


def colorize_json(json_data):
    """
    Colorizes the JSON output by applying different colors to keys and values.
    
    Args:
        json_data (dict): The JSON data to colorize.
        
    Returns:
        str: The colorized JSON string.
    """
    key_color = Colors.CYAN  # Color for keys
    value_color = Colors.MAGENTA  # Color for values
    reset_color = Colors.RESET  # Reset color

    colorized_output = []
    for key, value in json_data.items():
        if isinstance(value, dict):
            value = colorize_json(value)  # Recursively colorize nested JSON
        colorized_output.append(f"{key_color}\"{key}\"{reset_color}: {value_color}{value}{reset_color}")
    
    return "{\n  " + ",\n  ".join(colorized_output) + "\n}"


def print_msg(who: str, message: str, color: str = Colors.RESET) -> None:
    if DEBUG:
        print(f"{color}[{who}] {message}{Colors.RESET}\n")


def client(client_socket: Queue, server_socket: Queue):
    client_object = ZeroKnowledge.new(curve_name="secp256k1", hash_alg="sha3_256")
    main_seed = SeedGenerator(phrase="job").generate()
    identity = 'Encryptors'
    signature = client_object.create_signature(identity)

    server_socket.put(signature.to_json())
    print_msg('client', f'its signature {colorize_json(json.loads(signature.to_json()))}', Colors.YELLOW)

    token = client_socket.get()
    print_msg('client', f'its token {colorize_json(json.loads(token))}', Colors.YELLOW)

    proof = client_object.sign(identity, token).to_json()
    print_msg('client', f'proof {colorize_json(json.loads(proof))}', Colors.YELLOW)

    server_socket.put(proof)
    result = client_socket.get()
    print_msg('client', f"{result}", Colors.GREEN if result else Colors.RED)

    if result:
        server_socket.put(main_seed)
        obj = HMACClient(algorithm="sha256", secret=main_seed, symbol_count=1)

        if client_socket.get() == obj.encrypt_message(''):
            message = input(f"{Colors.YELLOW}Enter a message: {Colors.RESET}")
            if message:  # Check if the message is not empty
                server_socket.put(obj.encrypt_message_by_chunks(message))
                print_msg('client', f'client sent message {message}', Colors.YELLOW)
            else:
                print_msg('client', "No message entered to send.", Colors.RED)

            if client_socket.get() == obj.encrypt_message(message):
                print_msg('client', f'server has decrypted message: {message}', Colors.GREEN)


def server(server_socket: Queue, client_socket: Queue):
    server_password = "GeniusFactor"
    server_zk = ZeroKnowledge.new(curve_name="secp384r1", hash_alg="sha3_512")
    server_signature: ZeroKnowledgeSignature = server_zk.create_signature(server_password)

    sig = server_socket.get()
    client_signature = ZeroKnowledgeSignature.from_json(sig)
    print_msg('server', f'its client signature {colorize_json(json.loads(client_signature.to_json()))}', Colors.YELLOW)

    client_zk = ZeroKnowledge(client_signature.params)
    print_msg('server', f'its client_zk {client_zk}', Colors.YELLOW)

    token = server_zk.sign(server_password, client_zk.token())
    print_msg('server', f'its token {colorize_json(json.loads(token.to_json()))}', Colors.YELLOW)
    client_socket.put(token.to_json())

    proof = ZeroKnowledgeData.from_json(server_socket.get())
    print_msg('server', f'its proof {colorize_json(json.loads(proof.to_json()))}', Colors.YELLOW)

    token = ZeroKnowledgeData.from_json(proof.data)
    server_verif = server_zk.verify(token, server_signature)
    print_msg('server', f'its server_verif {server_verif}', Colors.GREEN if server_verif else Colors.RED)

    if not server_verif:
        client_socket.put(False)
    else:
        client_verif = client_zk.verify(proof, client_signature, data=token)
        print_msg('server', f'its client_verif {client_verif}', Colors.GREEN if client_verif else Colors.RED)

        client_socket.put(client_verif)

        main_seed = server_socket.get()
        obj = HMACClient(algorithm="sha256", secret=main_seed, symbol_count=1)

        client_socket.put(obj.encrypt_message(''))

        msg = server_socket.get()
        if msg:  # Check if msg is not empty
            print_msg('server', f'msg encrypted: {msg}', Colors.YELLOW)
            try:
                msg_raw = obj.decrypt_message_by_chunks(msg)
                print_msg('server', f'msg raw {msg_raw}', Colors.GREEN)
                client_socket.put(obj.encrypt_message(msg_raw))
            except Exception as e:
                print_msg('server', f"Error decrypting message: {e}", Colors.RED)
        else:
            print_msg('server', "Received an empty message from the client.", Colors.RED)


if __name__ == "__main__":
    server_queue = Queue()
    client_queue = Queue()

    server_thread = Thread(target=server, args=(server_queue, client_queue))
    client_thread = Thread(target=client, args=(client_queue, server_queue))

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()