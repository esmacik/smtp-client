# Erik Macik
# Computer Networks Assignment 1
# SMTP Server communication

from socket import *


# Constant SMTP commands used when creating messages for SMTP server
HELO = "helo "
MAIL_FROM = "mail from: "
RCPT_TO = "rcpt to: "
DATA = "data"
SUBJECT = "subject: "
BODY = ""
RETURN = "\r\n"

# Receive a message from the server represented y `client_socket`
def receive_and_print(client_socket):
    response = client_socket.recv(1024)
    print('From server:', response.decode())

# Send a message to the server represented by `client_socket`
# The message will have a prefix of `command` to identify command
# The message will have contents of `argument`
def send_message(client_socket, command, argument):
    to_send = command + argument + RETURN
    if command == SUBJECT:
        to_send += RETURN
    elif command == BODY:
        to_send += RETURN+"."+RETURN
    client_socket.send(to_send.encode())

# Main function. Read SMTP Server address and port number from user, and connect 
# to server.
# The user is walked through the SMTP conversation process where they are asked
# for input, it is automatically sent to the server in the correct format,
# and the response from the server is shown to the user.
# #
if __name__ == "__main__":
    print("SMTP Mail Server automation")

    # Get SMTP server and port from user
    server_name = input("Enter SMTP mail server address: ")
    server_port = int(input("Enter port numer: "))

    # Initiate TCP connection with server
    client_socket = socket(AF_INET, SOCK_STREAM) # TCP connection

    try:
        # Try to connect
        print("Connecting to mail server...")
        client_socket.connect((server_name, server_port))
        print("Connected to", server_name, "at port", server_port)
    except Exception as e:
        # Quit if the connection fails
        print("Couldn't connect to server")
        exit()

    # Display successful connection response
    receive_and_print(client_socket)

    # Read and communicate domain name with helo command
    domain_name = input("Enter the domain name: ")
    send_message(client_socket, HELO, domain_name)
    receive_and_print(client_socket)

    # Read and communicate source email
    source_email = input("Enter your email address: ")
    send_message(client_socket, MAIL_FROM, source_email)
    receive_and_print(client_socket)

    # Read and communicate receiving email
    dest_email = input("Enter the receiving email address: ")
    send_message(client_socket, RCPT_TO, dest_email)
    receive_and_print(client_socket)

    # Initiate start of email contents with server
    send_message(client_socket, DATA, "")
    receive_and_print(client_socket)

    # Read email subject and body from user
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")

    # Communicate email subject and body
    send_message(client_socket, SUBJECT, subject)
    send_message(client_socket, BODY, body)

    # Display successful message queued
    receive_and_print(client_socket)

    # Close connection
    client_socket.close()