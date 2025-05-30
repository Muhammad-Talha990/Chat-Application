import socket
import threading

HOST = '127.0.0.2'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(message, end='')
        except:
            print("Connection to server lost!")
            break
    sock.close()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
        return

    # First, receive the username prompt from the server
    try:
        username_prompt = client.recv(1024).decode('utf-8')
        print(username_prompt, end='') # Print the prompt received from the server
    except Exception as e:
        print(f"Error receiving username prompt: {e}")
        client.close()
        return

    # Get the username from the user input after displaying the server's prompt
    username = input()
    client.send(username.encode('utf-8')) # Send the entered username to the server

    # Now, start the thread to receive all subsequent messages (including join confirmation)
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    # Then enter the main loop for sending chat messages
    try:
        while True:
            message = input()
            if message.lower() == '/quit':
                break
            client.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("\nDisconnecting from server...")
    except Exception as e:
        print(f"An error occurred while sending messages: {e}")
    finally:
        # The receive_messages thread will handle closing the socket on its end
        # if the server disconnects. If the user types '/quit' or uses KeyboardInterrupt,
        # we break the sending loop, and the receive thread will eventually catch
        # the socket closure.
        # It's generally safer to let the receiver handle the final close
        pass # No need to explicitly close client socket here again

if __name__ == "__main__":
    main()
