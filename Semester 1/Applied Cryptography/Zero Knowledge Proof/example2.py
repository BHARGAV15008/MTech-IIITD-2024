from src.ZeroKnowledge import ZeroKnowledge_Algorithms
from src.ZeroKnowledge.ZeroKnowledge_Core import ZeroKnowledge, ZeroKnowledgeSignature, ZeroKnowledgeData
from queue import Queue
from threading import Thread
import json
from colors import Colors

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


def print_message(message, who: str = "System", what: str = None, color: str = None):
    """
    Enhanced function to print messages with JSON handling and color support.
    
    Args:
        message (any): Message to print (can be JSON string, dict, or regular text)
        who (str): Identifier of the message sender
        what (str): Additional context about the message (optional)
        color (str): ANSI color code (optional)
    """
    if not DEBUG:
        return
        
    try:
        # Start the line with sender identifier
        prefix = f"[{who}]"
        if what:
            prefix += f" {what}:"
        
        # Add color if provided
        if color:
            prefix = f"{color}{prefix}"
        
        # Try to parse as JSON
        if isinstance(message, str):
            try:
                json_data = json.loads(message)
                print(f"{prefix} ")
                print(colorize_json(json_data))
            except json.JSONDecodeError:
                print(f"{prefix} ")
                print(f"{message}")
        elif isinstance(message, dict):
            print(f"{prefix} ")
            print(colorize_json(message))
        else:
            print(f"{prefix} ")
            print(f"{message}")
            
        # Reset color if it was used
        if color:
            print(Colors.RESET)
            
    except Exception as e:
        print(f"{prefix} Error printing message: {str(e)}")
        if color:
            print(Colors.RESET)


def client(client_socket: Queue, server_socket: Queue):
    """
    Function representing the client logic.
    """
    # Creating a "Zero-Knowledge" object for the client
    client_object = ZeroKnowledge.new(curve_name="secp256k1", hash_alg="sha3_256")
    identity = 'Encryptors'

    # Creating a signature
    signature = client_object.create_signature(identity)
    print_message(signature.to_json(), "client", "signature", Colors.YELLOW)

    # Send signature to server
    server_socket.put(signature.to_json())

    # Get token from server
    token = client_socket.get()
    print_message(token, "client", "token", Colors.YELLOW)

    # Generate proof
    proof = client_object.sign(identity, token).to_json()
    print_message(proof, "client", "proof", Colors.YELLOW)

    # Send proof to server
    server_socket.put(proof)

    # Get verification result
    result = client_socket.get()
    if result:
        print_message("Verification successful", "client", "result", Colors.GREEN)
    else:
        print_message("Verification failed", "client", "result", Colors.RED)


def server(server_socket: Queue, client_socket: Queue):
    """
    Function representing the server logic.
    """
    # Server password
    server_password = "GeniusFactor"

    # Create server Zero-Knowledge object
    server_zk = ZeroKnowledge.new(curve_name="secp384r1", hash_alg="sha3_512")
    server_signature = server_zk.create_signature(server_password)

    # Get client signature
    sig = server_socket.get()
    client_signature = ZeroKnowledgeSignature.from_json(sig)
    print_message(client_signature.to_json(), "server", "client signature", Colors.YELLOW)

    # Create client Zero-Knowledge object
    client_zk = ZeroKnowledge(client_signature.params)
    print_message(str(client_zk), "server", "client_zk", Colors.YELLOW)

    # Generate token
    token = server_zk.sign(server_password, client_zk.token())
    print_message(token.to_json(), "server", "token", Colors.YELLOW)

    # Send token to client
    client_socket.put(token.to_json())

    # Get proof from client
    proof = ZeroKnowledgeData.from_json(server_socket.get())
    print_message(proof.to_json(), "server", "proof", Colors.YELLOW)

    # Verify proof
    token = ZeroKnowledgeData.from_json(proof.data)
    print_message(token.to_json(), "server", "verification token", Colors.YELLOW)
    
    # Server verification
    server_verif = server_zk.verify(token, server_signature)
    print_message(f"Server verification result: {server_verif}", "server", "verification", 
                 Colors.GREEN if server_verif else Colors.RED)

    if not server_verif:
        client_socket.put(False)
        return

    # Client verification
    client_verif = client_zk.verify(proof, client_signature, data=token)
    print_message(f"Client verification result: {client_verif}", "server", "verification", 
                 Colors.GREEN if client_verif else Colors.RED)
    client_socket.put(client_verif)


def main():
    """
    Main function to run the client and server threads.
    """
    # Create communication queues
    client_socket, server_socket = Queue(), Queue()
    
    # Create threads
    threads = [
        Thread(target=client, args=(client_socket, server_socket)),
        Thread(target=server, args=(server_socket, client_socket))
    ]

    # Start threads
    for thread in threads:
        thread.start()

    # Wait for threads to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()