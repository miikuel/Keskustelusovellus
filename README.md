Toteutettava sovellus on kurssin esimerkkiaiheen mukainen keskustelusovellus. Sovelluksen ideana on näyttää keskustelualueita, joissa jokaisella alueella on jokin tietty aihe. Keskustelualueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen sovelluksen käyttäjä on joko peruskäyttäjä tai ylläpitäjä.

Tavoitteena on sisällyttää sovellukseen alla listatut kurssimateriaalin mukaiset ominaisuudet (suluissa ominaisuuden tila per 7.4.2024).

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. (valmis)
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen sisällä ketjut ja viestien määrän ketjussa ja viimeksi lähetetyn viestin ajankohdan. (valmis)
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön. (valmis)
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun. (valmis)
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin. (puuttuu)
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana. (valmis)
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita. (osittain valmis / alueita ei voi poistaa)
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle. (puuttuu)

Sovellusta voi testata seuraavasti:
1. Kloonaa tämä repositorio
2. Siirry sovelluksen juurikansioon ja luo sinne .env-tiedosto ja määritä sen sisältö alla olevan mukaisesti (käytettävä tietokanta on PostreSQL-tietokanta, joka on asennettu kurssin esimerkin mukaisesti):
  DATABASE_URL=<tietokannan-paikallinen-osoite>
  SECRET_KEY=<salainen-avain>
3. Asenna requirements.txt -tiedoston mukaiset riippuvuudet komennolla pip install -r requirements.txt
4. Luo schema.sql -tiedostosta löytyvät sovelluksen vaatimat tietokantataulut komennolla psql < schema.sql
5. Käynnistä sovellus flask run -komennolla