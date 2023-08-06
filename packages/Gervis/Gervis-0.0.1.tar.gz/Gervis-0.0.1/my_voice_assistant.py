import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import JarvisAI
import re
import pprint
import random

obj = JarvisAI.JarvisAssistant()

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'gervis' in command:
                command = command.replace('gervis', '')
                print(command)
    except:
        pass
    return command


def run_gervis():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'google photos' in command:
        photos = obj.show_google_photos()
        print(photos)
    elif 'your name|who are you' in command:
        print("My name is gervis, I am your personal assistant")
        talkt("My name is gervis, I am your personal assistant")
    elif 'what can you do' in command:
        li_commands = {
            "open websites": "Example: 'open youtube.com",
            "time": "Example: 'what time it is?'",
            "date": "Example: 'what date it is?'",
            "launch applications": "Example: 'launch chrome'",
            "tell me": "Example: 'tell me about India'",
            "weather": "Example: 'what weather/temperature in Mumbai?'",
            "news": "Example: 'news for today' ",}
        ans = """I can do lots of things, for example you can ask me time, date, weather in your city,I can open websites for you, launch application and more. """
        print(ans)
        pprint.pprint(li_commands)
        talk(ans)
    elif 'how are you' in command:
        li = ['good', 'fine', 'great']
        response = random.choice(li)
        print(f"I am {response}")
        talk(f"I am {response}")
    elif 'hello' in command:
        print('Hi')
        talk('Hi')
    elif 'launch'in command:
        dict_app = {
        'chrome': 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        'epic games': 'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe'}

        app = res.split(' ', 1)[1]
        path = dict_app.get(app)
        if path is None:
            talk('Application path not found')
            print('Application path not found')
        else:
            talk('Launching: ' + app)
            obj.launch_any_app(path_of_app=path)
    elif 'open' in command:
        domain = res.split(' ')[-1]
        open_result = obj.website_opener(domain)
        print(open_result)
    elif 'tell me about' in command:
        topic = res[14:]
        wiki_res = obj.tell_me(topic, sentences=1)
        print(wiki_res)
        talk(wiki_res)
    elif 'news' in command:
        news_res = obj.news()
        pprint.pprint(news_res)
        talk("I have found {len(news_res)} news. You can read it. Let me tell you first 2 of them")
        talk(news_res[0])
        talk(news_res[1])
    elif 'weather|temperature' in command:
        city = res.split(' ')[-1]
        weather_res = obj.weather(city=city)
        print(weather_res)
        talk(weather_res)
    elif 'local photos' in command:
        photos = obj.show_me_my_images()
        print(photos)
    elif 'setup|set up' in command:
        setup = obj.setup()
        print(setup)
    elif 'exit|quit|goodbye ' in command:
        talk("Have a great day sir.")
        exit()
    else:
        talk('Please say the command again.')


while True:
    run_gervis()