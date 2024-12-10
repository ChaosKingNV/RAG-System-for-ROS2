from transformers import pipeline
from tqdm import tqdm
import json

def generate_labeled_data(input_file="youtube_transcripts.json", output_file="labeled_data.json"):
    """
    Generate labeled Q/A data from YouTube transcripts using Hugging Face pipeline.
    """

    # Load transcripts
    with open(input_file, "r") as f:
        transcripts = json.load(f)

    # Initialize Hugging Face pipeline for Q/A generation
    qa_generator = pipeline("text2text-generation", model="facebook/bart-large-cnn")

    labeled_data = []

    # Calculate total segments for progress tracking
    total_segments = sum(len(video["transcript"]) for video in transcripts)

    print(f"📊 Processing {total_segments} transcript segments...")

    # Process each transcript segment with progress bar
    with tqdm(total=total_segments, desc="Generating Q/A pairs", unit="segment") as pbar:
        for video in transcripts:
            for segment in video["transcript"]:
                text = segment["text"]
                try:
                    question = qa_generator(f"Generate a question from: {text}")[0]["generated_text"]
                    answer = text

                    # Store Q/A pair
                    labeled_data.append({
                        "question": question,
                        "answer": answer,
                        "video_id": video["video_id"]
                    })

                except Exception as e:
                    print(f"❌ Error generating Q/A for segment: {text} | Error: {e}")

                # Update progress bar
                pbar.update(1)

    # Save labeled data
    with open(output_file, "w") as f:
        json.dump(labeled_data, f, indent=4)

    print(f"📁 Labeled data saved to {output_file}")

