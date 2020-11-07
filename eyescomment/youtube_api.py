import json
import logging
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError


logger = logging.getLogger(__name__)
API_KEY = [
    'AIzaSyCGokxpLFG-7M259tOp7-q7fsqYKqvmQNE',
    'AIzaSyD08pO1kEyZ1t7RXQuAyUFlOTyJO68FZYg',
    'AIzaSyBOWzgpes4ryDn0BHthJjj7vcGr1VlpndA',
    'AIzaSyBaFMdTVrz6pJhSosmWNMaailKVWElkjIw',
    'AIzaSyCx8Lhnb81d1pp9CbFE_mPL-ql6Hicoe2E'
]


class YoutubeApi():
    YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
    YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
    YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v='

    def __init__(self, api_key):
        self.api_key = api_key

    def update_param_api_key(self, url, param):
        logger.warning('Youtube.Api.update param api key')

        def check_http():
            youtube_url = url + '?' + urlencode(param)
            try:
                return urlopen(youtube_url)
            except HTTPError as e:
                logger.error(
                    'update_param_api_key fail {} HTTPEroor: {}'.format(
                        youtube_url, e))
            except Exception as e:
                logger.error(
                    'update_param_api_key fail Exception {}'.format(e))

        for key in API_KEY:
            param.update({'key': key})
            if check_http():
                return param

    def get_url_data(self, url, param):
        content = '{}'
        try:
            youtube_url = url + '?' + urlencode(param)
            with urlopen(youtube_url) as f:
                data = f.read()
                f.close()
            content = data.decode("utf-8")
        except HTTPError as e:
            param = self.update_param_api_key(url, param)
            if param:
                return self.get_url_data(url, param)
            logger.error(
                'Youtube.Api.get_url_data {} HTTPError fail: {}'.format(
                    youtube_url, e))
        except Exception as e:
            logger.error(
                'Youtube.Api.get_url_data fail Exception {}'.format(e))
        return json.loads(content)

    def load_comment_replies(self, item):
        if 'replies' in item.keys():
            for reply in item['replies']['comments']:
                self.comment_detail.update({
                    'replyAuthor': reply['snippet']['authorDisplayName'],
                    'replyText': reply["snippet"]["textDisplay"]})

    def _load_comment(self, data):
        for item in data.get("items", {}):
            try:
                comment = item["snippet"]["topLevelComment"]
                detail = {
                    'commentId': comment["id"],
                    'videoId': item["snippet"]['videoId'],
                    'authorChannelId': comment["snippet"]['authorChannelId']['value'],
                    'author': comment["snippet"]["authorDisplayName"],
                    'text': comment["snippet"]["textDisplay"],
                    'likeCount': comment["snippet"]["likeCount"],
                    'publishedAt': comment["snippet"]["publishedAt"],
                    'updatedAt': comment["snippet"]["updatedAt"],
                    'replyCount': item['snippet']['totalReplyCount']}
                logger.info(
                    'YoutubeApi.load_comment loading {} comment: {}'.format(
                        item["snippet"]['videoId'], detail))
                self.comment_detail[item["snippet"]['videoId']].append(detail)
            # self.load_comment_replies(item)
            except Exception as e:
                logger.error("load_comment fail: {}".format(e))

    def gen_comment_by_page(self, params, content):
        nextPageToken = content.get('nextPageToken')
        try:
            while nextPageToken:
                params.update({'pageToken': nextPageToken})
                content = self.get_url_data(self.YOUTUBE_COMMENT_URL, params)
                self._load_comment(content)
                nextPageToken = content.get('nextPageToken')
        except KeyboardInterrupt:
            logger.warning("User Aborted the Operation")
        except Exception as e:
            logger.error("gen_comment_by_page fail: {}".format(e))

    def gen_comment(self, video_id=None, max_result=1):
        self.comment_detail = defaultdict(list)
        params = {
            'part': "snippet,replies",
            'maxResults': max_result,
            'videoId': video_id,
            'textFormat': 'plainText',
            'key': self.api_key}
        content = self.get_url_data(self.YOUTUBE_COMMENT_URL, params)
        self._load_comment(content)
        self.gen_comment_by_page(params, content)
        return self.comment_detail

    def _load_channel_video(self, data):
        for result in data.get('items', {}):
            try:
                if result["id"]["kind"] == "youtube#video":
                    snippet = result['snippet']
                    detail = {
                        'videoId': result['id']['videoId'],
                        'channelName': snippet['channelTitle'],
                        'channelId': snippet['channelId'],
                        'videoName': snippet['title'],
                        'description': snippet['description'],
                        'videoImage': snippet['thumbnails']['default']['url'],
                        'liveBroadcastContent': snippet['liveBroadcastContent'],
                        'publishedAt': snippet['publishedAt'],
                        'updateAt': datetime.now().replace(microsecond=0).isoformat()}
                    self.channel_video_detail[result['id']['videoId']].append(detail)
            except Exception as e:
                logger.error("load_comment fail: {}".format(e))

    def gen_video_by_page(self, params, content):
        try:
            nextPageToken = content.get('nextPageToken')
            while nextPageToken:
                params.update({'pageToken': nextPageToken})
                content = self.get_url_data(self.YOUTUBE_SEARCH_URL, params)
                self._load_channel_video(content)
                nextPageToken = content.get('nextPageToken')
        except KeyboardInterrupt:
            logger.warning("User Aborted the Operation")
        except Exception as e:
            logger.error("gen_video_by_page fail: {}".format(e))

    def gen_channel_video(self, channel_id, max_result=1):
        self.channel_video_detail = defaultdict(list)
        params = {
            'part': 'id,snippet',
            'channelId': channel_id,
            'maxResults': max_result,
            'key': self.api_key}
        content = self.get_url_data(self.YOUTUBE_SEARCH_URL, params)
        self._load_channel_video(content)
        self.gen_video_by_page(params, content)
        logger.info('gen_channel_video: {}'.format(self.channel_video_detail))
        return self.channel_video_detail
