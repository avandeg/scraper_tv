#!/usr/bin/python3
import cgitb
import cgi
import requests
from urllib.request import Request, urlopen
import re

cgitb.enable()

def get_episode_number():
    name = form.getvalue("name", "tt0060028")
    series = form.getvalue("series", "1")
    episode = form.getvalue("episode", "1")
    req = Request(url='https://www.imdb.com/title/' + name + '/episodes/?season=' + str(series),
                  headers={'User-Agent': 'Mozilla/6.0'})
    page = str(urlopen(req).read().decode('utf-8'))
    pattern = '<a href="/title/(tt\d+).*?/?ref_=ttep_ep(\d+)"'
    title_names = re.findall(pattern, page)
    try:
        t1, t2 = zip(*title_names)
        if t2.index(episode) >= 0 and t2.index(episode) < len(t1):
            return(t1[t2.index(episode)])
        else:
            return('tt0060028')
    except:
        return('tt0060028')

def find_episode():
    s1 = form.getvalue("name", "Star Trek")
    series = form.getvalue("series", "1")
    episode = form.getvalue("episode", "1")

    x = re.match("tt", s1)
    if x:
        s2 = get_episode_number()
        print("<p><a href='http://www.remotestat.com/compare.py?show1=" + s2 + "&show2=Gunsmoke'>Link to compare episode</a></p>")
        req = Request(url='https://www.imdb.com/title/' + s2 + '/fullcredits', headers={'User-Agent': 'Mozilla/6.0'})
        html = str(urlopen(req).read().decode('utf-8'))
        html = html.replace('\\u0026', '')
        html = html.replace('&amp;', '&')
        pattern = "<title>"
        start_loc = html.find(pattern)
        pattern = "</title>"
        end_loc = html.find(pattern)
        title1 = str(html[start_loc + 7:end_loc])
        title_fix = ""
        for x in title1:
            if ord(x) < 200:
                title_fix = title_fix + x
                if x == ')':
                    break
            else:
                title_fix = title_fix + '-'
        print("<p>Title: " + title_fix + "</p>")
        pattern = 'name="cast"'
        start_loc = html.find(pattern)
        pattern = 'name="producer"'
        end_loc = html.find(pattern)
        html_cast = html[start_loc:end_loc]
        pattern = 'href="/name/nm.*?\n.*?\n.*?</a>'
        clist = re.findall(pattern, html_cast)

        pattern = 'href="/name/(nm\d+).*?\n> (.*?)\n.*?</a>'
        name_list1 = re.findall(pattern, html_cast)
        char_list1 = []
        nm_list1 = []
        for x in range(len(clist)):
            start_loc = html_cast.find(clist[x])
            if (x == len(clist) - 1):
                html_element = html_cast[start_loc:start_loc + 500]  # last one can't look for next one
            else:
                end_loc = html_cast.find(clist[x + 1])
                html_element = html_cast[start_loc:end_loc]
            pattern = '/name/(nm.*?)/?ref_'
            namex = str(re.findall(pattern, html_element))
            start_loc = namex.rfind('nm')
            end_loc = namex.rfind('/?')
            namex = namex[start_loc:end_loc]
            nm_list1.append(namex)
            pattern = '"/title/.*?</a>'
            charx = str(re.findall(pattern, html_element))
            start_loc = charx.rfind('"')
            end_loc = charx.rfind('<')
            charx = charx[start_loc + 3:end_loc]
            charx = charx.replace('\\', '')
            char_list1.append(charx)

        print("<table style='width:50%'><colgroup><col style='background-color:AliceBlue'><col style='background-color:Azure'></colgroup>")
        print("<tr><th>Name</th><th>Char #1</th></tr>")
        for x in name_list1:
            index1 = name_list1.index(x)
            a = "{:<25}".format(x[1].strip())
            b = "{:<33}".format(char_list1[index1])
            a_fix = ""
            for x in a:
                if ord(x) < 200:
                    a_fix = a_fix + x
                    if x == ')':
                        break
                else:
                    a_fix = a_fix + '-'
            b_fix = ""
            for x in b:
                if ord(x) < 200:
                    b_fix = b_fix + x
                    if x == ')':
                        break
                else:
                    b_fix = b_fix + '-'
            print("<tr><td>")
            print("<a href='https://www.imdb.com/name/" + nm_list1[index1 - 1] + "/fullcredits'>")
            print(a_fix)
            print("</a>")
            print("</td><td>" + b_fix + "</td></tr>")
        print("</table>")

    else:
        print("<p>Looking this (" + s1 + ") up on the database...</p>")
        s1 = s1.replace(' ', '%20')
        req = Request(url='https://www.imdb.com/find/?q=' + s1, headers={'User-Agent': 'Mozilla/6.0'})
        page = str(urlopen(req).read().decode('utf-8'))
        page = page.replace('\\u0026', '')
        pattern = '=fn_al_tt.*?>(.*?)</a>'
        name = re.findall(pattern, page)
        pattern = '/title/(tt.*?)/'
        title = re.findall(pattern, page)
        try:
            i = 0
            for x in name:
                print('<p><a href="http://www.remotestat.com/episode.py?name=' + title[i] + '&series=' + str(series) + '&episode=' + str(episode) + '">')
                print(str(i + 1) + ": " + x + " (" + title[i] + ")</a></p>")
                i = i + 1
        except:
            print("<p>NOT FOUND</p>")

