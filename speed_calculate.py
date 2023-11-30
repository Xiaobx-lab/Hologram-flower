import serial
import time
import paho.mqtt.client as mqtt




if __name__ == "__main__":

    ser = serial.Serial('COM3', 9600, timeout=1)  # 根据实际情况修改串口号和波特率
    client = mqtt.Client()
    client.connect("localhost",1883,60)
    client.loop_start()
    moves = []

    while True:
        data = ser.readline().decode().strip()
        cutoff = time.time() - 1
        moves = [x for x in moves if x > cutoff]
        print("Moves in the last second", len(moves))

        if len(moves) == 10:
            client.publish("speed", "1")

        if len(moves) == 20:
            client.publish("speed", "1.5")

        if len(moves) == 40:
            client.publish("speed", "2")

        if data:
            print('data', data)
            pos = int(data)
            moves.append(time.time())
