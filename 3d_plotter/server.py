import os
from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import cv2 as cv
from edge_detect import adjust_image, save_canny_img, find_contours
from celery import Celery


UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = b'f89hsad8fh032n39f'
celery = Celery(app.name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0', task_ignore_result=False)


def fetch_img_filenames(wrap_size=5):
    drawables_location = os.getcwd() + '/static'
    files = os.listdir(drawables_location)
    non_adjusted = list(filter(lambda x: 'adjusted' not in x and '__canny_temp' not in x, files))
    return [non_adjusted[i:i+wrap_size] for i in range(0, len(non_adjusted), wrap_size)]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = run_plotter.AsyncResult(task_id)
    if task.state == 'DRAWING':
        response = {
            'state': task.state,
            'total_contours': task.info.get('total_contours'),
            'contours_completed': task.info.get('contours_completed'),
            'positions': task.info.get('positions')
        }
    else:
        response = {
            'state': task.state
        }
    return jsonify(response)


@celery.task(bind=True)
def run_plotter(self):
    working_img = cv.imread('/home/pi/personal/3d_plotter/static/__canny_temp.png', cv.IMREAD_GRAYSCALE)
    print(working_img.dtype)
    print(working_img.shape)
    contours = find_contours(working_img)
    plotter = Plotter(contours, telemetry=self)
    plotter.calibrate()
    plotter.draw()
    return {'state': 'FINISHED'}


@app.route('/submit-job', methods=['POST'])
def submit_job():
    task = run_plotter.apply_async()
    return jsonify({}), 202, {'Location': url_for('task_status', task_id=task.id)}


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
    app.run(host='0.0.0.0', debug=True)
