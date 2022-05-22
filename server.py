import requests
import json
import threading
import socket
from prettytable import PrettyTable


############################################################

class Server:

    def __init__(self):

        self.SS = socket.socket()
        self.host = '127.0.0.1'
        self.port = 2004

        try:
            self.SS.bind((self.host, self.port))

        except socket.error as e:
            print(str(e))

        print("Server is Loading Data of Flights..")
        arr_icao = input("Enter the arr_icao [4 Letters or more..]")
        flights_data = self.get_flights_info(arr_icao)
        print("Done Loading..")

        print('Server is listening..')
        self.SS.listen(5)

        # Counter for Clients
        self.ThreadCount = 0

        # Accepting Clients
        while True:
            Client, address = self.SS.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))

            # Adding the new Connecting to new thread
            t = threading.Thread(target=self.multi_threaded_client, args=(Client, flights_data))
            t.start()

    # Function to retreive information of flights
    def get_flights_info(self, arr_icao):

        URL = "http://api.aviationstack.com/v1/flights"
        ACCESS_KEY = "a6c52dceffdd0ec63fd1d2baea61ed4b"

        PARAMS = {'access_key': ACCESS_KEY,
                  'arr_icao': arr_icao,
                  'limit': 100}

        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()

        filename = "Group_1.json"
        with open(filename, "w") as file:
            file.write(json.dumps(data))

        return data

    ############################################################
    # Function of Server (Responses)
    def multi_threaded_client(self, connection, flights_data):
        connection.send(str.encode('Server message: Identify yourself please..'))

        # 1- Accepting username
        name = connection.recv(1024)
        print("Connected with ", name.decode())
        response = 'Server message: Hello ' + name.decode()
        connection.sendall(str.encode(response))

        req = "0"
        while (req != "5"):
            # 2- Accepting Requests
            req = connection.recv(1024)
            req = req.decode()
            if req == "1":
                print("Client: ", name.decode(), " Requested All Arrived Flights...")
                info = self.arrived_flights(flights_data)
                connection.sendall(str.encode(info))

            elif req == "2":
                print("Client: ", name.decode(), " Requested All Delayed Flights...")
                info = self.delayed_flights(flights_data)
                connection.sendall(str.encode(info))

            elif req == "3":
                print("Client: ", name.decode(), " Requested All flights for a specific city...")
                city = connection.recv(1024)
                city = city.decode()
                print("City Name: ", city)
                info = self.flights_city(flights_data, city)
                connection.sendall(str.encode(info))

            elif req == "4":
                print("Client: ", name.decode(), " Requested All info about a specific Flight...")
                iata = connection.recv(1024)
                iata = iata.decode()
                print("Flight Name: ", iata)
                info = self.special_flight(flights_data, iata)
                connection.sendall(str.encode(info))

            elif req == "5":
                print("Client: ", name.decode(), "Closing Connection with server..")
                connection.sendall(str.encode("Thank You!!"))
                connection.close()

    ####################################################################
    # Option 1:
    def arrived_flights(self, flights_data):

        data = []
        output_str = []
        information = flights_data['data']
        x = PrettyTable()
        x.field_names = ["Flight-IATA", "Dep-Airport", "Arrival-Time", "Terminal", "Gate"]

        for info in information:
            if info['flight_status'] == 'landed':
                d = {}
                d['flight_iata'] = str(info['flight']['iata'])
                d['dep_airport'] = str(info['departure']['airport'])
                d['arrival_time'] = str(info['arrival']['estimated']).split(':')[0]
                d['terminal'] = str(info['arrival']['terminal'])
                d['gate'] = str(info['arrival']['gate'])

                data.append(d)

        for d in data:
            x.add_row([d['flight_iata'], d['dep_airport'], d['arrival_time'], d['terminal'], d['gate']])

        return x.get_string()

    ###############################################################
    # Option2
    def delayed_flights(self, flights_data):

        data = []
        output_str = []

        information = flights_data['data']

        for info in information:
            if info['departure']['delay'] is not None:
                d = {}
                d['flight_iata'] = str(info['flight']['iata'])
                d['dep_time'] = str(info['departure']['estimated'].split(':')[0])
                d['dep_airport'] = str(info['departure']['airport'])
                d['terminal'] = str(info['arrival']['terminal'])
                d['gate'] = str(info['arrival']['gate'])
                d['est_arrival'] = info['arrival']['estimated'].split(':')[0]
                d['sch_arrival'] = info['arrival']['scheduled'].split(':')[0]
                d['delay'] = str(info['departure']['delay'])

                data.append(d)

        x = PrettyTable()
        x.field_names = ["Flight-IATA", "Dep-Airport", "Dep-Time", "Arrival-Scheduled", "Arrival-Estimated", "Terminal",
                         "Gate", "Delay"]
        for d in data:
            x.add_row(
                [d['flight_iata'], d['dep_airport'], d['dep_time'], d['sch_arrival'], d['est_arrival'], d['terminal'],
                 d['gate'], d['delay']])

        if (len(data) == 0):
            return "Sorry, no data found for delayed flights.."
        else:
            return x.get_string()

    ########################################################################
    # Option 3
    def flights_city(self, flights_data, city):

        data = []

        information = flights_data['data']

        for info in information:
            if info['departure']['iata'] == str(city).upper():
                d = {}
                d['flight_iata'] = str(info['flight']['iata'])
                d['dep_time'] = str(info['departure']['estimated'].split(':')[0])
                d['dep_airport'] = str(info['departure']['airport'])
                d['terminal'] = str(info['arrival']['terminal'])
                d['gate'] = str(info['arrival']['gate'])
                d['city_iata'] = str(info['departure']['iata'])

                data.append(d)

        x = PrettyTable()
        x.field_names = ["Flight-IATA", "Dep-Airport", "Dep-Time", "Terminal", "Gate", "CITY-IATA"]

        for d in data:
            x.add_row(d['flight_iata'], d['dep_airport'], d['dep_time'], d['terminal'], d['gate'], d['city_iata'])

        if (len(data) == 0):
            return "Sorry, no data found for this city.."
        else:
            return x.get_string()

    #######################################################################3
    # Option 4 -> Special flight
    def special_flight(self, flights_data, flight_iata):
        data = []

        information = flights_data['data']

        for info in information:
            if info['flight']['iata'] == flight_iata.upper():
                d = {}
                d['flight_iata'] = str(info['flight']['iata'])
                d['dep_time'] = str(info['departure']['estimated'].split(':')[0])
                d['dep_airport'] = str(info['departure']['airport'])
                d['terminal'] = str(info['arrival']['terminal'])
                d['gate'] = str(info['arrival']['gate'])
                d['city_iata'] = str(info['departure']['iata'])
                d['status'] = str(info['flight_status'])
                data.append(d)

        x = PrettyTable()
        x.field_names = ["Flight-IATA", "Dep-Airport", "Dep-Time", "Terminal", "Gate", "CITY-IATA", "Status"]

        for d in data:
            x.add_row([d['flight_iata'], d['dep_airport'], d['dep_time'], d['terminal'], d['gate'], d['city_iata'],
                       d['status']])

        if (len(data) == 0):
            return "Sorry, no data found for this IATA.."
        else:
            return x.get_string()
    ##########################################################################


server = Server()