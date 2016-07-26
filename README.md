# PokemonGo Map with Slack![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)

This is my personal extension on the PoGoMDev map. It integrates the map with slack and will send notifications of the selected pokemon to slack.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## How to setup the main pogo map

For instructions on how to setup and run the tool, please refer to the project [wiki](https://github.com/AHAAAAAAA/PokemonGo-Map/wiki), or the [video guide](https://www.youtube.com/watch?v=RJKAulPCkRI).

## How to setup for slack integration

In addition to the main setup you will need a few extra parameters:  
-sw (this is your slack webhook, enter like this: "/services/YOURWEBHOOKADDRESS/", this one is required)  
-r (set the rarity level of pokemon it should send to slack. You can change the rarity of pokemon in pokedata.csv)  
-pi (by default it will show a pokeball emoji in slack. If you want to display the corresponding pokemon emoji instead, use -pi ":")  


In order to get the pokemon-emojis working you will need to ad them to the emojis list in slack. You can the the emojis here:  
https://github.com/Templarian/slack-emoji-pokemon  
if you use the emojis with pokemon- in front of the pokemon name you should use the parameter -pi ":pokemon-". Otherwise you should use -pi ":".

## Warnings

Using this software is against the ToS of the game. You can get banned, use this tool at your own risk.
