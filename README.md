# ruokareseptit

Status:
Tehty:
* Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä voidaan kirjoittaa tarvittavat ainekset ja valmistusohje.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt reseptit.
* Käyttäjä pystyy etsimään reseptejä hakusanalla.
* Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
* Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen).
* Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.


Asennusohje
Lataa koodit hakemistoon
aja terminaalissa ko hakemistossa
python3 -m venv venv
source venv/bin/activate
sqlite3 database.db < schema.sql
flask run


Testitulokset 

