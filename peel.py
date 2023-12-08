#!/usr/bin/python3
import cgitb
import cgi
import requests
from urllib.request import Request, urlopen
import re

cgitb.enable()

def check_it():
    print('<p>STUFF HERE!</p>')

# Print necessary headers.
print("Content-Type: text/html")
print()

print("<title>Search for actor</title>")
print("<html><body>")
print("<h1> Enter an actor name for search:</h1>")
print('<p><a href="http://www.remotestat.com/">Home</a></p>')

form = cgi.FieldStorage()

if form.getvalue("name"):
    name = form.getvalue("name")
    name = name.replace(' ', '%20')
    req = Request(url='https://www.imdb.com/find/?q=' + name, headers={'User-Agent': 'Mozilla/6.0'})
    html = str(urlopen(req).read().decode('utf-8'))
    html = html.replace('\\u0026', '')
    html = html.replace('&amp;', '&')
    #url = requests.get('https://www.imdb.com/find/?q=' + name)
    #pattern = "/name/(nm.*?)"
    pattern = "/name/(nm[0-9]+.*?)/?.*?>(.*?)</a>"
    name_list = re.findall(pattern, html)
    #print(name_list[0][0])
    #print(len(name_list))
    #match_results = re.search(pattern, url.text, re.IGNORECASE)
    #match_results = re.search(pattern, html, re.IGNORECASE)
    #title2 = match_results.groups(1)
    for x in range(len(name_list)):
        print('<a href="https://www.imdb.com/name/')
        print(str(name_list[x][0]))
        print('/fullcredits">')
        print("<p>" + str(name_list[x][1]) + "--" + str(name_list[x][0]) + "</p>")
        print('</a>')
        #print(<p><a href="https://www.imdb.com/name/" + str(name_list[x][0])
        #+ str(name_list[x][0] + '/fullcredits</a></p>')
        #print('\n')
else:
    name = 'James Stewart'

try:
    if str(name_list[0][0]) != '':
        name_id = name_list[0][0]
    else:
        name_id = 'nm0000675'
except:
    print("<p>NOT FOUND</p>")
    name_id = 'nm0000675'

help_msg = "Enter a name in the Name Lookup box and hit enter or click on the Submit button"

print("<form method='post' action='peel.py'>")
name = name.replace('%20', '')
print("<p>Name Lookup: <input type='text' name='name' value=" + name + " /></p>")
print("<p>ID from database: <input type='text' name='name_id' value=" + name_id + " /></p>")
print("<input type='submit' value='Submit' />")
#print("<input type='button' onclick=alert('help!%20ME!') value='Help' />")
print("</form>")


print("</body></html>")

