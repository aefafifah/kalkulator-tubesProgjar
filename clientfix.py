import socket
import threading
import math

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except Exception as e:
            print(f"[ERROR] {e}")
            break

def calculate_trigonometric(trig_function, angle):
    try:
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
    except Exception as e:
        return f"Error: {e}"

def menu_choice(client_socket):
    while True:
        print("\nMenu:")
        print("1. Turunan 4 Tingkat")
        print("2. Integral 4 Tingkat")
        print("3. Fungsi Trigonometri (sin, cos, tan, cot, sec, cosec)")
        print("4. Operasi Matematika Dasar (tambah, kurang, kali, bagi)")
        print("5. Keluar")

        choice = input("Pilih opsi (1/2/3/4/5): ")

        if choice == '5':
            client_socket.close()
            break

        if choice not in ['1', '2', '3', '4']:
            print("Pilihan tidak valid.")
            continue

        if choice == '3':
            trig_function = input("Masukkan fungsi trigonometri (sin, cos, tan, cot, sec, cosec): ").lower()
            angle = float(input("Masukkan sudut dalam derajat: "))
            result = calculate_trigonometric(trig_function, angle)
            message = f"{trig_function}({angle}) = {result}"
            print(message)
            client_socket.send(f"3:{trig_function},{angle}".encode("utf-8"))
        else:
            expression = input("Masukkan ekspresi matematika: ")
            client_socket.send(f"{choice}:{expression}".encode("utf-8"))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("0.tcp.ap.ngrok.io", 14326))
client.connect(("127.0.0.1", 5555))


receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

menu_choice(client)
