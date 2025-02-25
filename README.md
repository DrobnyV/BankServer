# BankServer

Obecný popis programu
Tento program je bankovní simulátor, který umožňuje správu bankovních účtů a operací prostřednictvím síťového rozhraní. Aplikace je postavena na architektuře klient-server, kde server poskytuje služby pro vytváření účtů, provádění transakcí (vklady, výběry), správu zůstatků a další bankovní operace. Klienti se k serveru připojují pomocí síťového protokolu a komunikují s ním pomocí textových příkazů.

Hlavní funkce programu
Správa bankovních účtů:

Vytváření nových účtů.

Odstranění existujících účtů.

Získání informací o účtu (zůstatek).

Transakce:

Vklady na účty.

Výběry z účtů.

Správa banky:

Získání celkové částky v bance.

Získání počtu účtů v bance.

Síťová komunikace:

Server naslouchá na zadané IP adrese a portu.

Klienti se připojují k serveru a posílají příkazy.

Podpora pro proxy komunikaci mezi bankami (pokud je účet v jiné bance).

Logování:

Veškeré operace jsou logovány do souboru bank_system.log a zobrazovány na standardním výstupu.

Technologie a nástroje
Programovací jazyk: Python 3.

Databáze: SQLite3 pro ukládání informací o bankách a účtech.

Síťová komunikace: Socket API pro klient-server komunikaci.

Logování: Vestavěný modul logging pro sledování činnosti aplikace.

Konfigurace: Soubor conf.ini pro nastavení serveru a dalších parametrů.

Cíl programu
Cílem programu je demonstrovat schopnosti práce se síťovou komunikací, databázemi a logováním v Pythonu. Zároveň slouží jako ukázka jednoduchého bankovního systému, který lze rozšířit o další funkce, jako je šifrování komunikace, podpora více měn nebo integrace s externími platebními systémy.

Tento program je vhodný pro výukové účely, demonstraci základních principů síťové komunikace a správy databází, ale také jako základ pro složitější bankovní aplikace.

1. Návod k spuštění a ovládání aplikace
Požadavky
Python 3.8 nebo novější.

Nainstalované závislosti (viz requirements.txt).

Instalace
Naklonujte repozitář:

git clone <URL_repozitáře>

Konfigurace
Upravte soubor conf.ini podle potřeby:

[SERVER]
HOST = 127.0.0.1
PORT = 12345
PORT_TO_SCAN = 12346
TIMEOUT = 60
TIMEOUT_PORT = 1.0
Spuštění serveru
Spusťte server:

python main.py
Server bude naslouchat na adrese a portu uvedeném v conf.ini.

Ovládání klienta
Připojte se k serveru pomocí nástroje jako putty nebo vlastního klienta:

Příkazy pro komunikaci se serverem:

BC: Získání kódu banky.

AC: Vytvoření nového účtu.

AD <číslo_účtu>/<kód_banky> <částka>: Vklad na účet.

AW <číslo_účtu>/<kód_banky> <částka>: Výběr z účtu.

AB <číslo_účtu>/<kód_banky>: Získání zůstatku účtu.

AR <číslo_účtu>/<kód_banky>: Odstranění účtu.

BA: Získání celkové částky v bance.

BN: Získání počtu účtů v bance.

help: Zobrazení nápovědy.

exit: Ukončení spojení.

2. Použité zdroje
AI nástroje
ChatGPT: Konzultace a generování částí kódu.

Odkaz na konverzaci

https://chatgpt.com/share/67933cf0-ea00-800a-b2be-fda54f923488

Manuály a dokumentace
Python SQLite3 dokumentace - https://docs.python.org/3/library/sqlite3.html

Python Socket Programming - https://realpython.com/python-sockets/

Python Logging - https://realpython.com/python-logging/

Command pattern - https://www.geeksforgeeks.org/command-pattern/

3. Znovupoužitý kód
Z předchozích projektů
Použítí configu:
https://github.com/DrobnyV/ThetaDB/blob/main/src/database.py
Socket server:

Základní implementace socket serveru byla převzata z projektu, který jsme dělali v hodině.

Testevání proběhlo pomocí spolužáků:
Matěj Červenka
Tomáš Hůla
Daniel Linda

Nalezené chyby:
Špatné odpovědi při připojení naserver - opraveno.
Špatné formátování a odřádkování - opraveno.
Automatické posílání prázdné zprávy - opraveno.
Špatný port range. - opraveno.
Odesílání ER kvůli timeout i když vše bylo v pořádku.
