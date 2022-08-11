# TO USE:
 SAVE FILES TO DESKTOP
Go To: 
Desktop/CryptoBot/bot1/api_keys.json
Desktop/Cryptobot/bot2/api_keys.json

## add your keys to the designated locations: 

{
  "exchange": {
    "name": "binanceus",
    "key" : "put your key here",
    "secret" : "put your secret here"
  }
}

## It should look like this:

{
  "exchange": {
    "name": "binanceus",
    "key" : "12345678901234567890",
    "secret" : "12345678901234567890"
  }
}

## save these files once finished

## open command line (CMD on windows, Terminal on Mac+Linux)
### for WINDOWS:
		cd Desktop\CryptoBot\
		docker-compose up
### for Mac+Linux:
		cd ~/Desktop/CryptoBot
		docker-compose up
