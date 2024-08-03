# `amn-subscriber`

Un truc en *quick and dirty* pour stocker les inscriptions à l'infolettre.

```bash
# create virtualenv
python3 -m venv venv
source venv/bin/activate

# install dependencies
make install

# init
make init
```

N'oubliez pas de créer un `settings.py` pour ajuster les valeurs par défaut:

```python
SECRET_KEY = '****'
PASSWORD ='****'
```
