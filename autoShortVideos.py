import os
import random
from typing import List,Tuple
import subprocess

from gtts import gTTS
from moviepy.editor import (
    CompositeVideoClip, CompositeAudioClip,
    VideoFileClip, AudioFileClip, ImageClip, TextClip,
    concatenate_videoclips, concatenate_audioclips
)
import moviepy.video.fx.all as vfx
from rich.console import Console
from rich.progress import track
import pyfiglet
from dotenv import load_dotenv
from moviepy.config import change_settings
# Load variables from .env file
load_dotenv(".env")

# Change settings for IMAGEMAGICK_BINARY
change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})
# Generate Speech
def generate_speech(
        text: str,
        lang: str = 'en',
        filename: str = 'audio.mp3',):
    """
    Generate Speech Audio from gTTS

    text: str - Text to be synthesized
    lang: str - Language of text
    filename: str - Filename of output
    """
    myobj = gTTS(text=text, lang=lang, slow=False, tld='ca') # Change per settings https://gtts.readthedocs.io/en/latest/module.html
    myobj.save(filename)
    return
# Generate Complete Clip
def clip(
        content: str,
        video_file: str,
        outfile: str,
        image_file: str = '',
        offset: int = 0,
        duration: int = 0):
    """
    Generate the Complete Clip

    content: str - Full content text
    video_file: str - Background video
    outfile: str - Filename of output
    image_file: str - Banner to display
    offset: int - Offset starting point of background video (default: 0)
    duration: int - Limit the video (default: audio length)
    """
    # Calculate the duration of the video clip
    video_clip = VideoFileClip(video_file)
    video_clip_duration = video_clip.duration

    # Generate audio and text clips
    audio_comp, text_comp = generate_audio_text(split_text(content))

    # Concatenate audio clips
    audio_comp_list = []
    for audio_file in track(audio_comp, description='Stitching Audio...'):
        audio_comp_list.append(AudioFileClip(audio_file))
    audio_comp_stitch = concatenate_audioclips(audio_comp_list)
    audio_comp_stitch.write_audiofile('temp_audio.mp3', fps=44100)

    audio_duration = audio_comp_stitch.duration
    if duration == 0:
        duration = audio_duration

    audio_comp_stitch.close()

    # Ensure the offset allows the full audio duration to fit within the video
    max_offset = video_clip_duration - duration
    offset = random.uniform(0, max_offset)

    vid_clip = VideoFileClip(video_file).subclip(offset, offset + duration)
    
    # Calculate the dimensions for 9:16 aspect ratio (I Used 1440P Video)
    width = int(vid_clip.size[1] * 9 / 16)
    height = vid_clip.size[1]
    
    # Crop the video to 9:16 aspect ratio
    vid_clip = vid_clip.crop(x_center=vid_clip.size[0] / 2, y_center=vid_clip.size[1] / 2, width=width, height=height)

    if image_file:
        image_clip = ImageClip(image_file).set_duration(duration).set_position(("center", 'center')).resize(0.8) # Adjust if the Banner is too small
        vid_clip = CompositeVideoClip([vid_clip, image_clip])

    vid_clip = CompositeVideoClip([vid_clip, concatenate_videoclips(text_comp).set_position(('center', 860))])

    vid_clip = vid_clip.set_audio(AudioFileClip('temp_audio.mp3').subclip(0, duration))
    vid_clip.write_videofile(outfile, audio_codec='aac')
    vid_clip.close()

# Split Text
def split_text(text: str, delimiter: str = '\n'):
    """
    Split the Text

    text: str - Text to split
    delimiter: str - Delimiter of split (default: \n)
    """
    return text.split(delimiter)

# Generate Audio and Text
def generate_audio_text(fulltext: List[str]):
    """
    Generate Audio and Text from Full Text

    fulltext: List[str] - List of splitted Text
    """
    audio_comp = []
    text_comp = []

    for idx, text in track(enumerate(fulltext), description='Synthesizing Audio...'):
        text = text.strip() # Remove leading and trailing whitespace
        if text == "":
            continue

        audio_file = f"temp_assets/audio_{idx}.mp3"
        generate_speech(text.strip(), filename=audio_file)
        audio_file_speed_up = f"temp_assets/audio_SpeedUp_{idx}.mp3"
        speed_up_audio(audio_file, audio_file_speed_up, 1.5)
        audio_duration = AudioFileClip(audio_file_speed_up).duration

        text_clip = TextClip(
            text,
            font='gsfonts', # Change Font if not found
            fontsize=64,
            color="white",
            align='center',
            method='caption',
            stroke_color='black',
            stroke_width=2,
            size=(660, None)
        )
        text_clip = text_clip.set_duration(audio_duration)

        audio_comp.append(audio_file_speed_up)
        text_comp.append(text_clip)

    return audio_comp, text_comp

