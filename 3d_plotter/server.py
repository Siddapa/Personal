import os
from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import cv2 as cv
from edge_detect import adjust_image, save_canny_img, find_contours
from multiprocessing import Process, Manager, Value
from plotting.plotter import Plotter
from time import sleep
from ctypes import c_wchar_p


UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = b'f89hsad8fh032n39f'
plot_state = Manager().dict()
next_state = Value('i', -1)


def fetch_img_filenames(wrap_size=5):
    drawables_location = os.getcwd() + '/static'
    files = os.listdir(drawables_location)
    non_adjusted = list(filter(lambda x: 'adjusted' not in x and '__canny_temp' not in x, files))
    return [non_adjusted[i:i+wrap_size] for i in range(0, len(non_adjusted), wrap_size)]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run_job():
    working_img = cv.imread(UPLOAD_FOLDER + '__canny_temp.png', cv.IMREAD_GRAYSCALE)
    contours = find_contours(working_img)
    plotter = Plotter(contours, plot_state)
    while 1:
        if next_state.value == 1:
            plotter.calibrate()
        elif next_state.value == 2:
            plotter.draw_image(next_state)
            break
        next_state.value = -1
        sleep(0.01)
    plot_state['state'] = 'FINISHED'


@app.route('/status', methods=['GET'])
def status():
    return jsonify(dict(plot_state))


@app.route('/update-job', methods=['POST'])
def update_job():
    new_state = request.json['next_state']
    if new_state == 'INIT PLOTTER':
        task = Process(target=run_job)
        task.start()
        next_state.value = 0
    elif new_state == 'CALIBRATE':
        next_state.value = 1
    elif new_state == 'START':
        next_state.value = 2
    elif new_state == 'PAUSE':
        next_state.value = 3
    elif new_state == 'RESUME':
        next_state.value = 4
    elif new_state == 'STOP':
        next_state.value = 5
    return jsonify({}), 202, {}


@app.route('/gen-canny-img', methods=['POST'])
def gen_canny_img():
    if request.json != None:
        img_name = request.json['img_name'].split('/')[-1]
        working_img = cv.imread(UPLOAD_FOLDER + 'adjusted_' + img_name, cv.IMREAD_GRAYSCALE)

        save_canny_img(working_img, int(request.json['lower_thresh']), int(request.json['upper_thresh']))
        return "Saved"
    return "Didn't Save"


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'new_img' not in request.files:
            return redirect(request.url)

        img = request.files['new_img']
        if img.filename == '':
            return redirect(request.url)

        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            img.save(UPLOAD_FOLDER + filename)

            adjusted_img = adjust_image(cv.imread(UPLOAD_FOLDER + filename), (5, 5))
            cv.imwrite(UPLOAD_FOLDER + 'adjusted_' + filename, adjusted_img)
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', images=fetch_img_filenames())


if __name__ == '__main__':
    app.run(host='192.168.68.128', port=5000)
