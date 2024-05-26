import os
from flask import Flask, render_template, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import cv2 as cv
from edge_detect import EdgeDetect


UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = b'f89hsad8fh032n39f'


def fetch_img_filenames(wrap_size=5):
    drawables_location = os.getcwd() + '/static'
    files = os.listdir(drawables_location)
    non_adjusted = list(filter(lambda x: 'adjusted' not in x and '__canny_temp' not in x, files))
    return [non_adjusted[i:i+wrap_size] for i in range(0, len(non_adjusted), wrap_size)]

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/gen-canny-img', methods=['POST'])
def gen_canny_img():
    if request.json != None:
        img_name = request.json['img_name'].split('/')[-1]
        working_img = cv.imread(UPLOAD_FOLDER + 'adjusted_' + img_name, cv.IMREAD_GRAYSCALE)

        detector = EdgeDetect(working_img)
        detector.save_canny_img(request.json['lower_thresh'], request.json['upper_thresh'])
        return 'Saved'
    return "Didn't Save"


@app.route('/submit-job', methods=['GET'])
def submit_job():
    detector = EdgeDetect(cv.imread(UPLOAD_FOLDER + '__canny_temp.png'))
    detector.find_contours()

    plotter = Plotter()



@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'new_img' not in request.files:
            flash('No file part')
            return redirect(request.url)

        img = request.files['new_img']
        if img.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            img.save(UPLOAD_FOLDER + filename)

            detector = EdgeDetect(cv.imread(UPLOAD_FOLDER + filename))
            detector.adjust_image((5, 5))
            cv.imwrite(UPLOAD_FOLDER + 'adjusted_' + filename, detector.img)
            return redirect(url_for('upload_image'))

    return render_template('submit_job.html', images=fetch_img_filenames())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
