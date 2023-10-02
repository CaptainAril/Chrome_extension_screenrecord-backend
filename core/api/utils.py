import moviepy.editor as mp
import speech_recognition as sr

def transcribeVideo(video_path):
    vid = mp.VideoFileClip(video_path)
    vid.audio.write_audiofile('temp.wav')

    r = sr.Recognizer()

    with sr.AudioFile('temp.wav') as source:
        r.adjust_for_ambient_noise(source)
        data = r.record(source)
    
    try:
        text = r.recognize_google(data)
    except sr.UnknownValueError:
        return "Could not understand audio!"
    except sr.RequestError as e:
        return f'Could not request results; {e}'
    
    return text