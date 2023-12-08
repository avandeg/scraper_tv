#!/usr/bin/python3

# Turn on debug mode.
import cgitb
import cgi
import time
cgitb.enable()


print("Content-Type: text/html")
print()

timeStr = time.strftime("%c") # obtains current time

f = open("./index.html", "r")
contents = f.readlines()
for x in contents:
    if "Track Your Stuff" in x:
        print("<p>The current time and date is:  ")
        print(timeStr)
        print(" - UTC</p><br>")
    print(x)

#print(contents)

# Print necessary headers.
print("Content-Type: text/html")
print()

print("<html><body>")
print("<h1> Hello from REMOTESTAT.COM! </h1>")
