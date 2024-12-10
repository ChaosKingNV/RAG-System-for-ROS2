from youtube_transcript_api import YouTubeTranscriptApi
import json

def fetch_youtube_transcripts(video_ids, output_file="youtube_transcripts.json"):
    transcripts = []

    for video_id in video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcripts.append({
                "video_id": video_id,
                "transcript": transcript
            })
            print(f"✅ Transcript fetched for video {video_id}")
        except Exception as e:
            print(f"❌ Error fetching transcript for video {video_id}: {e}")

    # Save transcripts to JSON
    with open(output_file, "w") as f:
        json.dump(transcripts, f, indent=4)
    print(f"📁 Transcripts saved to {output_file}")
