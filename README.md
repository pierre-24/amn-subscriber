# `amn-subscriber`

Un truc en *quick and dirty* pour stocker les inscriptions à l'infolettre.


```bash
# create virtualenv
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip3 install --upgrade -r requirements.txt

# init
export FLASK_APP=amn_subscriber
flask init
```

N'oubliez pas de créer un `settings.py`

```python
SECRET_KEY = '****'
PASSWORD ='****'
```
