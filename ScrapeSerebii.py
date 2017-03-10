import bs4 as bs
import urllib.request
import re
from Pokemon import Pokemon


sauce = urllib.request.urlopen('http://www.serebii.net/duel/figures.shtml').read()
soup = bs.BeautifulSoup(sauce,'lxml')

type_list = ["C", "UC", "R", "EX"]
iDlist = []
nameList = []

pokemonList = []


table= soup.find_all('table')

#returns true if s is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#returns true if s is not a type (C, UC, R, EX)
def notType(s):
    for types in type_list:
        if(s == types):
            return False
    return True

#start when the actual names of Pokemon  begin
for tables in table[3:]:
    table_rows = tables.find_all('tr')
    for rows in table_rows[1:]:
        td_cells = rows.find_all('td')
        for data in td_cells:
                #data contains name, id, type (U, UC, R, EX) and a number
                if(notType(data.text.strip()) and not is_number(data.text)):
                    if("ID" in data.text):
                        iDlist.append(re.findall('\d+',data.text.strip())[0])
                    else:
                        nameList.append(data.text.strip())

#taking out new lines between entries
nameList = filter(None, nameList)
iDlist = filter(None, iDlist)

#special case for nidoran because of symbol after name
for names,id in zip(nameList, iDlist):
    if("nidoran" in names.lower()):
        p = Pokemon("nidoranm", id)
    else:
        p = Pokemon(names.lower() ,id)
    pokemonList.append(p)

#goes to each pokemons webpage
for pokemon in pokemonList:
    print(pokemon.getName())
    sauce1 = urllib.request.urlopen('http://www.serebii.net/duel/figures/{}-{}.shtml'.format(pokemon.getID(),pokemon.getName()))
    soup1 = bs.BeautifulSoup(sauce1, 'lxml')
    statTable = soup1.find_all('table', attrs={'class': 'dextable'})
    moveList = []
    realMoveList = []

    #separating by tr and then starting at the second element since first element is the "layout"
    tr = statTable[0].find_all('tr')
    for td in tr[1:]:
        moveList.append(td.text)
        for item in moveList:
            #separate by new lines
            line = item.splitlines();
            x=""
            for words in line[1:]:
                x +=(words+";");
        realMoveList.append(x)

    for moves in realMoveList:
            with open('Database/{}-{}.csv'.format(pokemon.getID(),pokemon.getName()), 'a') as myfile:
                myfile.write(moves)
                myfile.write("\n")
