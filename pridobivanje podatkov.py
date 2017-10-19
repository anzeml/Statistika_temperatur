import urllib.parse
import urllib.request
import re
import time
from datetime import datetime

f=open("temparatura_10let.txt","w")
def timestamp(curr, format):
    stime = time.mktime(time.strptime(curr, format))
    print(stime)
    stime += 3600*24
    print(stime)
    return time.strftime(format, time.localtime(stime))

def dni(l,m):
    '''koliko je dni meseca m, leta l'''
    if m in {1,3,5,7,8,10,12}: #ti meseci imajo 31 dni
        return 32
    elif m == 2:
        if 1%4 != 0: #če leto ni prestopno
            return 29
        else: #če je prestopno, ne obravnavamo posebnih (vsako stoto..)
            return 30
    return 31 #sicer bo 30 dni

for l in range(2011,2017): #gremo po letih
    print(str(l)) #testni izpis, izpiše leto
    g=open("temparature"+str(l)+".txt","w")
    for m in range(1,13): #gremo po mesecih          
        for d in range(1,dni(l,m)):#gremo po dneh
            print(str(l)+str(d)+str(m)) #testni izpis, da vidimo pri katerem datumu smo
            full_url = "http://www.wunderground.com/history/airport/LJLJ/"+str(l)+"/"+str(m)+"/"+str(d)+"/DailyHistory.html" #stran, ki jo hočemo
            # preberemo celotno stran, shranimo v spremenljivko 'the_page'
            req = urllib.request.Request(full_url)
            response = urllib.request.urlopen(req)
            the_page = response.read().decode('windows-1250')
            # ko z F12 pregledam spletno stran, ugotovim, kje se podatki nahajajo
            # '(.*?)' dobi vse, kar je med tem dvema oznakama
            podatki_o_temparaturah = re.search(r'<table cellspacing="0" cellpadding="0" id="obsTable" class="obs-table responsive">(.*?)</table>', str(the_page), re.S)

            if podatki_o_temparaturah==None:
                print("nič") #testni izpis, vidim da ni podatka
                continue #da ne javlja napak
            
            # re.search() nam razvrsti podatke kot
            # group 0: <table cellspacing="0" cellpadding="0" id="obsTable" class="obs-table responsive">
            # group 1: (.*?) - TA nas edini zanima
            # group 2: </table>
            
            podatki_brez_tabele=podatki_o_temparaturah.group(1)
            #<tr> in </tr> oznacuje vrstice v tabeli na strani
            #potrebujem <tr> in </tr>
            seznam_temparatur = re.findall(r'<tr class="no-metars">(.*?)</tr>', podatki_brez_tabele, re.S)
            
            for temperatura_za_uro  in seznam_temparatur:
                s=""
                # podatki se nahajajo <td> in </td> - stolpec		
                tempura = re.findall(r'<td *>(.*?)</td>', temperatura_za_uro, re.S)
                # poberemo ure
                d=datetime.strptime(tempura[0].strip(), "%I:%M %p")
                # jih uredimo da se začne z 00:00 konča 24:00
                s+=d.strftime("%H:%M")+";"
                # dodamo še temperautre
                s+=re.sub(r'(<.*?>)', '', tempura[1].replace("&nbsp;&deg;C","").strip() )

                # podatkom dodamo datum, ustrezno formatiramo
                if m<10:
                    if d<10:
                        print(str(l)+"0"+str(m)+"0"+str(d)+";"+s,file=g)
                        print(str(l)+"0"+str(m)+"0"+str(d)+";"+s,file=f)
                    else:
                        print(str(l)+"0"+str(m)+str(d)+";"+s,file=g)
                        print(str(l)+"0"+str(m)+str(d)+";"+s,file=f)
                else:
                    if d<10:
                        print(str(l)+str(m)+"0"+str(d)+";"+s,file=g)
                        print(str(l)+str(m)+"0"+str(d)+";"+s,file=f)
                    else:
                        print(str(l)+str(m)+str(d)+";"+s,file=g)
                        print(str(l)+str(m)+str(d)+";"+s,file=f)

    g.close()
f.close()
