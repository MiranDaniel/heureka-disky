# heureka-disky

Software pro hledání levných disků z Heuréky, řazení dle ceny za TB s filtrováním výsledků.

Inspirace z [diskprices.com](https://diskprices.com/) pro disky na Amazonu.

---

## Instalace

### Požadavky

- `python` >= 3.9.2 
- Balíčky ze souboru `requirements.txt`

### Instukce

- Instalace Pythonu, z repozitářů distribuce, wingetu nebo [www.python.org](https://www.python.org/)
- `python3 -m pip3 install -r requirements.txt` pro instalaci balíčků

## Použití

- `python3 scrape.py` načte všechny disky z Heuréky
- `python3 export.py` exportuje data do souboru `output.html`

## Poznámky

- Scraper bot má nastaven timeout jedné sekundy po načtení stánky, pokud program padá kvůli chybě [429](https://http.cat/429), nastavte v souboru `scrape.py` vyšší `sleep`.
- Heuréka nemá veřejné API, program tedy načítá data ze stránek pro lidi, je tedy možnost že se program rozbije po redesignu Heuréky, v tom případě prosím, vytvořte issue.

## Licence

Tento program je svobodný software: můžete jej šířit a upravovat podle ustanovení Obecné veřejné licence GNU (GNU General Public Licence), vydávané Free Software Foundation a to buď podle 3. verze této Licence, nebo (podle vašeho uvážení) kterékoli pozdější verze. 

Tento program je rozšiřován v naději, že bude užitečný, avšak BEZ JAKÉKOLIV ZÁRUKY. Neposkytují se ani odvozené záruky PRODEJNOSTI anebo VHODNOSTI PRO URČITÝ ÚČEL. Další podrobnosti hledejte v Obecné veřejné licenci GNU. 

![](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)

## Kontakt

heureka@mirandaniel.com / abuse@mirandaniel.com
