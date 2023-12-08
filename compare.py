#!/usr/bin/python3
import cgitb
import cgi
import requests
from urllib.request import Request, urlopen
import re

cgitb.enable()

def compare_shows():
    s1 = form.getvalue("show1", "Star Trek")
    s2 = form.getvalue("show2", "Bonanza")

    # look at show number 1
    x =  re.match("tt", s1)
    if x:
        first_search = s1
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
        if re.match("tt", title[0]):
            first_search = title[0]
        else:
            first_search = s1
        try:
            i = 0
            for x in name:
                print('<p><a href="http://www.remotestat.com/compare.py?show1=' + title[i] + '&show2=' + s2 +'">')
                print(str(i+1) + ": " + x + " (" + title[i] + ")</a></p>")
                i = i + 1
        except:
            print("<p>NOT FOUND</p>")

    y = re.match("tt", s2)
    if not y:
        print("<p>Looking this (" + s2 + ") up on the database...</p>")
        s2 = s2.replace(' ', '%20')
        req = Request(url='https://www.imdb.com/find/?q=' + s2, headers={'User-Agent': 'Mozilla/6.0'})
        page = str(urlopen(req).read().decode('utf-8'))
        page = page.replace('\\u0026', '')
        pattern = '=fn_al_tt.*?>(.*?)</a>'
        name = re.findall(pattern, page)
        pattern = '/title/(tt.*?)/'
        title = re.findall(pattern, page)
        try:
            i = 0
            for x in name:
                print('<p><a href="http://www.remotestat.com/compare.py?show1=' + first_search + '&show2=' + title[i] + '">')
                print(str(i + 1) + ": " + x + " (" + title[i] + ")</a></p>")
                i = i + 1
        except:
            print("<p>NOT FOUND</p>")

    if x and y:
        req = Request(url='https://www.imdb.com/title/' + s1 + '/fullcredits', headers={'User-Agent': 'Mozilla/6.0'})
        html = str(urlopen(req).read().decode('utf-8'))
        html = html.replace('\\u0026', '')
        html = html.replace('&amp;', '&')

        pattern = "<title>"
        start_loc = html.find(pattern)
        pattern = "</title>"
        end_loc = html.find(pattern)
        title1 = str(html[start_loc+7:end_loc])
        title_fix = ""
        for x in title1:
            if ord(x) < 200:
                title_fix = title_fix + x
                if x == ')':
                    break
            else:
                title_fix = title_fix + '-'
        print("<p>Title #1: " + title_fix + "</p>")
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

        req = Request(url='https://www.imdb.com/title/' + s2 + '/fullcredits', headers={'User-Agent': 'Mozilla/6.0'})
        html = str(urlopen(req).read().decode('utf-8'))
        html = html.replace('\\u0026', '')
        html = html.replace('&amp;', '&')

        pattern = "<title>"
        start_loc = html.find(pattern)
        pattern = "</title>"
        end_loc = html.find(pattern)
        title2 = str(html[start_loc + 7:end_loc])
        title_fix = ""
        for x in title2:
            if ord(x) < 200:
                title_fix = title_fix + x
                if x == ')':
                    break
            else:
                title_fix = title_fix + '-'
        print("<p>Title #2: " + title_fix + "</p>")
        pattern = 'name="cast"'
        start_loc = html.find(pattern)
        pattern = 'name="producer"'
        end_loc = html.find(pattern)
        html_cast = html[start_loc:end_loc]

        # Get all names!
        pattern = 'href="/name/nm.*?\n.*?\n.*?</a>'
        clist = re.findall(pattern, html_cast)

        pattern = 'href="/name/(nm\d+).*?\n> (.*?)\n.*?</a>'
        name_list2 = re.findall(pattern, html_cast)

        char_list2 = []
        for x in range(len(clist)):
            start_loc = html_cast.find(clist[x])
            if (x == len(clist) - 1):
                html_element = html_cast[start_loc:start_loc + 500]  # last one can't look for next one
            else:
                end_loc = html_cast.find(clist[x + 1])
                html_element = html_cast[start_loc:end_loc]
            pattern = '"/title/.*?</a>'
            charx = str(re.findall(pattern, html_element))
            start_loc = charx.rfind('"')
            end_loc = charx.rfind('<')
            charx = charx[start_loc + 3:end_loc]
            charx = charx.replace('\\', '')
            char_list2.append(charx)

        set_a = set(name_list1)
        set_b = set(name_list2)

        set_both = set_a & set_b
        # print(f'List of actors in both shows ({len(set_both)}):')
        print("<table style='width:80%'><colgroup><col style='background-color:AliceBlue'><col style='background-color:Azure'><col style='background-color:LightCyan'></colgroup>")
        print("<tr><th>Name</th><th>Char #1</th><th>Char #2</th></tr>")
        for x in set_both:
            index1 = name_list1.index(x)
            index2 = name_list2.index(x)
            a = "{:<25}".format(x[1].strip())
            b = "{:<33}".format(char_list1[index1])
            c = "{:<33}".format(char_list2[index2])
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
            c_fix = ""
            for x in c:
                if ord(x) < 200:
                    c_fix = c_fix + x
                    if x == ')':
                        break
                else:
                    c_fix = c_fix + '-'
            print("<tr><td>")
            print("<a href='https://www.imdb.com/name/" + nm_list1[index1 - 1] + "/fullcredits'>")
            print(a_fix)
            print("</a>")
            print("</td><td>" + b_fix + "</td><td>" + c_fix + "</td></tr>")
        print("</table>")
        #HYPERLINK

        a = f'\nTotal crossover count:  {len(set_both)}'
        print("<p>" + a + "</p>")

# Print necessary headers.
print("Content-Type: text/html")
# Always print a blank line between headers and rest of HTML
print()

# Title of page (in bar on page)
print("<title>Compare two TV shows</title>")
# Start of body/html
print("<html><body>")
# Heading for what this page does
print("<h1>Enter two TV shows:</h1>")
# Link back to home page
print('<p><a href="http://www.remotestat.com/">Home</a></p>')

# Pull the POST fields off the form
form = cgi.FieldStorage()

compare_shows()

show1 = form.getvalue("show1", "Star Trek")
show2 = form.getvalue("show2", "Bonanza")

print("<form method='post' action='compare.py'>")
show1 = show1.replace('%20', '')
print("<p>Show #1 Lookup: <input type='text' name='show1' value='" + show1 + "' /></p>")
#print("<p>Show #1 Season (1, 2, 3, etc.): <input type='text' name='season1' /></p>")
print("<p>Show #2 Lookup: <input type='text' name='show2' value='" + show2 + "' /></p>")
print("<input type='submit' value='Submit' />")
print("</form>")

print("<h2>Instructions</h2>")
print("<p>1. Enter two TV show names into the boxes above (just needs to be close enough for search)</p>")
print("<p>2. Press enter or submit.</p>")
print("<p>3. Click on the link of the first show you want to compare (top five results)</p>")
print("<p>4. Click on the link of the second show you want to compare (top five results)</p>")
print("<font color='#9900FF'><p> Note: clicking on the second link first assumes you want to pick the first link in the first set</p></font>")
print("<p>5. Type over the search results to compare a new show to the other one in the list</p>")
print("<p>6. Click on the actor name hyperlink to look at full credits for the actor</p>")
print("<font color='#9900FF'>Note: hold down link on phone and 'open new tab in incognito mode' to get the text version</p></font>")

# End of body/html
print("</body></html>")