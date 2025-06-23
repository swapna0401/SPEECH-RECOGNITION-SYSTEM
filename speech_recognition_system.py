"""
Speech-to-Text Transcription Tool

Description:
A Python-based tool to convert audio files (WAV or MP3) into transcribed text using
Google's Web Speech API. It includes optional MP3 to WAV conversion, audio duration
calculation, and saves a detailed transcription report to a text file.

"""

import os
import wave
import contextlib
import datetime
import speech_recognition as sr
from pydub import AudioSegment

def get_audio_duration(path):
    """
    Calculates and returns the duration of a WAV audio file in seconds.

    Parameters:
        path (str): Path to the WAV file.

    Returns:
        float: Duration in seconds.
    """
    try:
        with contextlib.closing(wave.open(path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = round(frames / float(rate), 2)
            return duration
    except Exception as e:
        print(f"Error reading audio file: {e}")
        return 0

def transcribe_audio(path):
    """
    Transcribes speech from an audio file using Google's Web Speech API.

    Parameters:
        path (str): Path to the WAV audio file.

    Returns:
        str: Transcribed text or an error message.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        print("Listening to audio...")
        audio_data = recognizer.record(source)
    try:
        print("Transcribing audio...")
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Google API request failed: {e}"

def save_transcription_report(file_path, duration, transcription):
    """
    Saves the transcription and audio metadata to a text file.

    Parameters:
        file_path (str): Path of the input audio file.
        duration (float): Duration of the audio.
        transcription (str): The transcribed text.
    """
    output_file = "transcription_output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("TRANSCRIPTION REPORT\n")
        f.write("="*50 + "\n")
        f.write(f"File Name     : {file_path}\n")
        f.write(f"Duration      : {duration} seconds\n")
        f.write(f"Processed At  : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("Transcribed Text:\n")
        f.write(transcription + "\n")
    print(f"\nTranscription successfully saved to '{output_file}'")

def main():
    """
    Main function to drive the speech-to-text transcription process.
    """
    print("\nSpeech-to-Text Transcription Tool")
    print("=" * 50)

    # Step 1: Request file path from user
    file_name = input("Enter the full path to your .wav or .mp3 file: ").strip()

    if not os.path.isfile(file_name):
        print("Error: The specified file does not exist.")
        return

    file_ext = file_name.split('.')[-1].lower()
    print(f"\nFile detected: {file_name}")
    print(f"File type     : {file_ext}")

    # Step 2: Convert MP3 to WAV if necessary
    if file_ext == "mp3":
        print("\nConverting MP3 to WAV format...")
        mp3_audio = AudioSegment.from_mp3(file_name)
        wav_file = file_name.replace(".mp3", ".wav")
        mp3_audio.export(wav_file, format="wav")
        file_path = wav_file
        print(f"Conversion complete. New file: {wav_file}")
    elif file_ext == "wav":
        file_path = file_name
    else:
        print("Unsupported file type. Please provide a .mp3 or .wav file.")
        return

    # Step 3: Get audio duration
    duration = get_audio_duration(file_path)
    print(f"\nAudio Duration: {duration} seconds")

    # Step 4: Transcribe audio
    transcription = transcribe_audio(file_path)

    # Step 5: Print report to terminal
    print("\n" + "="*70)
    print("TRANSCRIPTION REPORT")
    print("="*70)
    print(f"File Name     : {file_path}")
    print(f"Duration      : {duration} seconds")
    print(f"Processed At  : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nTranscribed Text:\n")
    print(transcription)
    print("="*70)

    # Step 6: Save output to file
    save_transcription_report(file_path, duration, transcription)

# Entry Point
if __name__ == "__main__":
    main()
