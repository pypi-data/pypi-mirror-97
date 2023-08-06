![](https://github.com/navikt/dataverk-gsm/workflows/Unittests/badge.svg)
![](https://github.com/navikt/dataverk-gsm/workflows/Release/badge.svg)
![](https://badge.fury.io/py/dataverk-gsm.svg)

# Dataverk GSM

Bibliotek med api mot google secret manager for 

### Installasjon

#### Master branch versjon
```
git clone https://github.com/navikt/dataverk-gsm.git
cd dataverk-gsm
pip install .
```

#### Siste release
```
pip install dataverk-gsm
```

## Eksempler på bruk
````python
from dataverk_gsm import api as gsm_api

# Hent hemmeligheter og sett de som miljøvariabler
gsm_api.set_secrets_as_envs()
````

## For NAV-ansatte
Interne henvendelser kan sendes via Slack i kanalen #dataverk
