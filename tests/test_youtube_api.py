from os import path

from eyescomment.youtube_api import YoutubeApi


CURRENT_PATH = path.dirname(path.abspath(__file__))


def test_gen_channel_video():
    api_key = 'AIzaSyCx8Lhnb81d1pp9CbFE_mPL-ql6Hicoe2E'
    video_id = 'ZRIs-oN8HHY'
    video_columns = [
        'videoId', 'channelName', 'channelId', 'videoName', 'description', 'videoImage',
        'liveBroadcastContent', 'publishedAt', 'updateAt']
    yt_api = YoutubeApi(api_key=api_key)
    channel_videos = yt_api.gen_channel_video(
        channel_id='UC6FcYHEm7SO1jpu5TKjNXEA', max_result=50)
    for column in video_columns:
        assert column in list(channel_videos[video_id][0].keys())
    assert len(channel_videos) > 0


def test_gen_video_comment():
    api_key = 'AIzaSyCx8Lhnb81d1pp9CbFE_mPL-ql6Hicoe2E'
    video_id = 'ZRIs-oN8HHY'
    comment_columns = [
        'commentId', 'videoId', 'authorChannelId', 'author', 'text', 'likeCount', 'publishedAt']
    yt_api = YoutubeApi(api_key=api_key)
    video_comments = yt_api.gen_comment(video_id='ZRIs-oN8HHY', max_result=50)
    for column in comment_columns:
        assert column in list(video_comments[video_id][0].keys())
    assert len(video_comments) > 0