# Print necessary headers.
print("Content-Type: text/html")
print()

print("<title>Search for an episode</title>")
print("<html><body>")
print("<h1> Enter a TV show name for search:</h1>")
print('<p><a href="http://www.remotestat.com/">Home</a></p>')

form = cgi.FieldStorage()

name = form.getvalue("name", "Star Trek")
series = form.getvalue("series", "1")
episode = form.getvalue("episode", "1")

find_episode()

print("<form method='post' action='episode.py'>")
name = name.replace('%20', '')
print("<p>TV Show Lookup: <input type='text' name='name' value='" + name + "' /></p>")
print("<p>Series (index year): <input type='number' name='series' value='" + str(series) + "' /></p>")
print("<p>Episode (index): <input type='number' name='episode' value='" + str(episode) + "' /></p>")
print("<input type='submit' value='Submit' />")
print("</form>")

#name = 'tt0052451'
x = re.match("tt", name)
if x:
    req = Request(url='https://www.imdb.com/title/' + name + '/episodes/?season=' + str(series), headers={'User-Agent': 'Mozilla/6.0'})
    page = str(urlopen(req).read().decode('utf-8'))
    pattern = 'title__text">(.*?)</div>'
    ep_names = re.findall(pattern, page)
    pattern = '<a href="/title/(tt\d+).*?/?ref_=ttep_ep(\d+)"'
    title_names = re.findall(pattern, page)

    t1, t2 = zip(*title_names)
    for x in ep_names:
        if re.match("S", x):
            pattern = r"E\d+"
            ep_find = re.search(pattern, x)
            ep_lu = ep_find.group()[1:]
            try:
                ep_title_lu = t1[t2.index(ep_lu)]
            except:
                ep_title_lu = name
            ep_fix = ""
            for y in x:
                if ord(y) < 200:
                    ep_fix = ep_fix + y
                    if y == ')':
                        break
                else:
                    ep_fix = ep_fix + '-'
            ep_fix = ep_fix.replace('&#x27;', '\'')

            print("<p> <a href='http://www.remotestat.com/episode.py?name=" + name + "&series=" + str(series) + "&episode=" + str(ep_lu) + "'>")
            print("Item:" + str(ep_fix) + "</a> - link - ")
            print("<a href='https://www.imdb.com/title/" + ep_title_lu + "/fullcredits'>database: " + ep_title_lu + "</a></p>")

print("</body></html>")