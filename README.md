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
sqlite3 database.db < init.sql
flask run


Testitulokset 

Etusivu + 10 sivun siirtymä + yhden reseptin avaaminen. Hitainta vaikuttaa olevan yhden reseptin ja siihen liittyvien arvosanojen ja kommenttien lataaminen.

 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
elapsed time: 0.06 s
127.0.0.1 - - [27/Apr/2025 13:37:59] "GET / HTTP/1.1" 200 -
elapsed time: 0.05 s
127.0.0.1 - - [27/Apr/2025 13:38:08] "GET /2 HTTP/1.1" 200 -
elapsed time: 0.06 s
127.0.0.1 - - [27/Apr/2025 13:38:09] "GET /3 HTTP/1.1" 200 -
elapsed time: 0.05 s
127.0.0.1 - - [27/Apr/2025 13:38:10] "GET /4 HTTP/1.1" 200 -
elapsed time: 0.05 s
127.0.0.1 - - [27/Apr/2025 13:38:10] "GET /5 HTTP/1.1" 200 -
elapsed time: 0.04 s
127.0.0.1 - - [27/Apr/2025 13:38:11] "GET /6 HTTP/1.1" 200 -
elapsed time: 0.04 s
127.0.0.1 - - [27/Apr/2025 13:38:12] "GET /7 HTTP/1.1" 200 -
elapsed time: 0.05 s
127.0.0.1 - - [27/Apr/2025 13:38:13] "GET /8 HTTP/1.1" 200 -
elapsed time: 0.04 s
127.0.0.1 - - [27/Apr/2025 13:38:14] "GET /9 HTTP/1.1" 200 -
elapsed time: 0.05 s
127.0.0.1 - - [27/Apr/2025 13:38:15] "GET /10 HTTP/1.1" 200 -
DEBUG item: <sqlite3.Row object at 0x7f8b08b9a730>
<sqlite3.Row object at 0x7f8b08b9a730>
elapsed time: 1.87 s
127.0.0.1 - - [27/Apr/2025 13:38:22] "GET /item/999910 HTTP/1.1" 200 –


Indeksien luomisen jälkeen yksittäisen reseptin ja siihen liittyvien arvosanojen ja kommenttien lataaminen on selkeästi nopeutunut. 
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
elapsed time: 0.03 s
127.0.0.1 - - [27/Apr/2025 13:49:12] "GET / HTTP/1.1" 200 -
elapsed time: 0.04 s
127.0.0.1 - - [27/Apr/2025 13:49:20] "GET /2 HTTP/1.1" 200 -
elapsed time: 0.03 s
127.0.0.1 - - [27/Apr/2025 13:49:21] "GET /3 HTTP/1.1" 200 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2025 13:49:22] "GET /4 HTTP/1.1" 200 -
elapsed time: 0.03 s
127.0.0.1 - - [27/Apr/2025 13:49:23] "GET /5 HTTP/1.1" 200 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2025 13:49:24] "GET /6 HTTP/1.1" 200 -
DEBUG item: <sqlite3.Row object at 0x7f7b1029a5d0>
<sqlite3.Row object at 0x7f7b1029a5d0>
elapsed time: 0.14 s
127.0.0.1 - - [27/Apr/2025 13:49:27] "GET /item/999946 HTTP/1.1" 200 -
![image](https://github.com/user-attachments/assets/cb101d36-1274-4446-9b86-2c1be3cddafd)