# Delete the temp_assets contents
def clean_up_temp_assets(folder: str):
    """
    Delete the temp_assets folder and its contents

    folder: str - The path to the folder to delete
    """
    if os.path.exists(folder):
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
        #os.rmdir(folder) #remove folder
    if os.path.exists("temp_audio.mp3"):
        os.remove("temp_audio.mp3")

# Function to randomly select a video from the "BackgroundVideos" folder
def select_random_video(folder_path: str) -> str:
    """
    Select a random video from the "BackgroundVideos" folder

    folder_path: str - The path to the folder containing the videos
    """
    try:
        video_files = [f for f in os.listdir(folder_path) if f.endswith('.webm')]
        if not video_files:
            raise FileNotFoundError("No video files found in the folder.")
        return os.path.join(folder_path, random.choice(video_files))
    except Exception as e:
        console.print(f"\n[dark_red] Error Select Random Video: {e}")
        return

# Function to select all stories from text files in the "Stories" folder
def select_all_stories(folder_path: str) -> List[Tuple[str, str]]:
    """
    Select all stories from text files in the "Stories" folder

    folder_path: str - The path to the folder containing the stories
    """
    try:
        story_files = [f for f in os.listdir(folder_path) if f.startswith('Story_') and f.endswith('.txt')] # Change prefix if needed
        if not story_files:
            raise FileNotFoundError("No story files found in the folder.")
        
        sorted_story_files = sorted(story_files)  # Sort the story files
        stories = []

        for story_file in sorted_story_files:
            with open(os.path.join(folder_path, story_file), 'r',encoding="utf-8") as file:
                story_content = file.read()
                stories.append((story_file[:-4], story_content))  # Remove the '.txt' suffix and save file name and content

        return stories

    except Exception as e:
        console.print(f"\n[dark_red] Error Select All Stories: {e}")
        return []

# Function to speed up the audio
def speed_up_audio(input_file, output_file, speed=1.5):
    """
    Speed up the audio

    input_file: str - Input audio file
    output_file: str - Output audio file
    speed: float - Speed up factor (default: 1.5)
    """
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter:a", f"atempo={speed}",
        "-vn",  # Disable video recording
        "-y",   # Overwrite output file without asking
        output_file
    ]
    subprocess.run(command)    
# Main Function
if __name__ == '__main__':
    try:
        AUTOCLIP_VERSION = "1.0.0"
        console = Console()
        banner = pyfiglet.figlet_format(text='AutoShortVideos', font='rectangles')
        console.print()
        console.print(f'[bold][purple] {banner}'  )
        console.print("[dark_red] By hdfblack06 (https://github.com/hdfblack06)")
        console.print(f'[dark_red] Version: {AUTOCLIP_VERSION}')

        # Make temp_assets folder if it doesn't exist
        if not os.path.exists("temp_assets"):
            os.mkdir("temp_assets")
        
        # Make Results folder if it doesn't exist "
        if not os.path.exists("Results"):
            os.mkdir("Results")
        # Select all stories and generate clips
        content = select_all_stories("Stories")
        for filename, content in content:
            output_file = f"Results/{filename}.mp4"
            video_background_file = select_random_video("BackGroundVideos")
            console.print("\n[light_green] Task Starting...")
            clip(content=content, 
                video_file=video_background_file, 
                #image_file=image_banner_file,
                outfile=output_file)

        console.print("\n[light_green] Completed!")
        video_results = os.listdir("Results")
        if(video_results):
            os.startfile("Results")

    except Exception as e:
        console.print(f"\n[dark_red] Error Execute: {e}")
    finally:
        clean_up_temp_assets("temp_assets")
        console.print("\n[light_green] Cleaned up temp assets!")




