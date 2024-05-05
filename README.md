Sovellus on kurssin esimerkkiaiheen mukainen keskustelusovellus ja sen ideana on näyttää keskustelualueita, joissa jokaisella alueella on jokin tietty aihe. Keskustelualueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen sovelluksen käyttäjä on joko peruskäyttäjä tai ylläpitäjä.

Sovellus on saatu valmiiksi ja kaikki alla listatut tavoitellut ominaisuudet on sisällytetty sovellukseen:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen sisällä ketjut ja viestien määrän ketjussa ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

Sovellusta voi testata seuraavasti:
1. Kloonaa tämä repositorio
2. Siirry sovelluksen juurikansioon ja luo sinne .env-tiedosto ja määritä sen sisältö alla olevan mukaisesti (käytettävä tietokanta on PostreSQL-tietokanta, joka on asennettu kurssin esimerkin mukaisesti):
  DATABASE_URL=<tietokannan-paikallinen-osoite>
  SECRET_KEY=<salainen-avain>
3. Luo ja aktivoi virtuaaliympäristö seuraavilla komennoilla:
- python3 -m venv venv
- source venv/bin/activate
3. Asenna requirements.txt -tiedoston mukaiset riippuvuudet komennolla pip install -r requirements.txt
4. Luo schema.sql -tiedostosta löytyvät sovelluksen vaatimat tietokantataulut komennolla psql < schema.sql
5. Käynnistä sovellus flask run -komennolla

Voit nyt luoda käyttäjätilejä sovellukseen ja aloittaa sovelluksen testaamisen. Testaamisen helpottamiseksi ensimmäisenä luotava käyttäjä saa automattisesti admin-oikeudet ja tämän jälkeen kaikki rekisteröityvät käyttäjät ovat normaaleja käyttäjiä, ja lisää admin oikeuksia voi antaa käyttäjille tietokannan puolella.