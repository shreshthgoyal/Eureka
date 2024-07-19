# Woodpecker

## Install and Run

To run it locally

````
# In the project repository
$ python3 -m venv venv
$ source venv/bin/activate
$ python -m pip install -r requirements.txt
$ python -m spacy download en_core_web_sm
$ sh entrypoint.sh     # For API : It will start at 8000 port.
$ streamlit run app.py # For UI : It will start at 8015 port.

````


or you can just start it up with docker

````
$ docker-compose build
$ docker-compose up
````
It will start at 3015 port.

