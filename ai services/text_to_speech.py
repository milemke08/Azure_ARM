import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration values from .env
TTS_API_KEY = os.getenv("TTS_SERVICE_KEY")
TTS_API_ENDPOINT = os.getenv("TTS_SERVICE_ENDPOINT")

# Validate environment variables
if not TTS_API_KEY or not TTS_API_ENDPOINT:
    raise EnvironmentError("TTS_SERVICE_KEY and TTS_SERVICE_ENDPOINT must be set in the .env file.")

# Function to call Azure TTS API
def text_to_speech(text, output_file):
    """
    Converts text to speech using Azure TTS API.
    """
    # Define the SSML content with emotion and intonation
    ssml_template = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <!-- Opening Greeting -->
    <voice name="en-US-GuyNeural">
        <prosody rate="0.95" pitch="0%">Well howdy there, stranger!</prosody>
        <break time="300ms" />
        <prosody rate="0.95" pitch="-1%">Ain’t seen your face ‘round these parts before.</prosody>
    </voice>
    
    <!-- Welcome -->
    <voice name="en-US-GuyNeural">
        <prosody rate="0.95" pitch="0%">
            Welcome to the Silver Spur Saloon,
        </prosody>
        <break time="300ms" />
        <prosody rate="0.95" pitch="0%">the finest waterin’ hole this side of the Pecos River.</prosody>
    </voice>
    
    <!-- Suggesting Drinks -->
    <voice name="en-US-GuyNeural">
        <prosody rate="0.95" pitch="0%">
            You look like you’ve been ridin’ hard.
        </prosody>
        <break time="300ms" />
        <prosody rate="0.95" pitch="-1%">How ’bout a cold sarsaparilla or somethin’ stronger?</prosody>
        <break time="300ms" />
        <prosody rate="0.95" pitch="0%">
            Got the best whiskey in town.
        </prosody>
        <break time="200ms" />
        <prosody rate="0.95" pitch="0%">Goes down smooth as a prairie breeze.</prosody>
    </voice>
    
    <!-- Inviting to Stay -->
    <voice name="en-US-GuyNeural">
        <prosody rate="0.95" pitch="0%">
            Pull up a chair, make yourself at home.
        </prosody>
        <break time="300ms" />
        <prosody rate="0.95" pitch="0%">
            Cards and dice start in an hour,
        </prosody>
        <break time="200ms" />
        <prosody rate="0.95" pitch="-1%">and Slim over there’s already itchin’ for a game.</prosody>
    </voice>
    
    <!-- Lighthearted Warning -->
    <voice name="en-US-GuyNeural">
        <prosody rate="0.95" pitch="0%">
            And if trouble finds ya,
        </prosody>
        <break time="200ms" />
        <prosody rate="0.95" pitch="-1%">don’t worry—we keep things nice and civilized ’round here.</prosody>
        <break time="300ms" />
        <prosody rate="0.95" pitch="0%">Mostly.</prosody>
    </voice>
    
    <!-- Closing Offer -->
    <voice name="en-US-GuyNeural">
        <prosody rate="0.95" pitch="0%">
            Now, what’ll it be, friend?
        </prosody>
        <break time="300ms" />
        <prosody rate="0.95" pitch="0%">The bar’s open and the stories are free.</prosody>
    </voice>
</speak>"""


    # Construct headers
    headers = {
        "Ocp-Apim-Subscription-Key": TTS_API_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm"
    }

    # Make the API request
    response = requests.post(
        # url=f"{TTS_API_ENDPOINT}/cognitiveservices/v1",
        url="https://eastus.tts.speech.microsoft.com/cognitiveservices/v1",
        headers=headers,
        data=ssml_template
    )

    # Check the response status
    if response.status_code == 200:
        # Save the audio content to the output file
        with open(output_file, "wb") as audio_file:
            audio_file.write(response.content)
        print(f"Audio content saved to {output_file}")
    else:
        print(f"Error: {response.status_code}")
        print(f"Error: {response.reason}")
        print(response.text)

# Main program
if __name__ == "__main__":
    # Text-to-speech example
    
    output_audio_file = "ai services\output_audio.wav"
    text_to_speech("This is a test of Azure TTS with emotion and intonation.", output_audio_file)
    print('code ran')
