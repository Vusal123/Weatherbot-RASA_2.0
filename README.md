# Weather Chatbot with Rasa 2.0

## Introduction

This is a chatbot that can help you tell the weather for any city and date which can be integrated to different platforms where messaging functionality is available. In this project example of telegram integration ia vailable. 


## Weather data

The weather data format chosen here is defined by WeatherApi (https://www.weatherapi.com/), which provides weather data freely for developers. On free version of the API provides weather condition for three days.


## Conversation Flow

The conversation is initiated by the end-user. User has several options to start the conversation, which are:
- Greeting
- Weather request with city name and date entities
- Weather request with city name entity
- Weather request with date entity
- Weather request without any entity

The conversation can be terminated/restarted by:
- Telling goodbye in the middle of any conversation flow path
- Expression of not wanting weather condition during any conversation flow path

On current version, chatbot can handle side talks during the conversations which are:
- Bot challenge (user challenges the bot by asking if it is a bot or human)
- Out of scope (user asks questions or reqeuests something that are not related to the weather condition)
- Appreciation (user thanks bot for providing weather condition)


## Implementation

In Rasa, the slots can be used for passing information to and back between Rasa and external actions. Two slots are required for this chatbot:
- City
  - During conversation, city entity is extracted by implementation of lookup table which is a list of city names used to generate case-insensitive regular expression patterns
- Date
  - For extracting dates, DucklingEntityExtractor was used, which lets you extract common entities like dates, amount of money, distances and others in a number of languages. Duckling allows to recognize dates, numbers, distances and other structured entities and normalizes them. For more information on Duckling, check https://github.com/facebook/duckling

External actions are user defined functions written in python. Five actions were defined for this project:
- weather_details_form : keeps requesting input for the weather form until the form is filled. Weather form consist of two entities which are city and date
- action_submit: to verify the submittion of required slots
- action_weather_api: to call weather function, and provide the weather condition by submitting city name and date to the weather api
- action_slot_reset: to reset slot inputs when rewuired
- action_chat_restart: to restart the chat based on requirement

The user intents, stories and rules are used for training the NLP model. These intent examples cover different ways of asking questions, and explaining to the model how to find the values for the required slots and what is the intent the user has. The stories and rules contain the conversation flows that will submit filled slots to provide weather condition or stop any conversation and force a different path. 


## Installation
 
Before installation make sure that you have correct Python version as Rasa 2.X.X requires Python 3.6, 3.7 or 3.8.

### Install Rasa

Below are the simple steps for creating a virtual environment on Windows and installing Rasa Open Source 2.0. If PATH and PATHEXT variables are already configured for your Python installation:

```
c:\>python -m venv c:\path\to\venv
```
To activate the virtual environment:
```
C:\> .\venv\Scripts\activate.bat
```
To install Rasa Open Source:
```
pip install rasa 
```

In case of issue, please refer to Rasa Open Source installation pages: 
https://rasa.com/docs/rasa/installation/

### Creating and initialising a new project:

```
mkdir rasa_chatbot
cd rasa_chatbot
rasa init --no-prompt
```
This will create a new directory, under which rasa creates all necessary directories and files.

Replace all files in the rasa_chatbot directory with the files in the project.

## Train the model

Train the model with command 

```
rasa train
```

There are additional actions that need to be started before starting the bot evaluation. These are in ```actions.py``` and ```weather.py``` files. Run below given command on separate terminal after virtual environment activation.

```
rasa run actions
```

For being able to use DucklingEntityExtractor component you need to run a duckling server. The easies option is to spin up a docker container. First you need to install docker on your computer from this link: https://www.docker.com/products/docker-desktop . After installation, run below given command on separate terminal.
```
docker run -p 8000:8000 rasa/duckling
```

## Activating Weather API

Currently my temporary API key is given in api_key part of the Weather function in weather.py file. Before starting the chatbot, make sure that you have valid API key. First, you need to sign up in https://www.weatherapi.com/ and then get your API key.

```python
def Weather(city,time)
  ...
  api_key = "insert your key here in weather.py file"
  ...
```

## Run the bot in command prompt

Start the discussion with weather chatbot:

```
rasa shell
```

To stop and restart the chatbot run below given commands respectively:
```
/stop
/restart
```

# Run the bot on Telegram
To run the bot on Telegram you need to update below given part on ```credentials.yml```. Currently, the credentials in the file is the ones that I got for my bot. Follow the instructions in https://rasa.com/docs/rasa/connectors/telegram/ to get credentials for ```access_token``` and ```verify``` part.

```yaml
telegram:
  access_token: "1822340776:AAEGnS3t6VhKB3bfRxJfJYQTiU7J-O5TT7o"
  verify: "weather_ml_project_demo_bot"
  webhook_url: "https://ee57e4dc85e7.ngrok.io/webhooks/telegram/webhook"
```

For testing purposes, you can use ngrok for updating ```https://ee57e4dc85e7.ngrok.io``` part of the ```webhook_url``` credential. 

Download ngrok and run on your computer without any installation requirements. For downloading follow https://ngrok.com/download . 

First you need to run the rasa model, in venv by:

```
rasa run
```

Then fire up ngrok and run

```
ngrok http 5005
```
By that you will get details of the new ngrok session. Take https address in the session and update you telegram ```webhook_url```  credential in ```credentials.yml``` file.

Terminate previous rasa run by ```CTRL + C``` and run again with above given command. Now, you are good to test your bot on Telegram.
