from openai import OpenAI
import time
from pathlib import Path

client = OpenAI()

def get_transcript(audiopath):
    audio_file= open(audiopath, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcript.text


def get_assistant_reply(query):

    threadId = "<Your Thread ID>"
    assistantId = "<Your Assistant ID>"
    message = client.beta.threads.messages.create(
    thread_id=threadId,
    role="user",
    content=query
        )
    
    run = client.beta.threads.runs.create(
    thread_id=threadId,
    assistant_id=assistantId,
    instructions="Please provide very short and to the point frank responses.."
    )

    response = "Couldn't get response. something went wrong."
    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=threadId,
        run_id=run.id
        )
        time.sleep(1)
        if run.status == 'completed':
            messages_ = client.beta.threads.messages.list(
            thread_id=threadId,
            )
            response = messages_.data[0].content[0].text.value
            break
    return response


def get_text_to_audio(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text
    )
    response.stream_to_file(speech_file_path)
    return "speech.mp3"
    