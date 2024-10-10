# This is an example program to show some of the functionality of the library
import json
import random

import client  # imports from client.py
import asyncio
import re
import anecdotesFetcher
import threading

token = "-21kqzBUT7L_5MWDI7e75K3B0DyHd5rFQt6y-ZJPxAylGtJdvL9J9FUBXjnO9hTE"
sessiontype = 'bot'
bot = client.Client(token, sessiontype)  # Initiates the client

anecdotesChannel = "01J9SYAG7CJ2B2DXK37ZKC0SA7"

mood = 1


def changeMood(change):
    global mood
    mood += change


def repeat_function():
    if mood < 1:
        changeMood(0.02)
    print(mood)
    threading.Timer(5, repeat_function).start()


greetings = ["Привет", "Здорова", "Здравия", "Приветствую", "Доброго времени суток", "Приветики"]
greeting_connectors = ["орлы", "молодёжь", "всем", "господа", "шпана", "борзята", "работяги", "заводчане", "ребятки"]
anecdoteStarters = ["Вот такой помню", "Есть такой", "Помню в армейке рассказывали", "Тёщин любимый", "Слушайте",
                    "Этот вообще как говорит молодёжь - бомба!", "Готовы?"]


def rand_of_seq(seq):
    return seq[random.randint(0, len(seq) - 1)]


async def onMessage(message):
    print(f'[{bot.fetchuser(message.author).username}]: {message.content}')  # Logs a message

    if message.channel == anecdotesChannel:
        msgContent = re.sub(r'[^\w]', '', message.content, flags=re.UNICODE).lower()
        if "расскажианекдот" in msgContent:
            if mood <= 0:
                await bot.sendmessage(message.channel,
                                      "Подустал я, " + rand_of_seq(greeting_connectors) + ", вздремну немного...")
            else:
                anecdote = anecdotesFetcher.fetchRandom()
                if anecdote is None:
                    await bot.sendmessage(message.channel, "Я устал, вздремну немного...")
                else:
                    changeMood(-0.25)
                    response = f"{rand_of_seq(anecdoteStarters)}. {anecdote}"
                    await bot.sendmessage(message.channel, response)


async def onMessageDelete(message):  # If a message is deleted, log it in the console with the message ID
    print(f'[{message["id"]}]: DELETED')


async def onLogin():
    print(f'Logged in as {bot.user.username}')
    await bot.sendmessage(anecdotesChannel, rand_of_seq(greetings) + ", " + rand_of_seq(greeting_connectors))


async def main():
    repeat_function()
    # bot.addEventListener("messagedelete", onMessageDelete)  # A listener for when a message is deleted
    bot.addEventListener("message", onMessage)  # A listener for when a message is sent
    bot.addEventListener("login", onLogin)  # A listener for when the bot comes online / logs in
    await bot.connect()


asyncio.run(main())
