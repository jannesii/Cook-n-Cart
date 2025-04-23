# Cook and Cart

**Cook and Cart** on Python + Qt/PySide6 ‑teknologioilla toteutettu resepti‑ ja ostoslistasovellus, joka toimii sekä työpöydällä että Android‑laitteissa. Sovellus auttaa tallentamaan reseptejä, hallitsemaan tuotteita ja suunnittelemaan ostokset – kustannukset huomioiden.

---

## Sisältö

- [Ominaisuudet](#ominaisuudet)
- [Rakenne](#rakenne)
- [Vaatimukset](#vaatimukset)
- [Käyttöönotto työpöydällä](#käyttöönotto-työpöydällä)
- [Android‑APK:n rakentaminen](#android-apkn-rakentaminen)
- [Konfigurointi](#konfigurointi)
- [Contributing](#contributing)
- [Lisenssi](#lisenssi)


---

## Ominaisuudet

|              |                             |
|--------------|-----------------------------|
| 🗂️ **Tuotteet** | Lisää, muokkaa ja poista tuotteita (nimi, yksikkö, hinta, kategoria). |
| 📝 **Reseptit** | Luo reseptejä, lisää ohjeet, tagit ja ainesosat tuotteista. |
| 🛒 **Ostoslistat** | Rakenna listoja resepteistä ja tuotteista, seuraa ostosten hintaa ja merkitse tuotteet ostetuiksi. |
| 📊 **Kustannuslaskelma** | Näe ostoslistan kokonaishinta ja ostettujen tuotteiden osuus. |
| 🔎 **Haku & suodatus** | Hae tuotteita ja reseptejä, suodata tageilla. |
| ☁️ **QML‑pohjaiset komponentit** | Mobiiliystävällinen UI QML‑listoilla ja ‑dialogeilla. |
| 📱 **Android‑tuki** | Ristikäännetty .apk, joka sisältää PySide6‑kirjastot ja Python‑tulkin. |
| 🛠️ **Virheenkäsittely** | Poikkeukset logitetaan SQLite‑kannassa *error_logs* ja näytetään toast‑viesteinä. |

---

## Rakenne

```
├── main.py                    # Sovelluksen käynnistyspiste
├── views_*                    # Käyttöliittymän sivut (Qt Widgets + QML)
├── widgets_*                  # Uudelleenkäytettäviä UI‑komponentteja
├── root_controllers.py        # Sovelluslogiikka (Controller‑kerros)
├── root_repositories.py       # Tietokantatoiminnot (Repository‑kerros)
├── root_models.py             # Dataclass‑mallit (Model‑kerros)
├── root_database.py           # SQLite‑yhteys ja skeeman luonti
├── error_handler.py           # Virheenkäsittely & toast‑ilmoitukset
├── utils/
│   ├── cook_and_cart.db       # SQLite‑tietokanta
│   └── config.json            # Käyttäjäkohtaiset asetukset
├── build/                     # Android build ‑skriptit ja riippuvuudet
│   ├── requirements.txt
│   ├── build_guide.txt        # Askelen‑askeleelta ohje (teksti)
│   └── setup-pyside6-android.sh
├── apkBuild.sh                # Yhden komennon .apk‑rakennus
└── whl/                       # Android‑yhteensopivat PySide6/Shiboken‑pyörät
```

---

## Vaatimukset

| Kehitysympäristö | Versio / työkalu |
|------------------|------------------|
| Python           | 3.11 (suositeltu) |
| Qt/PySide6       | 6.8.0.2 |
| pip + virtualenv | ^23 |
| SQLite           | 3.x |
| **Android build** | |
| Android SDK      | 34+ |
| Android NDK      | r26c (automaattisesti ladattava) |
| Java / JDK       | 17 |
| Buildozer        | 1.5+|
| python‑for‑android | 2024.x |

---

## Käyttöönotto työpöydällä

```bash
# 1. Kloonaa repo
$ git clone https://github.com/jannesii/Cook-n-Cart
$ cd cook-and-cart

# 2. Luo virtuaaliympäristö ja asenna riippuvuudet
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

# 3. Käynnistä sovellus
$ python main.py
```

> **Huom!** Ensimmäisellä ajokerralla `root_database.py` luo tietokantatiedoston *utils/cook_and_cart.db* ja alustus‑SQL:n.

---

## Android-APK:n rakentaminen

- Ohjeet: build/build_guide.txt

---

## Konfigurointi

- **Teemat & värit** sijaitsevat `main.py` → `default_styles` ‑muuttujassa (Qt QSS). Voit muokata värejä sieltä tai lisätä oman `.qss`‑tiedoston.

---

## Contributing

1. Forkkaa projekti ja luo uusi branch: `git checkout -b feature/oma-ominaisuus`  
2. Tee muutokset ja kirjaa selkeät commit‑viestit.  
3. Aja **flake8** / **black** sekä mahdolliset unit‑testit (tul tulossa).  
4. Lähetä pull request.

> Kaikki apu — bugiraportit, ominaisuuspyynnöt, dokumentointiparannukset — on tervetulleita!

---

## Lisenssi

Tämä projekti on lisensoitu **MIT‑lisenssillä**. Katso `LICENSE`‑tiedosto lisätietoja.

---

> © 2025 Cook and Cart ‑tiimi.  Rakennettu Qt/PySide6‑ ja Python‑rakkaudella ♥︎

