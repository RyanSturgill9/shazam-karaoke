import requests
import sounddevice as sd
import soundfile as sf
import shazam

# Function to recognize the song using the Shazam API
def recognize_song(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        shazam_client = shazam.Shazam(api_key='YOUR_SHAZAM_API_KEY')
        recognize_response = shazam_client.recognize(audio_file.read())
        return recognize_response

# Function to get lyrics using the Lyrics.ovh API
def get_lyrics(artist, title):
    lyrics_url = f'https://api.lyrics.ovh/v1/{artist}/{title}'
    response = requests.get(lyrics_url)
    if response.status_code == 200:
        return response.json()['lyrics']
    else:
        return "Lyrics not found."

# Function to record audio using sounddevice
def record_audio(duration, output_file):
    fs = 44100  # Sample rate
    recording = sd.rec(int(fs * duration), samplerate=fs, channels=2, dtype='int16')
    sd.wait()
    sf.write(output_file, recording, fs)

# Main function
def main():
    audio_file_path = 'recorded_audio.wav'
    recording_duration = 10  # Adjust the duration as needed

    print("Recording...")
    record_audio(recording_duration, audio_file_path)
    print("Recording complete.")

    # Recognize the song
    recognize_result = recognize_song(audio_file_path)
    track_title = recognize_result['track']['title']
    track_artist = recognize_result['track']['subtitle']

    print(f"Identified Song: {track_title} by {track_artist}")

    # Get and display lyrics
    lyrics = get_lyrics(track_artist, track_title)
    print("Lyrics:")
    print(lyrics)

if __name__ == "__main__":
    main()
