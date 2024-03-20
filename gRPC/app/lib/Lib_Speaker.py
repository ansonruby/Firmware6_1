from threading import Thread
import subprocess
import time
import os
from gtts import gTTS

CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class SpeakThread(Thread):
    text = ""

    def __init__(self, msg):
        Thread.__init__(self)
        self.msg = msg
        self.audio_path = CURRENT_DIR_PATH + "/audio/"

    def create_audio_folder(self):
        if not os.path.exists(self.audio_path):
            os.makedirs(self.audio_path)

    def write_audio_file(self, audio, reset):
        file_name = self.audio_path + "audio.mp3"

        if reset:
            file = open(file_name, 'wb')
            file.write(b'')
            file.close()

        file = open(file_name, 'ab')
        file.write(audio)
        file.close()
        return

    def write_tts_file(self, text):
        audio_name = "voz_" + str(int(time.time() * 1000)) + ".mp3"
        file_name = self.audio_path + audio_name
        language = 'es'
        tld = 'com.mx'
        myobj = gTTS(text=text, lang=language, tld=tld,
                     slow=False, lang_check=False)
        myobj.save(file_name)
        return audio_name

    def reproduce_audio(self, name, prio, delete_file):
        repetitions = prio if prio > 0 else 1

        file_name = self.audio_path + name + ".mp3"
        if os.path.exists(self.audio_path):
            for _ in range(repetitions):
                subprocess.call(["cvlc", "--alsa-audio-device", "hw:1,0", "--play-and-exit", file_name],
                                stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
            if delete_file:
                os.remove(file_name)

    def run(self):
        text = self.msg["message"]
        prio = self.msg["priority"]
        audio = self.msg["audio"]
        audio_name = ""
        delete_file = False
        self.create_audio_folder()

        if audio:
            return self.write_audio_file(audio, text == "¡audio", prio)

        if text.startswith("!"):
            audio_name = text.split("!")[1]
        else:
            delete_file = True
            audio_name = self.write_tts_file(text)

        return self.reproduce_audio(audio_name, prio, delete_file)


speak_threads = []


def send_speaker_msg(msg):
    if len(speak_threads) > 0:
        speak_thread = speak_threads.pop()
        if speak_thread and speak_thread.is_alive():
            if msg['message'] == speak_thread.msg['message']:
                speak_threads.append(speak_thread)
                return

            time.sleep(0.5)

    new_speak_thread = SpeakThread(msg)
    new_speak_thread.daemon = True
    new_speak_thread.start()
    speak_threads.append(new_speak_thread)
