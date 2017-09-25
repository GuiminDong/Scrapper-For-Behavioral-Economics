# coding=utf-8
import requests, csv, os, sys
from bs4 import BeautifulSoup


def getYear(year, writer1, writer2, writer3):
    url = "https://gdp.giustizia.it/index.php"
    headers = {}
    headers["Host"] = "gdp.giustizia.it"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    headers["Accept-Language"] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Connection"] = "keep-alive"
    headers["DNT"] = "1"
    headers["Referer"] = "https://gdp.giustizia.it/index.php?menu=ricerche&pagina=cambiaufficio&nextpagina=direttarg"
    headers["Cookie"] = "PHPSESSID=gfm1l4dbn657qjooipntse0b87"
    headers["Upgrade-Insecure-Request"] = "1"
    arrKey = []
    e = 0
    i = 1
    while 1:
        print "year:", year, "i:", i
        session = requests.session()
        data = {"pagina": "direttarg", "menu": "ricerche", "idatto": "", "NUMPROC": i, "AAPROC": year, "ricercax": "numproc"}
        try:
            rst = session.post(url, data=data, headers=headers, timeout=20)
        except:
            print i, "error"
            continue
        if rst.content.find("Nessun fascicolo trovato!") != -1:
            e += 1
            if e >= 50:
                return
            i += 1
            continue
        if rst.content.find("ATTENZIONE!! Fascicolo pre-iscritto e non ancora caricato!") != -1:
            i += 1
            continue
        soup = BeautifulSoup(rst.content, "lxml")
        main = soup.find("div", {"id": "div_main"})
        tb1 = main.findAll("table")[0].findAll("tr")
        tb2 = main.findAll("p")
        tb3 = main.findAll("table")[1].findAll("tr")
        rst1 = [year, i]
        for tr in tb1:
            tds = tr.findAll("td")
            if len(tds) != 3:
                continue
            rst1.append(tds[0].get_text().encode("utf-8"))
            rst1.append(tds[1].get_text().encode("utf-8"))
            rst1.append(tds[2].get_text().encode("utf-8"))
        writer1.writerow(rst1)

        rst2 = {"Ruolo Gen. Nr.": "", "Oggetto": "", "Giudice": "", "Valore della causa": "", "Stato del fascicolo": "",
                "Data di Citazione 1° udienza": "", "SENTENZA DEFINITIVA Nr.": "", "Esito": "", "Importo liquidato": "",
                "Tipo": "", "DECRETO INGIUNTIVO Nr.": "", "SENTENZA NON DEFINITIVA Nr.": "", "Rif. atto impugnato": "",
                "Importo richiesto": "", "Prossima udienza": "", "Domanda riconvenzionale": "", "Riconvenzionale concessa": "",
                "Motivo rinvio": "", "Ordinanza prefettizia": "", "Cartella esattoriale": "", "Ultima udienza": ""}
        beg, end = False, False
        for p in tb2:
            if p.find("a") != None:
                continue
            val = p.get_text().strip()
            if end:
                break

            if val == "Parti fascicolo":
                beg = True
                continue
            if beg == False:
                continue


            if val == "Storico fascicolo":
                end = True
                continue

            k = val.split(":")[0].strip()
            v = val.replace(k+": ", "").strip()
            k = k.replace("  ", " ").encode("utf-8")
            if k == "SENTENZA NON DEFIN":
                k = "SENTENZA NON DEFINITIVA Nr."
            if k == "Rif. atto impugnat":
                k = "Rif. atto impugnato"
            if k == "Importo r":
                k = "Importo richiesto"
            if k == "Importo r":
                k = "Importo richiesto"
            if k == "Tipo decreto":
                k = "Tipo"
            if k not in rst2.keys():
                print k
            rst2[k] = v
            # print k, "---------", v
        for kk in rst2:
            rst2[kk] = rst2[kk].encode("utf-8")
        writer2.writerow([year, i, rst2["Ruolo Gen. Nr."], rst2["Oggetto"], rst2["Giudice"],
                         rst2["Valore della causa"], rst2["Stato del fascicolo"], rst2["Data di Citazione 1° udienza"],
                          rst2["SENTENZA DEFINITIVA Nr."], rst2["Esito"], rst2["Importo liquidato"], rst2["Tipo"],
                          rst2["DECRETO INGIUNTIVO Nr."], rst2["SENTENZA NON DEFINITIVA Nr."], rst2["Rif. atto impugnato"],
                          rst2["Importo richiesto"], rst2["Prossima udienza"], rst2["Domanda riconvenzionale"],
                          rst2["Riconvenzionale concessa"], rst2["Motivo rinvio"], rst2["Ordinanza prefettizia"],
                          rst2["Cartella esattoriale"], rst2["Ultima udienza"]])

        for tr in tb3:
            tds = tr.findAll("td")
            if len(tds) != 3:
                continue
            rst3 = [year, i]
            rst3.append(tds[0].get_text().encode("utf-8"))
            rst3.append(tds[1].get_text().replace("\n", "").encode("utf-8"))
            rst3.append(tds[2].get_text().encode("utf-8"))
            writer3.writerow(rst3)
        i += 1
if __name__ == "__main__":
    year = sys.argv[1]
    exists = os.path.exists("./data/" + year + '_1.csv')

    csvfile1 = file("./data/" + year + '_1.csv', 'ab')
    csvfile2 = file("./data/" + year + '_2.csv', 'ab')
    csvfile3 = file("./data/" + year + '_3.csv', 'ab')
    writer1 = csv.writer(csvfile1)
    writer2 = csv.writer(csvfile2)
    writer3 = csv.writer(csvfile3)
    if exists == False:
        writer1.writerow(["Year", "Number", "Descrizione parte", "Tipo parte", "Avvocato",
                         "Descrizione parte", "Tipo parte", "Avvocato",
                         "Descrizione parte", "Tipo parte", "Avvocato",
                         "Descrizione parte", "Tipo parte", "Avvocato",
                         "Descrizione parte", "Tipo parte", "Avvocato",
                         "Descrizione parte", "Tipo parte", "Avvocato",
                         "Descrizione parte", "Tipo parte", "Avvocato"])
        writer2.writerow(["Year", "Number", "Ruolo Gen. Nr.", "Oggetto", "Giudice", "Valore della causa", "Stato del fascicolo",
                          "Data di Citazione 1° udienza", "SENTENZA DEFINITIVA Nr.", "Esito", "Importo liquidato", "Tipo",
                          "DECRETO INGIUNTIVO Nr.", "SENTENZA NON DEFINITIVA Nr.", "Rif. atto impugnato", "Importo richiesto",
                          "Prossima udienza", "Domanda riconvenzionale", "Riconvenzionale concessa", "Motivo rinvio", "Ordinanza prefettizia",
                          "Cartella esattoriale", "Ultima udienza"])
        writer3.writerow(["Year", "Number", "Data evento", "Evento", "Sub. procedimento"])

    getYear(year, writer1, writer2, writer3)
    csvfile1.close()
    csvfile2.close()
    csvfile3.close()
