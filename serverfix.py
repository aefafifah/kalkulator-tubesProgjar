import socket
import threading
import sympy as sp
import math

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break

            print(f"[{client_address}] {data}")

            # Split data to get the menu choice and the expression
            menu_choice, expression = data.split(":")
            menu_choice = int(menu_choice)

            # Calculate the result based on the menu choice
            if menu_choice == 1:
                result = calculate_derivative(expression)
            elif menu_choice == 2:
                result = calculate_integral(expression)
            elif menu_choice == 3:
                result = calculate_trigonometric(expression)
            elif menu_choice == 4:
                result = calculate_basic_math(expression)
            else:
                result = "Invalid menu choice"

            # Send the calculation result to all connected clients
            broadcast(f"Hasil dari {expression}: {result}")

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    print(f"[DISCONNECTED] {client_address}")
    client_socket.close()

def calculate_derivative(expression):
    try:
        x = sp.symbols('x')
        # Convert the mathematical expression into a SymPy expression
        expr = sp.sympify(expression)
        # Calculate the derivative of the expression
        derivative = sp.diff(expr, x)
        return derivative
    except Exception as e:
        return f"Error: {e}"

def calculate_integral(expression):
    try:
        x = sp.symbols('x')
        # Convert the mathematical expression into a SymPy expression
        expr = sp.sympify(expression)
        # Calculate the integral of the expression
        integral = sp.integrate(expr, x)
        return integral
    except Exception as e:
        return f"Error: {e}"

def calculate_trigonometric(expression):
    try:
        # Split the expression to get the trigonometric function and the angle
        trig_function, angle = expression.split(",")
        angle = float(angle)
        # Calculate the trigonometric value
        result = trigonometric_function(trig_function, angle)
        return result
    except Exception as e:
        return f"Error: {e}"

def trigonometric_function(trig_function, angle):
    angle_radians = math.radians(angle)
    if trig_function == 'sin':
        return math.sin(angle_radians)
    elif trig_function == 'cos':
        return math.cos(angle_radians)
    elif trig_function == 'tan':
        return math.tan(angle_radians)
    elif trig_function == 'cot':
        return 1 / math.tan(angle_radians)
    elif trig_function == 'sec':
        return 1 / math.cos(angle_radians)
    elif trig_function == 'cosec':
        return 1 / math.sin(angle_radians)
    else:
        return None

def calculate_basic_math(expression):
    try:
        # Evaluate the basic mathematical expression
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {e}"

def broadcast(message):
    for client_socket in clients:
        client_socket.send(message.encode("utf-8"))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5555))
server.listen(5)
print("[LISTENING] Server is listening for connections...")

clients = []

while True:
    client_socket, client_address = server.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
