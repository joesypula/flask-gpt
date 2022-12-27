# flask-gpt
Prototype ChatGPT clone written in flask

Install requirements
```commandline
pip3 install -r requirements.txt 
```

Install gunicorn

```commandline
pip3 install gunicorn
```

Create `config.py` and add OpenAI API Key

```commandline
API_KEY = "sk-xxxxxx"
```

Run server using `flask-gpt-uWSGI-conf.py`

```commandline
gunicorn -c flask-gpt-uWSGI-conf.py app:app
```