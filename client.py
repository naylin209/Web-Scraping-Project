""" NSSA 220 Final Group: Nay Lin Aung & Ayesha Khan"""

import socket
import xml.etree.ElementTree as ET
import sys

def read_query(file_path):
    """Read the XML query from a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Query file '{file_path}' not found.")
        return ""

def send_query(query, server_host, server_port):
    """Send query to the server and receive a response."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        print("Sending a query...")
        
        # Send the query to the server
        client_socket.sendall(query.encode())
        
        # Receive the response length
        response_length = client_socket.recv(1024).decode().strip()
        if not response_length.isdigit():
            raise ValueError("Invalid response length received from the server.")
        
        response_length = int(response_length)
        print(f"Expected response size: {response_length} bytes.")
        
        # Receive the full response in chunks
        response = b""
        while len(response) < response_length:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            response += chunk
        
        client_socket.close()
        print("Receiving a response...")
        return response.decode()
    except ConnectionError as e:
        print(f"Error connecting to server: {e}")
        return "<result><status>Failure</status></result>"
    except Exception as e:
        print(f"Error during query transmission: {e}")
        return "<result><status>Failure</status></result>"

def save_response(response, file_path):
    """Save the server response to an XML file."""
    try:
        with open(file_path, 'w') as file:
            file.write(response)
    except Exception as e:
        print(f"Error saving response to file '{file_path}': {e}")

def display_response(response):
    """Parse and display the server response in the terminal."""
    try:
        root = ET.fromstring(response)
        status = root.find("status").text
        print(f"Query {status}!")
        
        if status == "Success":
            print("Received Data:")
            print("#" * 25)
            for row in root.find("data").findall("row"):
                name = row.find("name").text
                title = row.find("title").text
                email = row.find("email").text
                print(f"Name: {name}\nTitle: {title}\nEmail: {email}")
                print("#" * 25)
    except ET.ParseError as e:
        print(f"Error parsing response XML: {e}")
    except Exception as e:
        print(f"Error displaying response: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <query_file> <response_file>")
        sys.exit(1)
    
    query_file = sys.argv[1]
    response_file = sys.argv[2]
    server_host = "localhost"
    server_port = 8080
    
    # Read the query, send it to the server, and handle the response
    query = read_query(query_file)
    if query:
        response = send_query(query, server_host, server_port)
        save_response(response, response_file)
        print("Response saved!")
        display_response(response)
