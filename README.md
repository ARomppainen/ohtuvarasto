# ohtuvarasto
Ohjelmistotuotanto-kurssin viikkojen [1](https://ohjelmistotuotanto-hy.github.io/tehtavat1), [2](https://ohjelmistotuotanto-hy.github.io/tehtavat2) ja [5](https://ohjelmistotuotanto-hy.github.io/tehtavat5) harjoituksia.

[![CI](https://github.com/ARomppainen/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/ARomppainen/ohtuvarasto/actions)

[![codecov](https://codecov.io/github/ARomppainen/ohtuvarasto/graph/badge.svg?token=AA00E4P1UE)](https://codecov.io/github/ARomppainen/ohtuvarasto)

## Hyödyllisiä komentoja

Web-käyttöliittymän käynnistäminen

`cd src && poetry run python app.py`

Web-käyttöliittymä käynnistyy osoitteeseen http://127.0.0.1:5000/

Testien suorittaminen ja testikattavuuden raportointi

`poetry run coverage run --branch -m pytest`

`coverage html`

Staattinen koodianalyysi

`poetry run pylint src`
