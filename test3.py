# 读取arduino串口数据并保存
import serial
import pandas as pd

# sets up serial connection (make sure baud rate is correct - matches Arduino)
# 设置串口号和波特率和Arduino匹配
ser = serial.Serial('com3', 9600)
# a为储存数据的列表
a = []
# count为次数，采集多少次就停止
count = 0
while count != 30:  # 30可以根据需要设置，while(True)：代表一直读下去
    # reads until it gets a carriage return. MAKE SURE THERE IS A CARRIAGE RETURN OR IT READS FOREVER
    data = ser.readline()  # 按行读取串口数据进来
    data = data.decode()  # 读进来的数据是bytes形式，需要转化为字符串格式
    data = data[13:30]  # 数据格式是'Orientation: 180.87 2.16 -3.86\r\n'，取第13到29为字符出来就是-->'180.87 2.16 -3.86'
    data = data.split(" ")  # 以空格为分隔符分隔字符串-->['180.87', '2.16', '-3.86']
    count += 1
    data = list(map(float, data))  # 把字符串转化为数字-->[180.87, 2.16, -3.86]
    print(data)
    a.append(data)  # 添加到列表里

df = pd.DataFrame(a)  # 转化为df格式数据
# print(df)
df.to_excel('test.xls', header=False, index=False)

