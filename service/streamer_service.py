from twitchAPI.twitch import Twitch
from dotenv import dotenv_values
from service.github_service import has_github_account

from service.twitter_service import has_twitter_account

config = dotenv_values(".env")
twitch = Twitch(config['CLIENT_ID'], config['CLIENT_SECRET'])

def get_streamers():

    games = twitch.get_games(names=['Software and Game Development'])
    game_id = games['data'][0]['id']
    streams = twitch.get_streams(language="pt", game_id=game_id)

    streams_model = []
    for s in streams['data']:
        stream = {}
        stream['id'] = s['id']
        stream['user_id'] = s['user_id']
        stream['user_name'] = s['user_name']
        stream['user_login'] = s['user_login']
        stream['title'] = s['title']
        stream['viewer_count'] = s['viewer_count']
        stream['started_at'] = s['started_at']
        stream['thumbnail_url'] = s['thumbnail_url']

        streamer = get_streamer(s['user_id'])
        stream['profile_image_url'] = streamer['profile_image_url']
        stream['description'] = streamer['description']
        stream['has_twitter'] = has_twitter_account(s['user_login'])
        stream['has_github'] = has_github_account(s['user_login'])
        streams_model.append(stream)

    return streams_model

def get_streamer(id):
    return twitch.get_users(user_ids=[id])['data'][0]
    