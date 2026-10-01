import requests #importovani modulu requests za ucelem vytahavani dat z webu
import finnhub #importovani finnhubu do kodu

import datetime #modul pro cas
from datetime import datetime #cas
from datetime import timezone #casova pasma

import time #casovy modul

import csv #modul pro zapisovani

import os #dovoli programu pristup k os
from dotenv import load_dotenv #pomaha nacitat .env soubory (tam mam API)
load_dotenv()
klic = os.getenv("FINNHUB_KEY") #vytahne z .env souboru API klic k finnhubu

akcie = [ #seznam, kde jsou dosaditelne vsechny informace, abych nemusle psat kod 10x
    {"ticker": "NVDA",  "pair": "NVDAxUSD",  "adresa": "Xsc9qvGR1efVDFGLrVsmkzv3qi45LTBjeUKSPmx9qEh"},
    {"ticker": "AAPL",  "pair": "AAPLxUSD",  "adresa": "XsbEhLAtcf6HdfpFZ5xEMdqW8nfAvcsP5bdudRLJzJp"},
    {"ticker": "TSLA",  "pair": "TSLAxUSD",  "adresa": "XsDoVfqeBukxuZHWhdvWHBhgEHjGNst4MLodqsJHzoB"},
    {"ticker": "GOOGL", "pair": "GOOGLxUSD", "adresa": "XsCPL9dNWBMvFtTmwcCA5v3xWPSMEBCszbQdiLLq6aN"},
    {"ticker": "MSTR",  "pair": "MSTRxUSD",  "adresa": "XsP7xzNPvEHS1m6qfanPUGjNmdnmsLKEoNAnHjdxxyZ"},
    {"ticker": "HOOD",  "pair": "HOODxUSD",  "adresa": "XsvNBAYkrDRNhA7wPHQfX3ZUXZyZLdnCQDfHZ56bzpg"},
    {"ticker": "CRCL",  "pair": "CRCLxUSD",  "adresa": "XsueG8BtpquVJX9LVLLEGuViXUungE6WmK5YZ3p3bd1"},
    {"ticker": "SPY",   "pair": "SPYxUSD",   "adresa": "XsoCS1TfEyfFhfvj8EtZ528L3CaKBDBRqRapnBbDF2W"},
    {"ticker": "QQQ",   "pair": "QQQxUSD",   "adresa": "Xs8S1uUs1zvS2p7iwtsG3b6fkhpvmwz4GYU3gWAmWHZ"},
    {"ticker": "GLD",   "pair": "GLDxUSD",   "adresa": "Xsv9hRk1z5ystj9MhnA7Lq4vjSsLwzL2nxrwmwtD3re"},
]
finnhub_client = finnhub.Client(api_key=klic)  # vytvori spojeni s finnhubem

for i in range(5): #mel jsem problem s gitem a jeho cyklaci, spustim to vzdykcy 4x, abych zamezil tomu, ze prijdu o data
    soubor = open("datasoc.csv", "a", newline="", encoding="utf-8")  # otevru soubor
    zapisovac = csv.writer(soubor)  # pojmenuju promennou, co zapisuje
    cas = datetime.now(timezone.utc)  # ziska aktualni, nemenny cas (neni ovlivnen casovymi posuny)
    cas = cas.isoformat()  # prepise do textoveho formatu
    for a in akcie: #cyklus
        try: #kdyz vyjde, tak normalne zapise
            ak = (finnhub_client.quote(a["ticker"])) #klasicka akcie
            ak = ak["c"] #cena posledniho obchodu
        except: #kdyz kvuli necemu nevyjde, zapise none a cely program se kvuli tomu nezesype
            ak = None

        try:
            atk = (requests.get(f"https://api.kraken.com/0/public/Ticker?pair={a['pair']}&asset_class=tokenized_asset")) #tokenizovana akcie kraken
            atk = atk2 = atk3 = atk4 = atk5 = atk.json() #ulozeni dat z requestu

            atk = atk["result"][a["pair"]]["c"][0] #cena posledniho obchodu

            atk2 = atk2["result"][a["pair"]]["a"][0] #cena ask (za kolik koupim)

            atk3 = atk3["result"][a["pair"]]["b"][0] #cena bid (za kolik prodam)

            atk4 = atk4["result"][a["pair"]]["t"][0] #pocet obchodu od 0:00

            atk5 = atk5["result"][a["pair"]]["t"][1] #pocet obchodu za poslednich 24 hodin
        except:
            atk, atk2, atk3, atk4, atk5 = None, None, None, None, None

        try:
            atoc = (requests.get(f"https://api.geckoterminal.com/api/v2/simple/networks/solana/token_price/{a['adresa']}")) #tokenizovana akcie onchain
            atoc = atoc.json()
            atoc = atoc["data"]["attributes"]["token_prices"][a["adresa"]] #cena na on-chainu
        except:
            atoc = None

        zapisovac.writerow([cas, a["ticker"], ak, atk, atk2, atk3, atk4, atk5, atoc]) #reknu, co zapsat

        print(ak)
        print(atk, atk2, atk3, atk4, atk5)
        print(atoc)
        print(cas)
        print("")
        time.sleep(15)
    soubor.close()  #zavru soubor
    time.sleep(3600)
