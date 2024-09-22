# AIzaSyBRPjYEDRZl2BwEwWOiLdj-QDyGcA0gTv0

from googleapiclient.discovery import build
import datetime

API_KEY = 'AIzaSyBRPjYEDRZl2BwEwWOiLdj-QDyGcA0gTv0'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_n_days(n: int) -> str:
    '''Gets n as an int and returns the date - n as str'''
    return (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=n)).replace(microsecond=0).isoformat()

def get_video_ids(max_resutl: int, days: str) -> list:
    '''Returns max_results number of videos in the past n days'''
    search_request = youtube.search().list(
        part="id",
        publishedAfter=days,
        maxResults=max_resutl,
        type="video",
        videoDuration="short",  # Filters for videos under 60 seconds
        order="viewCount"
    )
    search_response = search_request.execute()
    return [item['id']['videoId'] for item in search_response.get('items', [])]


def get_n_top_videos(video_ids: list) -> list:
    if video_ids:  # Get video statistics for these video IDs
        videos_request = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids)
        )
        videos_response = videos_request.execute()
        # Process and sort by view count
        videos = [
            {
                'title': item['snippet']['title'],
                'channelTitle': item['snippet']['channelTitle'],
                'lang': item['snippet'].get('defaultAudioLanguage'),
                'videoId': item['id'],
                'views': int(item['statistics']['viewCount']),
                'thumbnail': item['snippet']['thumbnails']['medium']['url']  # Get high-resolution thumbnail URL
            }
            for item in videos_response.get('items', [])
        ]
        return videos
    else:
        return []


if __name__ == '__main__':
    days = get_n_days(7)
    video_ids = get_video_ids(50, days)
    videos = get_n_top_videos(video_ids)
    top_10_videos = sorted(videos, key=lambda x: x['views'], reverse=True)[:10]
    for video in top_10_videos:
        print(f"Title: {video['title']}, Views: {video['views']}, Video ID: {video['videoId']}")
