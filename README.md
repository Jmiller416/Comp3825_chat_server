# Comp3825_chat_server
The document will cover the design of the chat server.

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
