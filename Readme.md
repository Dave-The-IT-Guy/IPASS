# LogfileBrowser
Student: Dave van der Leek (1777075)\
Klas: TICT-CSC-V1F\
Taal: Python(3)
***

## Inhoud:
- Vereisten
- Installeren
- Werken met het programma:
  
- - Starten van het programma:
    
- - - Met een GCLI (een menu)
    
- - - Vanaf de commandline (met parameters)
    
- - - Met een configuratiebestand
    
- - Het aangeven van de locatie van het logbestand

- - Top 10 IP-adressen
    
- - Top 5 dagen
    
- - Aantal connecties die niet gemaakt zijn met het OpenVPN-protocol tonen
    
- - Alle gebruikte management commando's
    
- - Controleren van IP-adressen
    
- - Controleren op nieuwe IP-adressen
    
- - Maken van een nieuw configuratie bestand
    
- - Output wegschrijven naar een bestand
    
- - Combineren van parameters

- - Overige opties
    
- Disclaimer

- Bronnen
***

## Vereisten

Om dit programma successvol te kunnen starten is python 3.8 of hoger nodig. Python is te downloaden vanaf: https://www.python.org/downloads/. Het programma gebruikt alleen librairies die al standaard bij python ingebouwd zitten. Mochten er toch problemen voorkomen bij het uitvoeren van het programma dan zou er gecontroleerd moeten worden of de volgende packages geïnstalleerd zijn:
- `re` voor regex
- `os` voor het zoeken naar bestanden
- `argparse` voor het parsen van de argumenten
- `contextlib` voor het supressen van onnodige error's
- `json` voor het werken met het configuratiebestand
- `datetime` voor het werken met datums

***

## Installeren

Om het programma te installeren moet u de volgende stappen uitvoeren:
- Clone deze repository: https://github.com/Dave-The-IT-Guy/IPASS
- Pak indien nodig de bestanden uit en zet de 'Logbrowser' map op de gewenste locatie.
- Zorg ervoor dat de 'Logbrowser' map en de bestanden in die map voldoende rechten hebben om uit gevoerd kunnen worden door python

Note: In de repository zitten een aantal demobestanden. Het enigste bestand dat echt nodig is om het programma uit te kunnen voeren is: `Logbrowser.py`

***

## Werken met het programma
In dit hoofdstuk staat in een aantal hoofdstukken beschreven wat de functionaliteiten van het programma zijn en hoe deze te gebruiken zijn.


### Het starten van het programma
Het programma kan op verschillende manieren gestart worden. 

#### Manier 1: met een menu:
- Indien er nog geen CLI-window openstaat, open er een.
- Navigeer naar de map waar het programma staat
- Start het programma op met het commando `Logbrowser.py -g`

#### Manier 2: via de CLI (met parameters):
- Indien er nog geen CLI-window openstaat, open er een.
- Navigeer naar de map waar het programma staat
- Start het programma op met het commando `Logbrowser.py {parameters}`

Alle parameters en bijbehorende waardes zijn te vinden met het commando `Logbrowser.py -h` of in het menu die met manier 1 getoond wordt.

#### Manier 3: via een configuratiebestand:
- Indien er nog geen CLI-window openstaat, open er een.
- Navigeer naar de map waar het programma staat
- Start het programma op met het commando `Logbrowser.py -c {logfile}`

Een configuratiebestand kan aangemaakt worden in het menu (optie 10) die met manier 1 getoond wordt. Als het programma via een configuratie bestand gestart wordt, wordt de output altijd weggeschreven naar de file `result.txt`

### Het aangeven van de locatie van het logbestand
Het programma gaat er vanuit dat de logfile standaard in dezelfde map als het programma staat en de naam `openvpn.log` heeft. Als dit niet het geval is kan je een andere locatie aangeven met:
1. Door het programma te starten met de `-l {logfile}` parameter
2. Door de `logfile` optie in het configuratiebestand de waarde van de locatie van de logfile te geven

Als het programma gestart is met menu en het logbestand niet vinden kan dan zal er gevraagd worden om een andere locatie te selecteren. Mocht dit niet het geval zijn dan zal er een foutcode gegeven worden en wordt het programma afgesloten.

### Top 10 IP-adressen
Het programma heeft de mogelijkheid om een top 10 IP-adressen te tonen met de meeste onsuccesvolle of meest succesvolle inlogpogingen. Deze functionaliteit kan op 3 manieren gebruikt worden:
1. Via optie 1 of 2 in het menu
2. Door het programma te starten met de parameter `-t {unsuccessful,successful}`
3. Door de `top10` optie in het configuratiebestand op `unsuccessful` of `successful` te zetten

### Top 5 dagen
Het programma heeft de mogelijkheid om een top 5 van dagen met het meeste aantal onsuccesvolle of succesvolle verbindingen te tonen. Deze functionaliteit kan op 3 manieren gebruikt worden:
1. Via optie 3 of 4 in het menu
2. Door het programma te starten met de parameter `-d {unsuccessful,successful}`
3. Door de `top5` optie in het configuratiebestand op `unsuccessful` of `successful` te zetten

### Aantal connecties die niet gemaakt zijn met het OpenVPN-protocol tonen
Het programma heeft de mogelijkheid om het aantal connecties die niet met het OpenVPN-protocol te tonen. Deze functionaliteit kan op 3 manieren gebruikt worden:
1. Via optie 5 in het menu
2. Door het programma te starten met de parameter `-p`
3. Door de `non-ovpn-prot` optie in het configuratiebestand op `True` te zetten

