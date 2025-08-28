# Project: AIUI

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
![Maintaner](https://img.shields.io/badge/maintainer-Synosis_Systems-blue)

[![forthebadge made-with-python](https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
![uses Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![uses DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

![uses git](https://img.shields.io/badge/git%20-%23F05033.svg?&style=for-the-badge&logo=git&logoColor=white)
[![uses-github](https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white)](https://GitHub.com/)

[![uses-html](https://img.shields.io/badge/html5%20-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white")](http://ForTheBadge.com)
[![uses-css](https://img.shields.io/badge/css3%20-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white)](http://ForTheBadge.com)
![uses Bootstrap](https://img.shields.io/badge/bootstrap%20-%23563D7C.svg?&style=for-the-badge&logo=bootstrap&logoColor=white")

![uses docker](https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white)
![uses postgres](https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white)

* Main Project Directory:
* Project Source Directory (under version control):
* Project Description: This project is an AI interface allowing access to user defined AI models.

## Project Initialisation

Project Initialised by: Simon Snowden

Project Initialised on: 16/06/2025

## Overview

AIUI is a demonstration app that includes an interface for AI models both through the web and through the BrilliantLabs Frame AR glasses (https://brilliant.xyz/). It is meant as a replacement for the default NOA server.

It is based on a stack of Python, Django, HTMX, and Bootstrap. It is meant to be run through a VS Code dev container (https://code.visualstudio.com/docs/devcontainers/containers).

## Notes

This is not meant as a project for those new to software development. It is built with experienced developers in mind and especially needs a good level around the Django framework. Some of the code has been built quick and dirty as it's basis is just a personal, weekend project.

I wouldn't want to deter anyone from using this repository but please be aware that if you are new to any of the technologies above you may face many frustrations working with this repository.

This is meant as a personal project running on a private server as a means to understanding developing replacement NOA servers for the BrilliantLabs Frame AR glasses. I also use my version of this app to experiment with all things AI and build memory, the ability to carry out specific workflows, and all kinds of silly ideas, through my BrilliantLabs Frame AR glasses. Essentially a lot of what has been introduced with the new BrilliantLabs Halo AR glasses. You've just got to love BrilliantLabs approach to open source wearable. Make it what you want to be.

As such there is some security built in (as comes standard with Django) but there are still many aspects of security missing so please do not expect this to be ready to use as a SaaS. If you do deploy as-is I cannot take any responsibility for security failures. To be clear: **DO NOT USE THIS ON ANYTHING OTHER THAN A PRIVATE SERVER BEHIND A FIREWALL ON A VPN**.

This is also built at the moment for a single user, but multiple users can be signed up. However, be aware that every user will be able to see evey other users chats and ai models. If you want fences between user data then you will need to implement this in the appropriate places.

You will find that there are a whole suite of tests at every level including functional tests (end-user tests). I wouldn't claim these cover all use cases, but they are a useful starting point to understanding the app, how it is configured and how it is used. There is no user manual, but if you wish to understand how it is used look at the various functional tests scattered throughout the project.

This project will not be actively maintained as it is only meant as a learning tool regarding creating replacement NOA servers for the BrilliantLabs Frame AR glasses. If you decide to use it as basis for your own NOA server then ensure you develop to the strongest security principles.

## Initialising

* Start the devcontainer by selecting 'Reopen container' from the VS Code command pallette. This should * happily build the base container for working on the project.
* Open a terminal.
* At the command line type `pip list` and you should see the following (or something very similar).

```bash
root@a7c991d0bc40:/app# pip list
Package                       Version
----------------------------- -----------
alabaster                     1.0.0
asgiref                       3.9.1
attrs                         25.3.0
babel                         2.17.0
certifi                       2025.8.3
cffi                          1.17.1
charset-normalizer            3.4.3
coverage                      5.5
cryptography                  45.0.6
debugpy                       1.8.16
distlib                       0.4.0
dj-database-url               3.0.1
dj-email-url                  1.0.6
Django                        5.2.5
django-allauth                65.11.1
django-appconf                1.1.0
django-cache-url              3.4.5
django-cryptography           1.1
django-debug-toolbar          6.0.0
djangorestframework           3.16.1
docutils                      0.21.2
docxcompose                   1.4.0
docxtpl                       0.20.1
environs                      14.3.0
filelock                      3.19.1
gunicorn                      23.0.0
h11                           0.16.0
idna                          3.10
imagesize                     1.4.1
Jinja2                        3.1.6
lxml                          6.0.1
MarkupSafe                    3.0.2
marshmallow                   4.0.0
mysqlclient                   2.2.7
outcome                       1.3.0.post0
packaging                     25.0
pip                           24.0
pipenv                        2025.0.4
platformdirs                  4.4.0
psycopg                       3.2.9
psycopg-binary                3.2.9
psycopg-pool                  3.2.6
pycparser                     2.22
Pygments                      2.19.2
PySocks                       1.7.1
python-docx                   1.2.0
python-dotenv                 1.1.1
requests                      2.32.5
roman-numerals-py             3.1.0
selenium                      4.12.0
setuptools                    80.9.0
six                           1.17.0
sniffio                       1.3.1
snowballstemmer               3.0.1
sortedcontainers              2.4.0
Sphinx                        8.2.3
sphinxcontrib-applehelp       2.0.0
sphinxcontrib-devhelp         2.0.0
sphinxcontrib-htmlhelp        2.1.0
sphinxcontrib-jsmath          1.0.1
sphinxcontrib-qthelp          2.0.0
sphinxcontrib-serializinghtml 2.0.0
sqlparse                      0.5.3
trio                          0.30.0
trio-websocket                0.12.2
typing_extensions             4.15.0
urllib3                       2.5.0
virtualenv                    20.34.0
wheel                         0.45.1
whitenoise                    6.9.0
wsproto                       1.2.0

[notice] A new release of pip is available: 24.0 -> 25.2
[notice] To update, run: pip install --upgrade pip
```

* From this list two key libraries are missing for ineteracting with key AI components in the project.
* At the moment pipenv cannot install the OpenAI library so you need to install it manually using pip with the command `pip install openai`. This will need to be done every time the python container is rebuilt.
* At the moment pipenv cannot install the `openai-whisper` library so you need to install it manually using pip with the command `pip install openai-whisper`. This will need to be done every time the python conatainer is rebuilt. Don't forget to install the ffmpeg library if not already installed. To do this `apt-get update` followed by `apt-get install ffmpeg`
* Everytime you rebuild the dev container you may need to do these two actions.
* The easiest way to do this is to build a requirements.txt and then include that and the installation of ffmpeg in the Docker file. Maybe the first customisation you do?
* When you have installed ffmpeg the command `ffmpeg` at the command line should show something like this:

```bash
root@a7c991d0bc40:/app# ffmpeg
ffmpeg version 7.1.1-1+b1 Copyright (c) 2000-2025 the FFmpeg developers
  built with gcc 14 (Debian 14.2.0-19)
  configuration: --prefix=/usr --extra-version=1+b1 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --disable-libmfx --disable-omx --enable-gnutls --enable-libaom --enable-libass --enable-libbs2b --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libglslang --enable-libgme --enable-libgsm --enable-libharfbuzz --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-openal --enable-opencl --enable-opengl --disable-sndio --enable-libvpl --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-ladspa --enable-libbluray --enable-libcaca --enable-libdvdnav --enable-libdvdread --enable-libjack --enable-libpulse --enable-librabbitmq --enable-librist --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libx264 --enable-libzmq --enable-libzvbi --enable-lv2 --enable-sdl2 --enable-libplacebo --enable-librav1e --enable-pocketsphinx --enable-librsvg --enable-libjxl --enable-shared
  libavutil      59. 39.100 / 59. 39.100
  libavcodec     61. 19.101 / 61. 19.101
  libavformat    61.  7.100 / 61.  7.100
  libavdevice    61.  3.100 / 61.  3.100
  libavfilter    10.  4.100 / 10.  4.100
  libswscale      8.  3.100 /  8.  3.100
  libswresample   5.  3.100 /  5.  3.100
  libpostproc    58.  3.100 / 58.  3.100
Universal media converter
usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...

Use -h to get full help or, even better, run 'man ffmpeg'
```

* Once you have installed the two libraries `pip list` should give this.

```bash
root@a7c991d0bc40:/app# pip list
Package                       Version
----------------------------- -----------
alabaster                     1.0.0
annotated-types               0.7.0
anyio                         4.10.0
asgiref                       3.9.1
attrs                         25.3.0
babel                         2.17.0
certifi                       2025.8.3
cffi                          1.17.1
charset-normalizer            3.4.3
coverage                      5.5
cryptography                  45.0.6
debugpy                       1.8.16
distlib                       0.4.0
distro                        1.9.0
dj-database-url               3.0.1
dj-email-url                  1.0.6
Django                        5.2.5
django-allauth                65.11.1
django-appconf                1.1.0
django-cache-url              3.4.5
django-cryptography           1.1
django-debug-toolbar          6.0.0
djangorestframework           3.16.1
docutils                      0.21.2
docxcompose                   1.4.0
docxtpl                       0.20.1
environs                      14.3.0
filelock                      3.19.1
fsspec                        2025.7.0
gunicorn                      23.0.0
h11                           0.16.0
httpcore                      1.0.9
httpx                         0.28.1
idna                          3.10
imagesize                     1.4.1
Jinja2                        3.1.6
jiter                         0.10.0
llvmlite                      0.44.0
lxml                          6.0.1
MarkupSafe                    3.0.2
marshmallow                   4.0.0
more-itertools                10.7.0
mpmath                        1.3.0
mysqlclient                   2.2.7
networkx                      3.5
numba                         0.61.2
numpy                         2.2.6
nvidia-cublas-cu12            12.8.4.1
nvidia-cuda-cupti-cu12        12.8.90
nvidia-cuda-nvrtc-cu12        12.8.93
nvidia-cuda-runtime-cu12      12.8.90
nvidia-cudnn-cu12             9.10.2.21
nvidia-cufft-cu12             11.3.3.83
nvidia-cufile-cu12            1.13.1.3
nvidia-curand-cu12            10.3.9.90
nvidia-cusolver-cu12          11.7.3.90
nvidia-cusparse-cu12          12.5.8.93
nvidia-cusparselt-cu12        0.7.1
nvidia-nccl-cu12              2.27.3
nvidia-nvjitlink-cu12         12.8.93
nvidia-nvtx-cu12              12.8.90
openai                        1.102.0
openai-whisper                20250625
outcome                       1.3.0.post0
packaging                     25.0
pip                           25.2
pipenv                        2025.0.4
platformdirs                  4.4.0
psycopg                       3.2.9
psycopg-binary                3.2.9
psycopg-pool                  3.2.6
pycparser                     2.22
pydantic                      2.11.7
pydantic_core                 2.33.2
Pygments                      2.19.2
PySocks                       1.7.1
python-docx                   1.2.0
python-dotenv                 1.1.1
regex                         2025.7.34
requests                      2.32.5
roman-numerals-py             3.1.0
selenium                      4.12.0
setuptools                    80.9.0
six                           1.17.0
sniffio                       1.3.1
snowballstemmer               3.0.1
sortedcontainers              2.4.0
Sphinx                        8.2.3
sphinxcontrib-applehelp       2.0.0
sphinxcontrib-devhelp         2.0.0
sphinxcontrib-htmlhelp        2.1.0
sphinxcontrib-jsmath          1.0.1
sphinxcontrib-qthelp          2.0.0
sphinxcontrib-serializinghtml 2.0.0
sqlparse                      0.5.3
sympy                         1.14.0
tiktoken                      0.11.0
torch                         2.8.0
tqdm                          4.67.1
trio                          0.30.0
trio-websocket                0.12.2
triton                        3.4.0
typing_extensions             4.15.0
typing-inspection             0.4.1
urllib3                       2.5.0
virtualenv                    20.34.0
wheel                         0.45.1
whitenoise                    6.9.0
wsproto                       1.2.0
```

* You should now see that 'openai' and 'openai-whisper' are now installed.
* Create a `.env` file in the project root (the same directory that 'manage.py' is in). For the contents see below in **Environment Variables > .env File**.
* Now we need to setup the data base so run `python manage.py makemigrations`.
* Followed by `python manage.py migrate`.
* Create a superuser account on the app with `python manage.py createsuperuser` and input the required data (a username, an email address and a password twice).
* Create a wav file called 'test_audio.wav' with you saying "What's the capital of France". Copy this file into the `project_apps/chats/tests` directory. This is for some of the tests.
* Run `python manage.py collectstatic` from the terminal to prepare for accessing the app.
* Now you can run the tests to check the project runs OK.
* In the `.vscode` directory note that there is a file in here called 'launch.json'.
* This file defines two methods for running the python debugger in VS Code. One called 'Django Server', the other called 'Django Tests'. 
* To run the test suite enter `python manage.py test` in the terminal. The terminal will appear to freeze. To run the test suite you will need to start the 'Django Tests' version of the debugger so ensure that 'Django Tests' is selected on the 'Run and Debug' view in VS Code, and then click the start dubugging button at the top or press F5.
* These should run fine but you may have some issues running tests associated with calls to AI models.
* **NOTE:** If you have any issues running tests relating to AI access I have found 'Reopen folder locally' and then 'Reopen in container' seems to fix the problem. If you are using GitHub Copilot and have issues, the same process seems to fix this problem.
* Note that AIModel instances for actual AI access are using openrouter.ai (see **project_apps.chats.tests.tests_noa_endpoint.NOAMultiModalEndpointTests.test_valid_request_with_audio**) - this may also cause failures in specific tests because you're not set up for openrouter or will want to use a different provider. Change the tests to reflect your access approach.
* Unfortunately there can be intermittent issues with the tests accessing an AI and when the tests are run individually the error doesn't appear and then running the suite again the problem doesn't arise.
* There can also be issues with the tests if you have run out of credit or hit a usage limitation of some form. They are assuming that there is no access issue.
* If there are only issues on accessing the AI, you may find the app is still useable.

## Running AIUI

* When I develop I like to run pretty close to a production environment, so the project is set to run as it is meant to run in production. This means settings such as `SECURE_SSL_REDIRECT` are set to use only `HTTPS` and this doesn't work well with Django development server (runserver) that is started in the docker-compose.yml file. In development I like the convenience of the development server.
* To get around this I use tunnelling software (specifically NGROK - https://ngrok.com/). This is a great piece of software that accepts HTTPS requests but will forward them as HTTP. I run it with `ngrok http 8000`. 
* You'll see something like below. CTRL + Click on the forwarding link. This should open the AIUI in the web interface.

```bash
ngrok                                                                                                                               (Ctrl+C to quit)
                                                                                                                                                    
🧠 Call internal services from your gateway: https://ngrok.com/r/http-request                                                                       
                                                                                                                                                    
Session Status                online                                                                                                                
Account                       Simon Snowden (Plan: Free)                                                                                            
Version                       3.26.0                                                                                                                
Region                        United States (us)                                                                                                    
Latency                       120ms                                                                                                                 
Web Interface                 http://127.0.0.1:4040                                                                                                 
Forwarding                    https://640790e66cf0.ngrok-free.app -> http://localhost:8000                                                          
                                                                                                                                                    
Connections                   ttl     opn     rt1     rt5     p50 
                              p90                                                                           
                              0       0       0.00    0.00    0.00    
                              0.00                                                                          
```

* Sign in with the superuser you created when you initialised the app.
* Now you will be at the home screen for the app asking you to start your first chat.
* Before you can do that you need to add your first model. Open the side navigation and click on Models.
* Now you can add your first model.
* Typical entries for the model settings can be found in the test **project_apps.chats.tests.tests_noa_endpoint.NOAMultiModalEndpointTests.test_valid_request_with_audio**.
* Once you have set up your first AI model successfully you can start to chat through the web interface.

## NOA and BrilliantLabs Frame Interface

This section provides guidance on the NOA API implementation for integration with BrilliantLabs Frame AR glasses, based on the code in project_apps.chats.api.views.py.

### Overview

The NOA API endpoint is designed to mimic the official NOA API, allowing multimodal requests (text, audio, image) from the Frame glasses or NOA app. It processes incoming data, interacts with an AI model, and returns structured responses.

### Using with the NOA App for the BrilliantLabs Frame AR glasses

There are a number of steps to ensuring that this works.

1. Ensure that the NOA app is installed on your device and the glasses are paired and working correctly with the Noa Server (the default option). If they are not working with the NOA server you have no chance of them working with this server.
2. Once you are happy the glasses are working fine, launch the AIUI app, whether in test mode or as a deployed service.
3. Try sending a simple post request to the app on its endpoint (e.g. <https://app.address/mm/mm/>) using a service such as Postman, Thunder Client or curl from the command line. Your should recieve something like:

```json
{
  "detail": {
    "local_time": [
      "This field may not be blank."
    ],
    "address": [
      "This field may not be blank."
    ]
  }
}
```

4. You could send a get request via your broswer (simply put the address in your browser) and you'll recieve a HTTP 405 Method not allowed. You should also have a web page returned that allows you to make a post request. If you click the `POST` button you should recieve the above in some form.
5. Now to setup the Noa app on your device to work with the app.
6. Open the app and choose the 'HACK' option at the bottom.
7. On this screen you should now see that the 'Noa Server' option has been chosen (the default official server for the glasses). Also on the screen the system prompt, Temperature, Response length, Text to speech, and Promptless options (this is on the iOS app - not so sure about others).
8. Now on the top slider choose Custom Server Option rather than the Noa Server.
9. You will now see text boxes for 'API Endpoint', 'API Header Key' and 'API Header Value'.
10. In the 'API Endpoint' text box put the same address that you used previously when testing the endpoint was live.
11. In the 'API Header Key' text box type `Content-Type`.
12. And in the 'API Header Value' type `application/json`.
13. You are now are ready to go.
14. Send a request using the glasses as per the glasses instructions. Try something simple at first such as 'What's the captial of France'.
15. The answer should then appear in your glasses prism.
16. On the chat screen you should see it displaying the request you made and the answer that you recieved.

### Endpoint

* Path: /mm/mm/ (example; confirm with your routing)
* Method: POST
* Authentication: Not required (anonymous access)

### Request Format

The API accepts multipart/form-data or form-encoded requests. Key fields:

* prompt: Text prompt from the user.
* audio: (optional) Audio file (WAV format recommended) for speech-to-text.
* image: (optional) Image file for vision features.
* location: (optional) User location/address.
* time: (optional) Local time.
* messages: (optional) JSON array of message history.

Example using curl:

```bash
curl -X POST <API_URL> \
  -F "prompt=What's the capital of France?" \
  -F "audio=@/path/to/audio.wav" \
  -F "image=@/path/to/image.jpg"
```

### Processing Steps

1. Data Extraction: The endpoint parses incoming fields and files.
2. Audio Transcription: If audio is provided, it uses Whisper to transcribe speech to text.
3. Image Handling: If image is provided, it is logged and can be processed for vision features.
4. Prompt Construction: Combines prompt and transcribed audio.
5. AI Model Response: Uses the configured AI model (openai/gpt-oss-20b:free by default) to generate a reply.
6. Conversation Logging: Optionally saves the conversation (thread/item) for analytics or history.
7. Response Formatting: Returns a structured JSON response.

### Response Format

A typical response includes:

```json
{
  "user_prompt": "<full user prompt>",
  "message": "<AI-generated response>",
  "debug": {
    "topic_changed": false
  }
}
```

Additional fields (like token usage, timings, or image analysis) can be added as needed.

### Error Handling

* Invalid JSON or missing fields result in a 400 Bad Request.
* Server errors return a 500 Internal Server Error with details.

### Customization

* The AI model can be changed by updating aimodel_name in the view.
* Extend the endpoint to process more multimodal data (e.g., GPS, vision, assistant model).
* Add authentication or user tracking if needed.

## Integration Tips

* Ensure the NOA app or Frame glasses POST to the correct endpoint with required headers (Content-Type: multipart/form-data).
* For audio, use WAV format for best Whisper compatibility.
Test with tools like Postman or curl before integrating with hardware.

**The rest of the documentation will deal with operational issues.**

## Testing the project

### Running and debugging tests

* You will need to record a wav file called test_audio/wav and save it to the `project_apps/chats/tests` directory.
* Make sure that you have a model provider for tests that actually call an ai model.
* Running tests follows the usual python pattern e.g. `python manage.py test project_apps.chats.tests` will run all tests for the 'chats' app, `python manage.py test project_apps.aimodels.tests.AIModelCRUDTest.test_model_generate_ai_response` will run the very specific test `test_model_generate_ai_response` in the 'aimodels' app. 
* Always remember to start the debugger once you have entered the test command.

### Running and debugging the server.

* Run the interface as described above with ngrok. In the 'Run and Debug' view in VS Code select the 'Django Server' debugger and run it.
* You can now set breakpoints in the code and when actuating the approrpiate point in the interface it will trigger the breakpoint so you can see what is going on.

### Trouble shooting tests

* Sometimes when running a test that actually calls an LLM there may be fails. Make sure that you have the test model setup correctly and an `OPEN_AI_MODEL_KEY` set up in the `.env` file. This doesn't have to be a ChatGPT model, this is simply about the `openai` library so can be for any provider (e.g. I use openrouter.ai). Also make sure you have the right endpoint for the ai provider you are using.
* If you have a test model setup correctly and still get fails, it may be due to usage limits being reached.

## Creating documentation

Make sure all project apps documentation files (found in the 'docs' directory for each app under 'project_apps') are added to the 'modules' directory and then included in the index.rst in the docs folder below:

To make the necessary documentation:

* From the terminal go to the 'docs' directory with `cd /app/docs`.
* Then run the command `make html` and the documentation will be automatically built and saved in the '_build' directory off the 'docs' directory.

## Environment Variables

There are two ways to set environment variables, the first is through the `docker-compose` file and the second is through an `.env` file.

### docker-compose File

In the web service definition there will be an additional environment section detailing the environment variables.

``` yaml
  web:
    depends_on:
      - db
    environment:
        - "DJANGO_SECRET_KEY=<YOUR_SECRET>"
        - "DJANGO_ADMIN=admin/"
        - "DJANGO_DEBUG=True"
        - "DJANGO_ALLOWED_HOSTS=457-81-102-151-57.ngrok-free.app,localhost,127.0.0.1,"
        - "SECURE_HSTS_SECONDS=0"
        - "SECURE_HSTS_INCLUDE_SUBDOMAINS=False"
        - "SECURE_HSTS_PRELOAD=False"
        - "SESSION_COOKIE_SECURE=False"
        - "CSRF_COOKIE_SECURE=False"
```

In the `settings.py` file in the config folder the python will look like this.

```python
from environs import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()
```

### .env File

The environment variables would be removed from the `docker-compose` file if they already exist and a .env file in the project root created that looks like this (it includes MySQL environment variables if using this db - see below):

```text
DJANGO_SECRET_KEY=<YOUR_SECRET>
OPEN_AI_MODEL_KEY=<YOUR_Provider_Key>
ESK=<IFUSINGENCRYPTION>
DJANGO_ADMIN=admin/
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*,localhost,127.0.0.1,
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
DJANGO_SETTINGS_MODULE=aiui_config.settings
```

In the `settings.py` file in the config folder the python will look like this.

```python
from environs import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(os.path.join(BASE_DIR, ".env"))
```

## Databases

This runs with Postgres (default) and MySQL. From the cuttiecutter the projects run with postgres out of the box. However, when running on certain platforms (e.g. pythonanywhere's free tier) we may only have access to MySQL and so will need to make changes to the database settings in the `settings.py` file.

With the postgres setup the settings will look like this...

```python
DATABASES = {
    "default": env.dj_db_url("DATABASE_URL", default="postgres://postgres@db/postgres")
}
```

...and the `docker-compose` file will have a db service like this.

```yaml
  db:
    image: postgres:13.1
    environment:
      - "POSTGRES_HOST_AUTH_METHOD=trust"
  selenium:
    image: selenium/standalone-chrome-debug:latest
    volumes:
      - /dev/shm:/dev/shm
    ports:
      - 4444:4444
      - 5900:5900
```

For MySQL the settings will change to...

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("MYSQL_DATABASE"),
        "USER": env("MYSQL_USER"),
        "PASSWORD": env("MYSQL_PASSWORD"),
        "HOST": env("MYSQL_HOST"),
        "PORT": env("MYSQL_PORT"),
        "default-character-set": "utf8",
        "OPTIONS": {
            "sql_mode": "traditional",
        },
        "TEST": {
            "NAME": "test_mysql_db",
        },
    }
}
```

...and the db service in the `docker-compose` file will change to this...

```yaml
  db:
    image: mysql:8
    ports:
      - "3306:3306"
    environment:
      - MYSQL_DATABASE=mysql_db
      - MYSQL_USER=mysqlboss
      - MYSQL_PASSWORD=testpass123
      - MYSQL_ROOT_PASSWORD=testpass456
      - MYSQL_HOST=localhost
      - MYSQL_ROOT_HOST=%
      - MYSQL_PORT=3306
```

...with the necessary settings to access the database on the db service as shown in the `.env` file section above.

We also need to add the `mysqlclient` python package to the pipfile. Do this by first opening in the dev container, then run `pipenv install mysqlclient`. This will install a virtual environment and then install `mysqlclient` in the virtual environment. The `mysqlclient` python package will now be in the `Pipfile` and the `Pipfile.lock` will be updated with the latest dependencies. Running `pipenv --rm` will now remove this virtual environment.

We have now updated dependencies for the project for rebuilds of the devcontainer or bilding future containers when hosting on external services for deployment. However, it is still not installed in the dev container. Using `pip list` will show that the local environment doesn't have it. So run `pip install mysqlclient` to install the `mysqlclient` package into the dev container.

Once the containers have been rebuilt perform `migrate` to generate database tables. There may be significant errors at this point due to differences between PostGres and MySQL if you are migrating between the two. You will have to track these down individually. It may also be necessary to delete exisiting migrations and perform `makemigrations` again

When running with MySql we need to make sure our db user has the ability to
create the test database when running tests. At the intial creation of the project containers
(such as at the intial creation of a project or after a docker-comose down command) we need
to go into a shell for the db container and starting mysql with `mysql -u root -p` and
provide the db root password when requested. Then in the shell we need to:

```sql
    GRANT ALL PRIVILEGES ON test_mysql_db.* TO 'mysqlboss'@'%';
    SHOW GRANTS FOR 'mysqlboss'@'%';
    +--------------------------------------------------------------+
    | Grants for mysqlboss@%                                       |
    +--------------------------------------------------------------+
    | GRANT USAGE ON*.*TO `mysqlboss`@`%`                        |
    | GRANT ALL PRIVILEGES ON `mysql\_db`.* TO `mysqlboss`@`%`     |
    | GRANT ALL PRIVILEGES ON `test_mysql_db`.* TO `mysqlboss`@`%` |
    +--------------------------------------------------------------+
```

or from the terminal once attached to the db container:

```bash
mysql -uroot -ptestpass456 -e "GRANT ALL PRIVILEGES ON test_mysql_db.* TO 'mysqlboss'@'%';"
mysql -uroot -ptestpass456 -e "SHOW GRANTS FOR 'mysqlboss'@'%';
```

NOTE: Before and after this operation run a full test suite and make sure all tests are working.

## Upgrading Dependencies

To upgrade dependencies (specified in the Pipfile) use the following process.

1. Back up pipfile and piplock
2. Open the dev container.
3. Grab the current state of python packages `pip list > requirements-old.txt`.
4. Update each individual package and run tests after update - `pip install <package> --upgrade`.
5. If a fail in tests either fix or revert to the version in original found in the requirements file made in (3).
6. If errors fixed, make a new list of the python packages `pip list > requirements-old.txt`, take the version number of the updated package and put this in the Pipfile if necessary.
7. You also need to install each using pipenv to keep the pipfile uptodate. Do this by `pipenv install <package>`. This will install a virtual environment and then install the package in the virtual environment. The python package will now be in the `Pipfile` and the `Pipfile.lock` will be updated with the latest dependencies. Running `pipenv --rm` will now remove this virtual environment. Then to install in the system `pipenv install --system --dev`.
8. Before installing latest Django run python Wa manage.py test to look for deprecation warnings and make changes.
9. After installing latest Django run python Wa manage.py test to look for deprecation warnings and make changes.
10. And test once more (but will probably require a full rebuild on dev systems).

NOTE: At the moment pipenv cannot install the OpenAI library so you need to install it manually using pip with the command `pip install openai`. This will need to be done every time the python conatainer is rebuilt.

NOTE: At the moment pipenv cannot install the `openai-whisper` library so you need to install it manually using pip with the command `pip install openai-whisper`. This will need to be done every time the python conatainer is rebuilt. Don't forget to install the ffmpeg library if not already installed. To do this `apt-get update` followed by `apt-get install ffmpeg`

## Database Field Encryption

This is only for converting an existing field to an encrypted field.

1. Ensure django-crytography is installed (see Upgrading Dependencies).
2. Set up an new env variable `ESK=<secret-key>` in .env file.
3. Add `CRYPTOGRAPHY_KEY = env("ESK")` to settings.py.
4. To double check the process has worked you can use a mysql session to look at changes to the relevant database table. Attach shell to database container and open a mysql session with `mysql -u root -p mysql_db` and enter the password when requested.
5. To see the tables for the database `SHOW TABLES;`.
6. To see the contents of the table `SELECT * FROM tabel_name;`. Do this before and after the rest of the process to see the encrypted fields being encrypted.
7. In app models.py change the field to be encrypted to have te prefix `old_`. Also change any reference to this field in forms.py and admin.py to this new name or any migrations won't work.
8. Run `python manage.py makemigrations`.
9. This will ask if you wish to rename the field name. Select y for yes.
10. This will generate a migrations file that looks something like this.

```python
# Generated by Django 4.2.13 on 2024-10-04 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('situations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='situation',
            old_name='description',
            new_name='old_description',
        ),
    ]
```

11. In the models.py file import the django-cryptography library `from django_cryptography.fields import encrypt`.
12. Next create code for the new encrypted version of the field. It will look like:

```python
  old_description = models.TextField(
      blank=False, null=False, verbose_name="Situation Statement"
  )
  description = encrypt(
      models.TextField(blank=False, null=False, verbose_name="Situation Statement")
  )
```

13. Run `python manage.py makemigrations`.
14. If this is set to `blank=False, null=False` you will be asked to provide a default. Choose option 1 and default value 'encrypting'.
15. This will create a migrations file that looks like this:

```python
# Generated by Django 4.2.16 on 2024-10-04 08:46

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('situations', '0002_rename_description_situation_old_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='situation',
            name='description',
            field=django_cryptography.fields.encrypt(models.TextField(default='encrypting', verbose_name='Situation Statement')),
            preserve_default=False,
        ),
    ]
```

16. Now we need to copy the data from the old field to the new one. We also need to ensure that the process can be reversed.
17. To do this run `python manage.py makemigrations --empty yourappname`
18. This will generate a migrations file that looks something like this:

```python
# Generated by Django 4.2.16 on 2024-10-04 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('situations', '0003_situation_description'),
    ]

    operations = [
    ]
```

19. This now needs changing to this:

```python
# Generated by Django 4.2.16 on 2024-10-04 08:51

from django.db import migrations


def forwards_encrypted_char(apps, schema_editor):
    EncryptedCharModel = apps.get_model("situations", "Situation")

    for row in EncryptedCharModel.objects.all():
        row.description = row.old_description
        row.save(update_fields=["description"])


def reverse_encrypted_char(apps, schema_editor):
    EncryptedCharModel = apps.get_model("situations", "Situation")

    for row in EncryptedCharModel.objects.all():
        row.old_description = row.description
        row.save(update_fields=["old_description"])


class Migration(migrations.Migration):

    dependencies = [
        ("situations", "0003_situation_description"),
    ]

    operations = [migrations.RunPython(forwards_encrypted_char, reverse_encrypted_char)]
```

20. Finally we need to remove the old_ version of the field from the models.py and change the field reference in forms.py and admin.py back to the original.
21. Run `python manage.py makemigrations`.
22. To build these changes in now run `python manage.py migrate`.
23. If you look at the raw table for the model you will see it is now encrypted.
24. The server may need to be restarted by `Reopen Folder Locally` followed by `Reopen Container` if the test server crashes.
25. Run tests and fix anything if failing.
26. Before running this on the production server backup the production database.
27. Do do this from a console on the production server run `mysqldump -u annelofthouse3 -h annelofthouse3.mysql.eu.pythonanywhere-services.com --set-gtid-purged=OFF --no-tablespaces 'annelofthouse3$default'  > db-backup.sql`.
28. When you deploy these changes to the production server ensure that the `ESK` entry is in the .env file.

## A last message.

There is a lot here to get your head around. Take your time, have a good nose around the codebase and get an understanding of how it all works and fits together. Then start experimenting.

I really do hope some of you find this useful.

All the best.

Simon Snowden 2025.