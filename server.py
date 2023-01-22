from flask import Flask, render_template, request, url_for
import threading
from io import BytesIO
import base64
import banana_dev as banana

app = Flask(__name__)



transciptions = []

@app.route("/")
def home():
    return render_template("index.html", transciptions=transciptions)

def transcribe(path):
    global transciptions
    print("STARTING")

    api_key = "9318c758-09a8-4cc5-810f-65d48571baa4"
    model_key = "8dc38f14-f4f8-4b07-b1fc-ea29d7c1d83f"

    # Expects an mp3 file named test.mp3 in directory
    with open(path, 'rb') as file:
        mp3bytes = BytesIO(file.read())
    mp3 = base64.b64encode(mp3bytes.getvalue()).decode("ISO-8859-1")

    model_payload = {"mp3BytesString": mp3}

    out = banana.run(api_key, model_key, model_payload)["modelOutputs"][0]["text"]
    transciptions.append(out)


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

