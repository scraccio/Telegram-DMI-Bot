import bs4
import requests
import json

def getGiorno(giorno):
    if giorno == "LUN":
        return 1
    elif giorno == "MAR":
        return 2
    elif giorno == "MER":
        return 3
    elif giorno == "GIO":
        return 4
    elif giorno == "VEN":
        return 5
    else:
        return 0
def scrape_orario():
    ids = ["l-31","l-35","lm-18","lm-40"]
    materie = []
    for id_ in ids:
        url = "http://web.dmi.unict.it/corsi/"+str(id_)+"/orario-lezioni"
        sorgente = requests.get(url).text
        soup = bs4.BeautifulSoup(sorgente, "html.parser")



        if soup.find('b',id='attivo').text[0] == 'S':
            semestre = 2;
        elif soup.find('b',id='attivo').text[0] == 'P':
            semestre = 1;

        table = soup.find('table',id='tbl_small_font')
        tr_all =  table.find_all('tr')

        anno = 1
        for tr in tr_all:
                td_all = tr.find_all('td')
                #Calcola anno materia
                td_anno = tr.find('td')
                if td_anno is not None:
                    if td_anno.text[0] == '2' or td_anno.text[0] == '3':
                        anno = td_anno.text[0]

                if len(td_all) == 3:
                    orarioDefinitivo = []
                    orari = td_all[2]
                    for orario in orari:
                        if str(orario) != '<br/>':
                            giorno = getGiorno(orario[0:3])
                            orario = orario.replace(orario[0:3],'') #GIORNO
                            oraInizio = orario[1:6] #ORA INIZIO
                            print oraInizio
                            oraFine = orario[7:12]
                            print oraFine # ORA FINE
                            orario = orario.replace(oraInizio+"-"+oraFine,'')
                            aula = orario[2:]
                            print aula #AULA

                            materia = {"Nome": td_all[0].text, "GiornoSettimana": giorno, "OraInizio": oraInizio, "OraFine": oraFine, "Aula": aula, "Anno": anno, "Semestre": semestre}
                            materie.append(materia)


    finaljson = {"materie" : materie}
    with open('../data/json/lezioni.json', 'w') as outfile:
        json.dump(finaljson, outfile, sort_keys=False, indent=4)