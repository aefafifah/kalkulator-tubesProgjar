import asyncio
import websockets
import sympy as sp
import math

clients = set()

async def handle_client(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")

            # Split data to get the menu choice and the expression
            menu_choice, expression = message.split(":")
            menu_choice = int(menu_choice)

            # Calculate the result based on the menu choice
            if menu_choice == 1:
                result = calculate_derivative(expression, 1)
            elif menu_choice == 2:
                result = calculate_integral(expression, 1)
            elif menu_choice == 3:
                result = calculate_trigonometric(expression)
            elif menu_choice == 4:
                result = calculate_basic_math(expression)
            elif menu_choice == 5:
                result = calculate_derivative(expression, 2)
            elif menu_choice == 6:
                result = calculate_derivative(expression, 3)
            elif menu_choice == 7:
                result = calculate_derivative(expression, 4)
            elif menu_choice == 8:
                result = calculate_integral(expression, 2)
            elif menu_choice == 9:
                result = calculate_integral(expression, 3)
            elif menu_choice == 10:
                result = calculate_integral(expression, 4)
            else:
                result = "Invalid menu choice"

            # Send the calculation result to all connected clients
            await broadcast(f"Hasil dari {expression}: {result}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        clients.remove(websocket)

def calculate_derivative(expression, order):
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression)
        derivative = sp.diff(expr, x, order)
        return str(derivative)
    except Exception as e:
        return f"Error: {e}"

def calculate_integral(expression, order):
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression)
        integral = expr
        for _ in range(order):
            integral = sp.integrate(integral, x)
        return str(integral)
    except Exception as e:
        return f"Error: {e}"

def calculate_trigonometric(expression):
    try:
        trig_function, angle = expression.split(",")
        angle = float(angle)
        result = trigonometric_function(trig_function, angle)
        return str(result)
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
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

async def broadcast(message):
    if clients:
        await asyncio.gather(*(client.send(message) for client in clients))

start_server = websockets.serve(handle_client, "127.0.0.1", 5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()