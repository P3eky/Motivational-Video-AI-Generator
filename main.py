import os
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
#ELEVIN LABS API KEY
client = ElevenLabs(
  api_key="ELEVENLABS_AI_KEY",
)
import assemblyai as aai
#ASSEMBLY AI API KEY
aai.settings.api_key = "ASSEMBLY_AI_KEY"
from gpt4all import GPT4All
model = GPT4All(model_name='orca-mini-3b-gguf2-q4_0.gguf', model_path='./')
import datetime
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, concatenate_audioclips
import math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pysrt import SubRipFile
from pydub import AudioSegment

font="./my-font.ttf"

"""
WORKFLOW:
0 - It is checked that there is nothing in the "customscript.txt" file, if there is that text will be used as the script for the video.
1 - ChatGPT generates text to be used for the video.
2 - The ChatGPT script is passed to Eleven Labs, which genertes an mp3 file to be used for the video.
3 - The text to speech audio is passed into AssemblyAI, which 
"""

#FINISHED
def dsc_log(text):
    textdsc=str(text)
    os.system('python send_discord.py ' + textdsc)


#UNFINISHED
def cleanExistingFiles():
    dsc_log("Deleting-Old-Files:wastebasket:")

    files_to_delete = [
        "subtitles.srt",
        "tts.mp3",
        "video.mp4",
        "final_output_video.mp4",
        "temp_video.mp4",
        "TEMPoutput_video.mp4",
        "videoTEMP_MPY_wvf_snd.mp4",
        "video_with_background.mp4",
        "ttsShort.mp3"
    ]
    
    for file_name in files_to_delete:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Deleted: {file_name}")
            dsc_log(f"Deleted:{file_name}:x:")
        else:
            print(f"{file_name} does not exist, skipping deletion.")


#FINISHED
def mp3Gen(text, filename):
    dsc_log("Starting_Audio_Generation:loud_sound:")
    audio = client.generate(
  	text=text,
  	voice="Adam")

    save(audio, str(filename)+".mp3")
    dsc_log("Finished-Audio-Generation:loud_sound:")

#FINISHED
def replace_spaces_with_dashes(input_string):
    return input_string.replace(' ', '-')


#FINISHED
def extend_mp3_duration():
    # Define input and output file paths
    input_mp3 = "./ttsShort.mp3"
    output_mp3 = "./tts.mp3"
    
    # Duration to extend the MP3 file by (in seconds)
    extension_duration = 3
    
    # Load the input MP3 file
    audio = AudioSegment.from_file(input_mp3, format="mp3")
    
    # Create a silent audio segment with the desired extension duration (in milliseconds)
    silence = AudioSegment.silent(duration=extension_duration * 1000)
    
    # Concatenate the original audio with the silent audio segment
    extended_audio = audio + silence
    
    # Export the extended audio as MP3
    extended_audio.export(output_mp3, format="mp3")
    dsc_log("Mp3-Extended:straight_ruler:")


#FINISHED
def subTextGen():
    cleanExistingFiles()
    dsc_log("Starting-Subtitle-Text-Generation:abcd:")

    current_date = datetime.datetime.now()
    day_of_week = current_date.strftime('%A')

    with model.chat_session():
        response = model.generate(prompt='There are these Tiktok videos that are like "wake the fuck up you fucking glorious man, todays your fucking day" and it is inspirational to start and go at your goals and it constantly uses swear words, like almost every other sentence. Make text similar to that with at least 1/3 of the text being curse words (Fuck, Shit, Badass, Motherfucker, etc.) Start with the f word within the first three words to grab the viewers attention. Do not hesitate to think there are too few. The day of the week is ' + day_of_week.upper() + ' , so incorporate that into the prompt if you see fit. Limit it to under 65 words because it needs to be a shorter video. DO NOT PUT EMOJIS. Do not put the text inside of quotes. Be really energetic and capitalize text you want to sound like it is yelling in the text to speech. Always end it with "LETS FUCKING GO!" Capitalize power words. The main thing to worry about is that it is under 100 words and over 70 words. Only respond with the answer and no context.', temp=0.50)
    response = str(response)
    print(response)
    dsc_log("Finished-Subtitle-Text-Generation:abcd:")
    dsc_log("The-prompt-is:" +  replace_spaces_with_dashes(response))
    mp3Gen(response, "ttsShort")
    extend_mp3_duration()
    os.remove("./ttsShort.mp3")
    return response

#FINISHED
def subTitleGen():
    subtitleText = subTextGen()
    dsc_log("Starting-Subtitle-Generation:film_frames:")
    transcript = aai.Transcriber().transcribe("tts.mp3")

    subtitles = transcript.export_subtitles_srt()

    f=open("subtitles.srt", "a")
    f.write(subtitles)
    f.close
    dsc_log("Finished-Subtitle-Generation:film_frames:")


