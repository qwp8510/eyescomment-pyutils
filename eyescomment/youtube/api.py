from ..platform.api import RegionApi


class YoutubeVideo(RegionApi):
    """Videos of Youtube Channel from db"""

    def __init__(self, host, cache_path, filter_params={}):
        """
        Args:
            host (str): http url host.
            path (str): http url path.
            filter_params: filter params.
        """
        self.filter_params = filter_params
        super(YoutbeVideo, self).__init__(
            host=host, target_path='Youtube_videos', cache_path=cache_path)

    def __getitem__(self, idx):
        videos_detail = self.get(params=self.filter_params)
        return videos_detail[idx]


class Youtubechannel(RegionApi):
    """Youtube Channel from db"""

    def __init__(self, host, cache_path, filter_params={}):
        """
        Args:
            host (str): http url host.
            path (str): http url path.
            filter_params: filter params.
        """
        self.filter_params = filter_params
        super(Youtubechannel, self).__init__(
            host=host, target_path='Youtube_channels', cache_path=cache_path)

    def __getitem__(self, idx):
        channels_detail = self.get(params=self.filter_params)
        return channels_detail[idx]
