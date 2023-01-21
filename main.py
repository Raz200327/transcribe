import whisper
from flask import Flask, render_template, request, url_for
import threading

app = Flask(__name__)



transciptions = []

@app.route("/")
def home():
    return render_template("index.html", transciptions=transciptions)

def transcribe(path):
    global transciptions
    print("STARTING")
    model = whisper.load_model("base")
    result = model.transcribe(path)
    transcription = result["text"]
    transciptions.append(transcription)
    print("DONE")



@app.route("/whisper-transcribe", methods=["GET", "POST"])
def find_files():
    if request.method == "POST":

        #Saving audio
        audio = request.files["audio"]
        filename = audio.filename
        audio.save(f"./audio/{filename}")
        path = f"./audio/{filename}"

        threading.Thread(target=transcribe, kwargs={"path": path}).start()
        #transcribing audio
        return render_template("success.html")



if __name__ == "__main__":
    app.run(debug=True)