### Alle gebruikte management commando's
Het programma heeft de mogelijkheid om alle gebruikte management commando's te tonen. Deze functionaliteit kan op 3 manieren gebruikt worden:
1. Via optie 6 in het menu
2. Door het programma te starten met de parameter `-m`
3. Door de `man-coms` optie in het configuratiebestand op `True` te zetten

### Controleren van IP-adressen
Het programma heeft de mogelijkheid om individuele IP-adressen op te zoeken en te controleren. Deze functionaliteit kan op 3 manieren gebruikt worden:
1. Via optie 7 in het menu
2. Door het programma te starten met de parameter `-i {IP-adressen met een spatie gescheiden}`
3. Door de `check-ip` optie in het configuratiebestand in te vullen met een lijst met alle IP-adressen die gecontroleerd moeten worden. Voorbeeld: `"check-ip" = ["IP1", "IP2"]`

### Controleren op nieuwe IP-adressen
Het programma heeft ook de mogelijkheid om de logfile te controleren op nieuwe IP-adressen. Deze functionaliteit kan op 3 manieren gebruikt worden:
1. Via optie 8 in het menu
2. Door het programma te starten met de parameter `-n`
3. Door de `new-ips` optie in het configuratiebestand op `True` te zetten

Om goed de nieuwe IP-adressen te kunnen laten zien heeft het script een bestand nodig waar alle bekende IP-adressen instaan. Dit bestand is de known-ip.txt file. Het programma gaat er standaard vanuit dat dit bestand in dezelfde map staat als het programma. Mocht dat niet zo zijn kan het pad op 2 manieren aangepast worden:
1. Met de `-k {knownip-file location}` parameter
2. Door de `knownip-file` optie in het configuratiebestand op `{knownip-file location}` te zetten

Als het programma met het menu gestart is en het pad niet gevonden worden kan, dan wordt er gevraagd om het juiste pad naar het bestand op te geven. Als de knownip-file niet bestaat kan deze aangemaakt worden met optie 9 in het menu.

### Maken van een nieuw configuratie bestand
Het maken van een nieuw configuratiebestand kan best ingewikkelt zijn aangezien je precies moet weten welke opties er zijn en welke waarde je die moet geven. Om dat probleem op te kunnen lossen heeft het menu de optie (optie 10) om een nieuw configuratiebestand te configureren. Er wordt dan een reeks vragen gesteld waardoor het configuratiebestand aan je wensen voldoet. 

Let op! Als er al een configuratiebestand staat in de map waar ook het programma staat is er een kans aanwezig dat deze overschreven wordt. 

### Output wegschrijven naar een bestand
Het programma heeft de mogelijkheid om alle, anders getoonde ouput, weg te schrijven naar de result.txt file. Als het bestand bestaat wordt de output aan het bestand toegevoegd, anders zal er een nieuw bestand aangemaakt worden. Deze functionaliteit is aan te roepen op slechts 1 manier:
1. Met de `-s` parameter

### Combineren van parameters
Het programma heeft veel opties en hierdoor dus veel parameter-combinaties. Vrijwel alle parameters kunnen met elkaar gecombineerd worden. Mocht een combinatie niet kloppen dan kiest het programma de meest logische combinatie. Hieronder staan een aatal voorbeeld combinaties en welke output ze geven:

Combinatie: `Logbrowser.py -g -l openvpn.log`</br>
Resultaat: start het programma met een menu en geeft de locatie van de logfile aan

Combinatie: `Logbrowser.py -m -p -d unsuccessful`</br>
Resultaat: Laat een top 5 dagen zien met de meest unsuccesvolle connecties, laat het aantal connecties zien die niet gemaakt zijn met het OpenVPN-protocol en laat zien welke manangement commando's gebruikt zijn

Combinatie: `Logbrowser.py -g -c configfile`</br>
Resultaat: Start het programma met het configuratiebestand (negeert de `-g` parameter)

Combinatie: `Logbrowser.py -g -m`</br>
Resultaat: Start het programma met een menu (negeert de `-m` parameter)

Combinatie: `Logbrowser.py -g -s`</br>
Resultaat: Start het programma met een menu en schrijft alle resultaten naar de result.txt file

Combinatie: `Logbrowser.py -t successful -t unsuccessful`
Resultaat: De top 10 functie wordt 1 keer aangeroepen met de waarde `unsuccessful`

### Overige opties
Naast alle eerder opgenoemde opties zijn er ook nog een paar opties die hierboven niet genoemd zijn. Het gaat hier om de volgende opties:
- Alle parameters laten zien die het programma gebruikt. Dit kan op 2 manieren:
1. Via optie 11 in het menu
2. Met de `-h` parameter

- Het sluiten van het programma kan, en is ook alleen nodig, via het menu. Dit is te doen met menu optie 12.

***

## Disclaimer
Het gebruik van het programma is op eigen risico. Ik, de ontwikkelaar, ben niet verantwoordelijk voor iedere vorm van schade die dit product eventueel zou kunnnen verrichten.

***

## Gebruikte bronnen
Om ervoor te kunnen zorgen dat alles werkt zijn de volgende bronnen gebruikt:
- https://martin-thoma.com/configuration-files-in-python
- https://docs.python.org/3/library/
- https://linuxhint.com/add_command_line_arguments_to_a_python_script
- https://docs.python.org/3/library/argparse.html
- https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/
- https://towardsdatascience.com/quick-python-tip-suppress-known-exception-without-try-except-a93ec34d3704
- https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/
- https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/
- https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python
- https://gist.github.com/shaunlebron/746476e6e7a4d698b373
