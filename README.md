# Motivational Video AI Generator

# What is This?

This is a tool I created to use several AI programs in order to generate motivational short videos that can be posted on social media. It has support for outputting logs into discord using a discord bot.

## Installation

**I RECOMMEND THAT YOU SAVE THIS IN A SEPARATE FOLDER TO AVOID ANY FILES BEING ACCIDENTIALLY DELETED**

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the several necessary packages to run the script.

```bash
pip install elevenlabs assemblyai GPT4All moviepy pydub opencv-python-headless av ffmpeg-python pysrt pillow numpy 
```

Install ffmpeg using any of the methods seen [here](https://avpres.net/FFmpeg/install_Windows).

You will require the following accounts to run the script.
- [Elevenlabs](https://elevenlabs.io/)
- [AssemblyAI](https://www.assemblyai.com/)

Add the proper AI keys to the following lines to set up the script.
```python
client = ElevenLabs(
  api_key="ELEVENLABS_AI_KEY",
)
import assemblyai as aai
#ASSEMBLY AI API KEY
aai.settings.api_key = "ASSEMBLY_AI_KEY"
```
The font can also be changed by changing the following line to the font path.
```python
font="./my-font.ttf"
```
## Adding Media
In order to have background videos, there is a folder titled `Media`, in which 100 different videos titled 1.mp4 to 100.mp4 need to be provided in the 1080x1920px ratio (9:16 Vertical). 

## Adding Music
Just place a file titled `music.mp3` into the root of the folder 

## Usage

Just run the `start.bat` file to open the script.

## Discord Bot
A discord bot is highly recommended, and you can see how to create one [here](https://www.upwork.com/resources/how-to-make-discord-bot).

Replace the following lines with your bot information in the `send_discord.py` file to set up the bot.
```python
# Replace with your bot token
BOT_TOKEN = 'BOT_TOKEN'
# Replace with your channel ID
CHANNEL_ID = CHANNEL_ID
```
