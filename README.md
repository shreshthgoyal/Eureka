
# AI Data Query Interface

This project aims to create an AI-powered query interface that allows users to efficiently access and understand client data stored in internal databases using a user-friendly chat interface.


## Run Locally

Clone the project

$ python3 -m venv venv
$ source venv/bin/activate
$ python -m pip install -r requirements.txt
$ sh entrypoint.sh     # For API : It will start at 8000 port.
$ streamlit run app.py # For UI : It will start at 8015 port.

or you can just start it up with docker

$ docker-compose build
$ docker-compose up  # The API will be live on port 3015





## API Reference

#### Get 200 OK Response

```
  GET /healthcheck
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get answer to the query

```
  POST /search
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `input`      | `string` | **Required**. Query For Entire Database |

```
  POST /message
```

#### Create a session for chat

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `document_title`      | `string` | **Required**. Document Title |

```
  POST /message
```

#### Get chat responses

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `session_id`      | `string` | **Required**. Session ID for chat|
| `query`      | `string` | **Required**. Query For Chat |



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`FIREWORKS_API_KEY`

`COHERE_API_KEY`
## Authors

- [@shreshthgoyal](https://www.github.com/shreshthgoyal)
- [@mounicasruthi](https://www.github.com/mounicasruthi)
- [@rish78](https://www.github.com/rish78)

