############################################################
#Naam: Dave van der Leek (1777075)
#Klas:
#Programanaam: OVPNLogbrowser
#Beschrijving: Een programma om OpenVPN logfiles uit te lezen
#Versie:
versie = 0.1
############################################################

#Functies

#Functie die het menu laat zien
def dvdl_toon_menu():
    #Laat het menu zien:
    #Wat wilt u doen?
    #1. Top 10 IP's met de meeste unsuccesvolle verbindingen
    #2. Top 10 IP's met de meeste succesvolle verbindingen
    #3. Top 10 succesvolle verbindingen per adres
    #4. Top 10 unsuccesvolle verbindingen per adres
    #5. Top 5 dagen met veel succesvolle connecties
    #6. Top 5 Dagen met veel unsuccesvolle connecties
    #7. Laat aantal verbindingen zien die niet met OVPN gemaakt zijn
    #8. Laat gebruikte management commando's zien (gesorteerd op aantal)
    #9. Type een adres in en laat aantal connecties zien (en of ze gelukt zijn)
    #10. Laat alle nieuwe IP's zien
    #11. Maak een configfile aan
    #x12. Laat parameters zien
    #13. Sluit programma af
    #Maak uw keuze:
    print("Wat wilt u doen?\n1. Ik wil ...\n2. Ik wil...")

    #Vraag om input en sla deze op in een variabele
    choice = input("Maak uw keuze: ")
dvdl_toon_menu()