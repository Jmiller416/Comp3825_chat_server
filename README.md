# Comp3825_chat_server
The document will cover the design of the chat server.

![demo](https://github.com/Jmiller416/Comp3825_chat_server/blob/Master/demo.png?raw=true)

## Setup

### pip
Please install the pip requirements using pip/pip3 depending on how your installed Python3:

```bash
pip3 install -r requirements.txt
```

### Tkinter
Also ensure you have a recent version of Tkinter installed. The system version provided with Python 3 is unsupported on macOS/Linux

#### macOS:
```bash
brew install python-tk
```

#### Linux:
```bash
sudo apt-get install python3-tk
```

#### Windows:
Please see https://tkdocs.com/tutorial/install.html#install-win-python

### SSL/TLS

The project by default includes everything needed to start and run the 
server with a self-signed SSL certificate in the `ssl/` directory. However, I've included these instructions for posterity
and to show I am not a complete moron.

#### Creating the root key
Create the root key (used later) by running the following:
```bash
openssl genrsa -des3 -out server.orig.key 2048
```

The key included in `ssl/` uses the password `comp3825`

##### Output:
```
Generating RSA private key, 2048 bit long modulus
.....+++
........................................+++
e is 65537 (0x10001)
Enter pass phrase for server.orig.key:
Verifying - Enter pass phrase for server.orig.key:
```

#### Generating an RSA key

Create an RSA key from the key you just created by running the following:

```bash
openssl rsa -in server.orig.key -out server.key
```
You will be prompted for the password you entered to secure the `server.orig.key`

##### Output:
```
Enter pass phrase for server.orig.key:
writing RSA key
```

#### Creating the signing request (self-signed)
The certificate signing request (CSR) is generated using OpenSSL like shown:

```bash
openssl req -new -key server.key -out server.csr
```

**Note, do not use a challenge password when prompted, just press Return/Enter**

##### Output:
```
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:US
State or Province Name (full name) []:TN
Locality Name (eg, city) []:Memphis
Organization Name (eg, company) []:University of Memphis
Organizational Unit Name (eg, section) []:COMP-3825
Common Name (eg, fully qualified host name) []:comp-3825-class-project
Email Address []:kbrleson@memphis.edu

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
```

#### Creating the certificate:

I use the certificate signing request with the key generated previously.

```bash
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

##### Output:
```
Signature ok
subject=/C=US/ST=TN/L=Memphis/O=University of Memphis/OU=COMP-3825/CN=comp-3825-class-project/emailAddress=kbrleson@memphis.edu
Getting Private key
```

If you are attempting to run the server and client with your own self-signed certificates,
please ensure they are stored in the `ssl/` directory. Additionally, make sure the certificate is named 
`server.crt` and the key is named `server.key`.

## Design
<body lang=EN-US style='tab-interval:.5in;word-wrap:break-word'>

<div class=WordSection1>

<p class=MsoNormal align=center style='text-align:center;line-height:200%'><span
style='font-size:12.0pt;line-height:200%'>D_1 project design<o:p></o:p></span></p>

<p class=MsoNormal align=center style='text-align:center;line-height:200%'><span
style='font-size:12.0pt;line-height:200%'>Jonathan Miller and Keaton Burleson<o:p></o:p></span></p>

<p class=MsoNormal align=center style='text-align:center;line-height:200%'><span
style='font-size:12.0pt;line-height:200%'><o:p>&nbsp;</o:p></span></p>

<p class=MsoNormal style='line-height:200%'><span style='font-size:12.0pt;
line-height:200%'>A server will spin up and wait for connections to be made
from clients. To handle multiple clients the server will make use of multi-threading
to allow sending and receiving of messages at the same time. When Clients
connect to the server a message will be sent to all clients already connected
notifying them that user &quot;x&quot; has connected to the server. From there
clients will be able to send messages to a specific specified user based on who
is available/connected. If a user disconnects the server will send out a
message to all currently connected users notifying them that client
&quot;y&quot; has disconnected. Users will be able to disconnect from the chat
server by typing <span class=GramE>&quot;.exit</span>&quot; which will close
the connection from the client.<o:p></o:p></span></p>

<p class=MsoNormal style='text-indent:.5in;line-height:200%'><span
style='font-size:12.0pt;line-height:200%'><o:p>&nbsp;</o:p></span></p>

  ![image](https://user-images.githubusercontent.com/91217608/135722432-0fb39f8e-60f6-4757-a109-d201c9fa7897.png)
