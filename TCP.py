#from socket import *
import socket
import serial
import time
import re


#串口发送类，将数据通过串口发送至单片机
class MySerial:
    def __init__(self):
        try:
            self.ser = serial.Serial(port="/dev/ttyAMA1", baudrate=9600)
            if self.ser.isOpen == False:
                self.ser.open()
        except KeyboardInterrupt:
            if self.ser != None:
                self.ser.close()

    def SerialSendData(self,str): #G前进  S停止 L左转 R右转 B倒车
        str += '\n'
        strData = str.encode("gbk")
        self.ser.write(strData)
        #print(self.ser.read(6))
        #time.sleep(1)

#TCP连接， 接收TCP消息
class MyTCPClient:
    def __init__(self,ip,port=8888):
        ADDRESS = (ip, port)
        self.BUFSIZ = 1024
        self.tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpClientSocket.connect(ADDRESS)

    def TCPreceiveData(self):
        data, ADDR = self.tcpClientSocket.recvfrom(self.BUFSIZ)
        if not data:
            print('error')
        #print("服务器端响应：", data.decode('utf-8'))
        return data.decode('utf-8')


#坐标数据类
class LocationStruct:
    # def __init__(self,name,x,y,z,updateflag = False):
    def __init__(self,name,x,y,z):
        self.name = name
        self.x = x
        self.y =y
        self.z = z
        #self.updateflag = updateflag
    
    def printSelfData(self):
        print('name:%s, X:%d, Y:%d, Z:%d' %(self.name,self.x, self.y ,self.z))

#对数据进行处理
class MyDataProcess:
    def __init__(self):
        self = self

    def GetTargetLocation(x, y, z):
        print('111')

    def UpdateLocation(self, Recvdata, CarLoca, TargetLoca):
        if Recvdata.find('Target:') != -1: #判断是否是发送目标坐标
            print('found Target')
            x = re.findall(r"\d+\.?\d*",Recvdata)
            print(x)
            #更新XYZ坐标
            if TargetLoca.name == 'Target':
                TargetLoca.x = x[0]
                TargetLoca.y = x[1]
                TargetLoca.z = x[2]
                #TargetLoca.updateflag = True
                TargetLoca.printSelfData()
            #GetTargetLocation(x[0], x[1], x[2])
            return True
        if Recvdata.find('Car:') != -1:
            print('found carLoca')
            x = re.findall(r"\d+\.?\d*",Recvdata)
            print(x)
            #更新XYZ坐标
            if CarLoca.name == 'car':
                CarLoca.x = x[0]
                CarLoca.y = x[1]
                CarLoca.z = x[2]
                #CarLoca.updateflag = True
                CarLoca.printSelfData()
            #GetTargetLocation(x[0], x[1], x[2])
            return False
    
    def CheakIfReach(self, CarLoca, TargetLoca, precision = 0.01): #判断是否到达Targe
        if abs(CarLoca.x - TargetLoca.x) > precision
            return False
        if abs(CarLoca.y - TargetLoca.y) > precision
            return False
        return True
    
    def JudgeDirection(self, CarLoca, TargetLoca):
        


def main():
    Ser = MySerial()
    TCPC = MyTCPClient('192.168.8.249')
    CarLocation = LocationStruct('car', 0.0, 0.0, 0.0)
    TargetLocation = LocationStruct('Target', 0.0, 0.0, 0.0)
    reachFlag = True
    i = 100
    while True:
        i += 1
        reciveData = TCPC.TCPreceiveData()
        if MyDataProcess.UpdateLocation(reciveData, CarLocation, TargetLocation) == True: #返回TRUE 代表 Target改变
            reachFlag = False  #已更新Target,需再次判断是否到达

        if MyDataProcess.CheakIfReach(CarLocation, TargetLocation) == True:     #已到达Target
            Ser.SerialSendData('AS')
            reachFlag = True

        if reachFlag == False:          #未到达Target
            Ser.SerialSendData(str(i) + reciveData)

if __name__ == '__main__':
    main()
