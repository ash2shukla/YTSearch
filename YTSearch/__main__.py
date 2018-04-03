from requests import get
from json import loads
from math import ceil
from .config import API_KEY, MAX_RESULTS, MAX_PAGE
from itertools import count


class YTSearch:
    def __init__(self, channelId='',
                 max_results=MAX_RESULTS,
                 max_page=MAX_PAGE):
        self.channelId = channelId
        self.videoId = ''
        self.max_page = max_page
        self.max_results = max_results
        self.results = []
        self.related_videos = 0
        self.channel_videos = 0

    def get_channel_url(self, page_token=''):
        """returns URL corresponding to config and page_token for a channel"""
        CHANNEL_URL = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={self.channelId}&part=snippet,id&type=video&order=date&maxResults={self.max_page}&pageToken={page_token}'
        return CHANNEL_URL

    def get_video_url(self, page_token=''):
        """ returns URL corresponding to config and page_token for a video"""
        VIDEO_URL = f'https://www.googleapis.com/youtube/v3/search?part=snippet&relatedToVideoId={self.videoId}&type=video&key={API_KEY}&pageToken={page_token}&order=date&maxResults={self.max_page}'
        return VIDEO_URL

    def get_list(self, _type="channel"):
        """returns a list containing all videos in a channel
        _type -- video for getting similar videos for self.videoId 
        """
        self.results = []
        page_token = ''
        if _type == "channel":
            info = loads(get(self.get_channel_url()).text)
        elif _type == "video":
            info = loads(get(self.get_video_url()).text)
        page_info = info.get('pageInfo')
        total_results = page_info.get('totalResults')
        if _type == "channel":
            self.channel_videos = total_results
        elif _type == "video":
            self.related_videos = total_results
        required_results = min(total_results, self.max_results)
        required_pages = required_results / self.max_page

        # To show progress
        total_count = ceil(required_pages)

        full_pages = int(required_pages)
        items = info.get('items')
        if items is not None:
            # in case max_results was less than length of a page then it will
            # trim the result to max_results length
            self.results += items[:self.max_results]
            print('\rProgress =',(1 / total_count)*100,'%               ',end='\r')
        if full_pages == 0:
            return self.results
        else:
            results_in_last_page = required_results % self.max_page
            for i in range(1, full_pages):
                page_token = info.get('nextPageToken')
                if _type == "channel":
                    next_page_url = self.get_channel_url(page_token)
                elif _type == "video":
                    next_page_url = self.get_video_url(page_token)
                info = loads(get(next_page_url).text)
                items = info.get('items')
                print('\rProgress =',((i + 1) / total_count)*100,'%               ',end='\r')
                if items is not None:
                    self.results += items
            if results_in_last_page != 0:
                self.max_page = results_in_last_page
                if _type == "channel":
                    info = loads(get(self.get_channel_url(page_token)).text)
                elif _type == "video":
                    info = loads(get(self.get_video_url(page_token)).text)
                items = info.get('items')
                if items is not None:
                    self.results += items
                print('\rProgress = 100 %               ',end='\n\n')
            return self.results

    def get_generator(self, _type="channel"):
        """returns a generator for results of each page
        _type -- video for getting similar videos for self.videoId
        """
        page_token = ''
        self.max_page = MAX_PAGE
        if _type == "channel":
            info = loads(get(self.get_channel_url()).text)
        elif _type == "video":
            info = loads(get(self.get_video_url()).text)
        page_info = info.get('pageInfo')
        total_results = page_info.get('totalResults')
        if _type == "channel":
            self.channel_videos = total_results
        elif _type == "video":
            self.related_videos = total_results
        required_results = min(total_results, self.max_results)
        required_pages = required_results / self.max_page

        # To show progress
        total_count = ceil(required_pages)

        full_pages = int(required_pages)
        items = info.get('items')
        # in case max_results was less than length of a page then it will
        # trim the result to max_results length 
        if isinstance(items, list):
            yield items[:self.max_results]
        else:
            yield []
        results_in_last_page = required_results % self.max_page
        for i in range(1, full_pages):
            page_token = info.get('nextPageToken')
            if _type == "channel":
                next_page_url = self.get_channel_url(page_token)
            elif _type == "video":
                next_page_url = self.get_video_url(page_token)
            info = loads(get(next_page_url).text)
            yield info.get('items')
        if not (results_in_last_page== 0 or full_pages == 0):
            # Using DeMorgans for results_in_lst_page!=0 and full_pages!=0
            self.max_page = results_in_last_page
            if _type == "channel":
                info = loads(get(self.get_channel_url(page_token)).text)
            elif _type == "video":
                info = loads(get(self.get_video_url(page_token)).text)
            yield info.get('items')

    def get_onebyone(self, _type="channel"):
        """returns videos one by one
        _type -- video for getting similar videos for self.videoId

        NOTE- Mind that it might seem this method alone is enough for all tasks
        but it sends unique GET for all requests
        Usage of this method should be avoided if more than one result is
        required
        """
        counter = count()
        self.max_page = 1
        page_token = ''
        while page_token is not None:
            if _type == "channel":
                url = self.get_channel_url(page_token)
            elif _type == "video":
                url = self.get_video_url(page_token)
            info = loads(get(url).text)
            page_info = info.get('pageInfo')
            total_results = page_info.get('totalResults')
            if _type == "channel":
                self.channel_videos = total_results
            elif _type == "video":
                self.related_videos = total_results
            page_token = info.get('nextPageToken')
            if next(counter) == self.max_results:
                raise StopIteration
            yield info.get('items')
