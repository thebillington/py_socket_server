# Import socket and protocols
from socket import socket, AF_INET, SOCK_STREAM

# Create a new socket
s = socket(AF_INET, SOCK_STREAM)

# Bind to localhost
host = "127.0.0.1"
port = 5000
s.bind((host, port))

# Listen for incoming connections
s.listen(5)

# Function to return a list of resource identifiers
def decodeResource(resource):
	
	# Strip the first slash
	locations = resource.strip("/")
	
	return locations.split("/")

# Infinite loop
while True:
	
	# Get the connection socket to send data over and address
	cSock, (cHost, cPort) = s.accept()
	
	print("GET request received from {}:{}".format(cHost, cPort))
	
	# Get the request
	request = cSock.recv(1024)
	
	# Get the message data
	data = request.decode().split(" ")
	resourceLocation = data[1]
	locations = decodeResource(resourceLocation)
	
	# Send response header
	cSock.send("HTTP/1.1 200 OK\n".encode())
	cSock.send("Content-Type: text/html\n".encode())
	cSock.send("\n".encode())
	
	# Check if index
	if locations[0] == "" or locations[0] == "index":
		html = "<h1>It works!</h1>\n"
	# Otherwise if it was names
	elif locations[0] == "name":
		# If there was a name in the URL, say hello to them
		if len(locations) > 1:
			html = "<h1>Hello {}!</h1>\n".format(locations[1].title())
		# Otherwise say hello stranger
		else:
			html = "<h1>Hello stranger!</h1>\n"
	else:
		html = "<h1>404 not found!</h1"
	
	# Send html content
	cSock.send(html.encode())
	
	# Close the request
	cSock.close()
