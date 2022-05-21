# Connecting to Server
import socket
CS = socket.socket()
host = '127.0.0.1'
port = 2004
print('Connecting to Server...')
try:
    CS.connect((host, port))
except socket.error as e:
    print(str(e))    

print("Connected to Server..")
res = CS.recv(1024)
print(res.decode())
# Identifying yourself and sending username
username = input('Username: ')
CS.send(str.encode(username))
res = CS.recv(1024)
print(res.decode('utf-8'))

ans = "0"
while(ans != "5"):
    # Five Requests
    print("Do you want to: ")
    print("1- Arrived Flights Requests.")
    print("2- Delayed Flights Requests.")
    print("3- All flights coming from a specific city.")
    print("4- Details of particular flight.")
    print("5- Quit..")
    ans = input()
    CS.send(str.encode(ans))
    
    if (ans == "3"):
        city = input("Please enter city name: ")
        CS.send(str.encode(city))
    
    if (ans == "4"):
        iata = input("Please enter flight name: ")
        CS.send(str.encode(iata))
        
        

    res = CS.recv(10000)
    print(res.decode())
    print('\n')