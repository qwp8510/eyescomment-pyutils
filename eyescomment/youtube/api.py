from ..platform.api import RegionApi


class YoutubeVideo(RegionApi):
    """Videos of Youtube Channel from db"""

    def __init__(self, host, cache_path, filter_params={}):
        """
        Args:
            host (str): http url host.
            path (str): http url path.
            filter_params: http filter params.
        """
        self.filter_params = filter_params
        super(YoutubeVideo, self).__init__(
            host=host, target_path='Youtube_videos', cache_path=cache_path)
        self.videos_detail = self.get(params=self.filter_params)

    def push(self, data):
        super(YoutubeVideo, self).push(data=data)

    def __len__(self):
        return len(self.videos_detail)

    def __getitem__(self, idx):
        return self.videos_detail[idx]


class YoutubeChannel(RegionApi):
    """Youtube Channel from db"""

    def __init__(self, host, cache_path, filter_params={}):
        """
        Args:
            host (str): http url host.
            path (str): http url path.
            filter_params: http filter params.
        """
        self.filter_params = filter_params
        super(YoutubeChannel, self).__init__(
            host=host, target_path='Youtube_channels', cache_path=cache_path)
        self.channels_detail = self.get(params=self.filter_params)

    def push(self, data):
        super(YoutubeChannel, self).push(data=data)

    def __len__(self):
        return len(self.channels_detail)

    def __getitem__(self, idx):
        return self.channels_detail[idx]
