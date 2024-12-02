from youtube_transcript_api import YouTubeTranscriptApi

def fetch_youtube_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript
