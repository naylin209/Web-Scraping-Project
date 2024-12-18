""" NSSA 220 Final Group: Nay Lin Aung & Ayesha Khan"""

import socket
import csv#-
import pandas as pd#+
import xml.etree.ElementTree as ET

def parse_query(query):#-
    """Parse the query XML and extract filtering conditions."""#-
    try:#-
        conditions = []#-
        root = ET.fromstring(query)#-
        for condition in root.findall("condition"):#-
            column = condition.find("column").text.strip()#-
            value = condition.find("value").text.strip()#-
            conditions.append((column, value))#-
        return conditions#-
    except ET.ParseError as e:#-
        print(f"Error parsing query XML: {e}")#-
        return []#-
# The parse_query function remains unchanged#+

def filter_data(conditions, csv_file):
    """Filter the CSV data based on query conditions."""#-
    result_rows = []#-
    """Filter the CSV data based on query conditions using pandas."""#+
    try:
        df = pd.read_csv(csv_file)#+
        for column, value in conditions:#+
            df = df[df[column].str.contains(value, case=False, na=False)]#+
        # Convert the filtered DataFrame back to a list of dictionaries#+
        result_rows = df.to_dict('records')#+

        # Debug: Print the filtered rows#+
        print(f"Filtered rows: {result_rows}")#+

        return result_rows#+
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return []#+
    except KeyError as e:
        print(f"Error: Column '{e}' not found in CSV file.")
    return result_rows#-

"""Generate the XML response based on filtered data."""#-
def generate_response(data):#-
    try:#-
        root = ET.Element("result")#-
        status = ET.SubElement(root, "status")#-
        status.text = "Success" if data else "Failure"#-
#-
        data_elem = ET.SubElement(root, "data")#-
        for row in data:#-
            row_elem = ET.SubElement(data_elem, "row")#-
            for key, value in row.items():#-
                elem = ET.SubElement(row_elem, key.lower())#-
                elem.text = value#-
#-
        return ET.tostring(root).decode()#-
        return []#+
    except Exception as e:
        print(f"Error generating response XML: {e}")#-
        return "<result><status>Failure</status></result>"#-
        print(f"Error filtering data: {e}")#+
        return []#+

"""Start the server and handle incoming client connections."""#-
def start_server(host, port, csv_file):#-
    try:#-
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#-
        server_socket.bind((host, port))#-
        server_socket.listen(5)#-
        print("Server is running...")#-
# The generate_response function remains unchanged#+

        while True:#-
            client_socket, addr = server_socket.accept()#-
            print(f"Connected to {addr}")#-
# The start_server function remains unchanged#+

            try:#-
                query = client_socket.recv(1024).decode()#-
#-
                if not query:#-
                    raise ValueError("Received empty query.")#-
                print("Received query from client.")#-
#-
                # Parse query, filter data, and generate response#-
                conditions = parse_query(query)#-
                data = filter_data(conditions, csv_file)#-
                response = generate_response(data)#-
#-
                # Send the response length first#-
                response_bytes = response.encode()#-
                response_length = str(len(response_bytes)).encode()#-
                client_socket.sendall(response_length + b'\n')  # Send length with newline#-
#-
                # Send the actual response#-
                client_socket.sendall(response_bytes)#-
            except Exception as e:#-
                print(f"Error handling client request: {e}")#-
                client_socket.sendall(b"0\n")  # Send failure length#-
            finally:#-
                client_socket.close()#-
    except Exception as e:#-
        print(f"Error starting server: {e}")#-
    finally:#-
        server_socket.close()#-
        print("Server stopped.")#-
if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5000 
    CSV_FILE = "directory.csv"
    start_server(HOST, PORT, CSV_FILE)
