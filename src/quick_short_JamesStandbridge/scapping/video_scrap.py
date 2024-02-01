import requests
from dotenv import load_dotenv
import os
import argparse
from moviepy.editor import concatenate_videoclips, VideoFileClip
import json  

load_dotenv()

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

def search_pexels_videos(query, orientation=None, size=None, locale=None, page=1, per_page=10):
    """
    Search for videos on Pexels.

    :param query: The search query string.
    :param orientation: Desired orientation of the videos ('landscape', 'portrait', 'square').
    :param size: Minimum size of the videos ('large', 'medium', 'small').
    :param locale: Locale for the search.
    :param page: Page number of the results.
    :param per_page: Number of results per page.
    :return: Search result as a JSON dictionary.
    """
    url = "https://api.pexels.com/videos/search"
    headers = {'Authorization': PEXELS_API_KEY}
    params = {
        'query': query,
        'orientation': orientation,
        'size': size,
        'locale': locale,
        'page': page,
        'per_page': per_page
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    return result

def download_video(url, file_path):
    """
    Download a video from a given URL and save it to a specified path.

    :param url: URL of the video to be downloaded.
    :param file_path: Path to save the downloaded video.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Video successfully downloaded: {file_path}")
    else:
        print(f"Failed to download the video. Status Code: {response.status_code}")

def download_video_from_pexel_search(query_result, file_path, desired_duration):
    """
    Download videos from a Pexels search result and concatenate them until the desired duration is reached or exceeded,
    prioritizing videos with a resolution of 1080x1920 or an equivalent aspect ratio.

    :param query_result: Pexels search result.
    :param file_path: Path to save the final concatenated video.
    :param desired_duration: Desired total duration of the video in seconds.
    """
    total_duration = 0
    video_clips = []
    for video in query_result.get('videos'):
        selected_video_file = None
        for video_file in video.get('video_files'):
            width = video_file.get('width')
            height = video_file.get('height')
            aspect_ratio = width / height if height else 0
            
            if abs(aspect_ratio - (9/16)) < 0.01:
                if width == 1080 and height == 1920:
                    selected_video_file = video_file
                    break
                elif not selected_video_file or video_file.get('quality') == 'hd':
                    selected_video_file = video_file
        
        if selected_video_file:
            video_url = selected_video_file.get('link')
            temp_file_path = f"temp_{len(video_clips)}.mp4"
            download_video(video_url, temp_file_path)
            clip = VideoFileClip(temp_file_path)
            video_clips.append(clip)
            total_duration += clip.duration
            if total_duration >= desired_duration:
                break
    
    if video_clips:
        final_clip = concatenate_videoclips(video_clips)
        final_clip.write_videofile(file_path)
        
        # Clean up the temporary files
        for clip in video_clips:
            clip.close()
            os.remove(clip.filename)
    else:
        print("No videos found matching the desired aspect ratio and resolution.")

def main():
    parser = argparse.ArgumentParser(description="Download videos from Pexels based on search query.")
    parser.add_argument("file_path", help="Path to save the downloaded video")
    parser.add_argument("query", nargs='+', help="Search query keywords")
    parser.add_argument("duration", type=int, help="Desired total duration of the video in seconds")

    args = parser.parse_args()

    query = ' '.join(args.query)
    file_path = args.file_path
    desired_duration = args.duration

    result = search_pexels_videos(query)
    download_video_from_pexel_search(result, file_path, desired_duration)

if __name__ == "__main__":
    main()