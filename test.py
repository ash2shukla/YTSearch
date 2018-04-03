from YTSearch import YTSearch


def simpleTasks(showInfo=False):
    channelId = 'UCIwqOzOcNFrtF8tNF0S40Yw'
    yt = YTSearch()
    print('Get Channel Videos')
    yt.channelId = channelId
    # if results are needed in a bunch
    yt.get_list("channel")
    # yt.results contains results for the last get_list query
    print('Get all at once')
    print(len(yt.results))
    if showInfo:
        print(yt.results)
    # if results are needed page by page (according to MAX_PAGE in config.py)
    print('Get page by page')
    channel_gen = yt.get_generator("channel")
    while True:
        try:
            inf = next(channel_gen)
            print(len(inf))
            if showInfo:
                print(inf)
        except StopIteration:
            break
    # if results are needed one by one till results are exhausted
    print('Get one by one')
    channel_gen = yt.get_onebyone("channel")
    while True:
        try:
            inf = next(channel_gen)
            print(len(inf))
            if showInfo:
                print(inf)
        except StopIteration:
            break

    print('****Get Videos related to a video****')
    # Create channel video generator
    channel_gen = yt.get_onebyone("channel")
    # Get first video from channel generator
    video_of_channel = next(channel_gen)
    if showInfo:
        print(video_of_channel)
    # Extract videoId from the video of channel
    videoId = video_of_channel[0]['id']['videoId']
    # Set videoId in yt
    yt.videoId = videoId
    if showInfo:
        print(yt.videoId)
    # if all videos related to the current videoId are needed
    # In case we want to change max_results for related videos then do
    yt.max_results = 10
    print('Get all related videos')
    related_videos = yt.get_list("video")
    print(len(related_videos))
    if showInfo:
        print(related_videos)
    print('Get all related videos page by page')
    video_gen = yt.get_generator("video")
    while True:
        try:
            pbp_related_videos = next(video_gen)
            print(len(pbp_related_videos))
            if showInfo:
                print(pbp_related_videos)
        except StopIteration:
            break
    # if results are needed one by one till results are exhausted
    print('Get all related videos one by one')
    video_gen = yt.get_onebyone("video")
    while True:
        try:
            obo_related_videos = next(video_gen)
            print(len(obo_related_videos))
            if showInfo:
                print(obo_related_videos)
        except StopIteration:
            break


def complexTasks(showInfo=False):
    """Comlex Tasks
    Fetch first 5 videos from channelId 'UCf3u_7F_-GNilFK_7dZhQzQ'
    for first 2 videos from that channel get 10 similar videos
    except that for the rest of the videos get 2 similar videos
    """
    yt = YTSearch('UCIwqOzOcNFrtF8tNF0S40Yw')
    yt.max_results = 5
    # Create generator for channel
    channel_gen = yt.get_generator("channel")
    # Get first max_page results (default 10 can be changed to any number <50)
    first_5 = next(channel_gen)
    print(len(first_5))
    if showInfo:
        print(first_5)
    first_2 = first_5[:2]
    for i in first_2:
        if showInfo:
            print(i)
        # extract videoId 
        yt.videoId = i['id']['videoId']
        # Create generator @ 10 for the videoId
        yt.max_results = 10
        video_gen = yt.get_generator("video")
        first_10 = next(video_gen)
        print(len(first_10))
        if showInfo:
            print(first_10)
    for i in first_5[2:]:
        if showInfo:
            print(i)
        yt.videoId = i['id']['videoId']
        # Create generator @ 1 for the videoId
        yt.max_results = 1
        video_gen = yt.get_generator("video")
        first_1 = next(video_gen)
        print(len(first_1))
        if showInfo:
            print(first_1)

# Invoke method with False to hide all retrieved information
# Methods will only print length of retrieved contents if invoked with False
simpleTasks(True)
complexTasks(True)
