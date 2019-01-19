from flask import Flask, request, send_file, send_from_directory, url_for, redirect
from flask import render_template
from werkzeug import secure_filename
import image_slicer
import io
import zipfile
import os, sys

app = Flask(__name__)


fileName = ""

sliced = None

mas = []
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        global fileName
        fileName = file.filename
        sliced_size = int(request.form['tentacles'])
        file.save(secure_filename(file.filename))

        sliced_array = image_slicer.slice(file.filename, sliced_size)
        global sliced
        sliced = sliced_array

    return render_template('display.html', files = sliced_array, image_added=False)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("./", filename)


@app.route('/add_image/<file>')
def add_image(file):
        global mas
        mas.append(file)
        return render_template('display.html', files = sliced, image_added=True, f = mas)

def remove():
    os.system("rm *.png")
    os.system("rm *.jpg")
    
@app.route('/save_zip', methods=['GET', 'POST'])
def save_zip():
    if request.method == 'POST':
        global mas
        fileN = request.form['zipName'] + ".zip"
        print(fileN)
        with zipfile.ZipFile(fileN, 'w') as zip:
            for tile in sliced:
                print(tile)
                for pic in mas:
                    print(pic)
                    if pic == str(tile.filename):
                        with io.BytesIO() as data:
                            tile.save(data)
                            zip.writestr(tile.generate_filename(path=False),
                                         data.getvalue())
        mas = []
        remove()
        return "Saved"
    else:
        remove()
        return "didn't save zip"

if __name__ == '__main__':
    app.run(debug=True)