#FINISHED
def videoEditSplice():

    subTitleGen()

    dsc_log("Starting-Splicing-Together-Video:vhs:")
    
    audio_path = './tts.mp3'
    media_folder = './media'
    output_path = './TEMPoutput_video.mp4'

    # Get available video clips
    available_clips = [f"{i}.mp4" for i in range(1, 101)]
    random.seed()  # Initialize random seed for random module
    random_clips = random.sample(available_clips, len(available_clips))  # Shuffle all available clips
    video_clips = []

    # Calculate number of clips needed
    audio_length = AudioFileClip(audio_path).duration
    num_clips_needed = math.ceil(audio_length / 5)

    # Load video clips
    for i in range(num_clips_needed):
        if i < len(random_clips):  # Ensure we don't exceed available clips
            clip_path = os.path.join(media_folder, random_clips[i])
            if os.path.exists(clip_path):  # Check if clip exists
                clip = VideoFileClip(clip_path).subclip(0, 5)
                video_clips.append(clip)

    if len(video_clips) == 0:
        print("Error: No valid video clips found.")
        return

    # Concatenate video clips
    final_video = concatenate_videoclips(video_clips)

    # Set audio
    audio = AudioFileClip(audio_path)
    final_video = final_video.set_audio(audio)

    # Write final video file
    try:
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        print(f"Video saved successfully to {output_path}")
    except Exception as e:
        print(f"Error occurred while writing video file: {e}")
    finally:
        # Close resources
        audio.close()
        final_video.close()

    dsc_log("Finished-Splicing-Together-Video:vhs:")


def generate_video_with_subtitles_and_audio():
    # Define paths and parameters

    videoEditSplice()
    dsc_log("Starting-Burning-Subtitles:fire:")
    video_path = './TEMPoutput_video.mp4'
    srt_path = './subtitles.srt'
    output_path = './final_output_video.mp4'
    audio_path = './tts.mp3'
    font_path = font
    font_size = 125
    outline_width = 8  # Increase this value for a thicker outline

    # Load the custom font
    font = ImageFont.truetype(font_path, font_size)

    # Configure video parameters
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Parse subtitle file
    subs = SubRipFile.open(srt_path)
    word_timings = []
    for sub in subs:
        words = sub.text.split()
        start_time = sub.start.ordinal / 1000.0
        end_time = sub.end.ordinal / 1000.0
        duration = (end_time - start_time) / len(words)
        for i, word in enumerate(words):
            word_timings.append((word, start_time + i * duration, start_time + (i + 1) * duration))

    # Initialize lists for edited video frames and subtitles
    edited_frames = []

    # Function to add subtitle text to a frame
    def add_subtitle_text(frame_img, text):
        pil_img = Image.fromarray(cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

        # Calculate text size and position
        text_size = draw.textlength(text, font=font)
        text_x = (width - text_size) // 2
        text_y = (height - font_size) // 2

        # Define outline color
        outline_color = 'black'

        # Draw text with outline
        for i in range(1, outline_width + 1):
            # Draw outline
            draw.text((text_x-i, text_y-i), text, font=font, fill=outline_color)
            draw.text((text_x+i, text_y-i), text, font=font, fill=outline_color)
            draw.text((text_x-i, text_y+i), text, font=font, fill=outline_color)
            draw.text((text_x+i, text_y+i), text, font=font, fill=outline_color)

        # Draw actual text
        draw.text((text_x, text_y), text, font=font, fill='white')

        # Convert PIL image back to OpenCV format
        frame_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        return frame_img

    # Iterate through each frame of the video
    frame_num = 0
    current_word_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_time = frame_num / fps

        # Add subtitles if necessary
        if current_word_idx < len(word_timings) and word_timings[current_word_idx][1] <= frame_time:
            word, start_time, end_time = word_timings[current_word_idx]

            # Add subtitle text to the frame
            frame = add_subtitle_text(frame, word)

            # Move to the next subtitle
            if end_time <= frame_time:
                current_word_idx += 1

        edited_frames.append(frame)
        frame_num += 1

    cap.release()

    # Write edited frames to a temporary video file
    temp_video_path = './temp_video.mp4'
    out = cv2.VideoWriter(temp_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for frame in edited_frames:
        out.write(frame)
    out.release()

    # Load edited video clip
    edited_clip = VideoFileClip(temp_video_path)

    # Load audio clip
    audio_clip = AudioFileClip(audio_path)

    # Set audio for the video clip
    final_clip = edited_clip.set_audio(audio_clip)

    # Write final video with audio to output path
    final_clip.write_videofile(output_path, codec='libx264', fps=fps)

    # Close clips
    edited_clip.close()
    audio_clip.close()

    # Clean up temporary video file
    os.remove(temp_video_path)
    dsc_log("Finished-Burning-Subtitles:flame:")
# Example usage:

def overlay_audio():
    generate_video_with_subtitles_and_audio()
    
    dsc_log("Starting-Overlaying-Music:musical_note:")
    input_video = "./final_output_video.mp4"
    background_music = "./music.mp3"
    output_video = "./video.mp4"
    
    # Ffmpeg command to overlay background music
    ffmpeg_command = (
        f"ffmpeg -i {input_video} -i {background_music} "
        f"-filter_complex \"[0:a]volume=1.0[a0]; [1:a]volume=0.35[a1]; "
        f"[a0][a1]amix=inputs=2:duration=first:dropout_transition=2\" "
        f"-c:v copy -shortest {output_video}"
    )
    
    # Execute the ffmpeg command using os.system
    os.system(ffmpeg_command)

    # Clean up: delete temporary video
    # Uncomment and adjust as needed
    if os.path.exists('TEMPoutput_video.mp4'):
        os.remove('TEMPoutput_video.mp4')
    if os.path.exists('final_output_video.mp4'):
        os.remove('final_output_video.mp4')
    
    dsc_log("Finished-Overlaying-Music:musical_note:")


if __name__ == '__main__':
    overlay_audio()
    dsc_log("Finsihed-Video-Generation:white_check_mark:")
    
