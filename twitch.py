from datetime import datetime

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.pubsub import PubSub
import asyncio
import logging
import pygame

from main import generate_sound_effect
from secrets import CLIENT_ID, CLIENT_SECRET

# Replace these values with your client_id and client_secret
USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS]  # Scope for channel point redemption
TARGET_CHANNEL_ID = '38606166'

# Set up logging
logging.basicConfig(level=logging.INFO)


async def on_channel_point_redemption(uuid: str, data: dict) -> None:
    message = data.get('data').get('redemption').get('user_input')
    event = data.get('data').get('redemption').get('reward').get('title')

    if event == 'Make Sound':
        filename = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp3'
        generate_sound_effect(message, filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()


async def listen_to_redemptions():
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)

    # Authenticate the user and get the token
    token, refresh_token = await auth.authenticate()

    # Set the token
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # Create PubSub listener
    pubsub = PubSub(twitch)
    pubsub.start()

    # Hook up the PubSub listener for channel points redemptions
    uuid = await pubsub.listen_channel_points(TARGET_CHANNEL_ID, on_channel_point_redemption)

    # Keep it alive
    input('Press ENTER to exit...\n')
    await pubsub.unlisten(uuid)
    pubsub.stop()
    await twitch.close()


if __name__ == '__main__':
    pygame.mixer.init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen_to_redemptions())
