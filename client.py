# Connecting to Server
import socket


class Client:

    def __init__(self):
        self.CS = socket.socket()
        self.host = '127.0.0.1'
        self.port = 2004
        print('Connecting to Server...')
        try:
            self.CS.connect((self.host, self.port))
        except socket.error as e:
            print(str(e))

        print("Connected to Server..")
        res = self.CS.recv(1024)
        print(res.decode())
        # Identifying yourself and sending username
        self.username = input('Username: ')
        self.CS.send(str.encode(self.username))
        res = self.CS.recv(1024)
        print(res.decode('utf-8'))

        self.ans = "0"
        while (self.ans != "5"):
            # Five Requests
            print("Do you want to: ")
            print("1- Arrived Flights Requests.")
            print("2- Delayed Flights Requests.")
            print("3- All flights coming from a specific city.")
            print("4- Details of particular flight.")
            print("5- Quit..")
            self.ans = input()
            self.CS.send(str.encode(self.ans))

            if (self.ans == "3"):
                city = input("Please enter city name: ")
                self.CS.send(str.encode(city))
                print('\n')

            if (self.ans == "4"):
                iata = input("Please enter flight name: ")
                self.CS.send(str.encode(iata))
                print('\n')

            res = self.CS.recv(10000)
            print(res.decode())
            print('\n')


######################################################3
client = Client()