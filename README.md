# ohtuvarasto
Ohjelmistotuotanto-kurssin [viikon 1](https://ohjelmistotuotanto-hy.github.io/tehtavat1) harjoituksia

[![CI](https://github.com/ARomppainen/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/ARomppainen/ohtuvarasto/actions)

[![codecov](https://codecov.io/github/ARomppainen/ohtuvarasto/graph/badge.svg?token=AA00E4P1UE)](https://codecov.io/github/ARomppainen/ohtuvarasto)

## Hyödyllisiä komentoja

Testien suorittaminen ja testikattavuuden raportointi

`poetry run coverage run --branch -m pytest`

`coverage html`

Staattinen koodianalyysi

`poetry run pylint src`
