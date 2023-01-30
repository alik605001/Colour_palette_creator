import matplotlib.pyplot as plt
from sklearn import cluster
import numpy as np
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images/"
Bootstrap(app)


def rgb_to_hex(r,g,b):
    return '#%02x%02x%02x' % (r,g,b)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/result',  methods=['GET', 'POST'])
def result():
    num = int(request.form.get('num'))
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image_path = f"static/images/{file.filename}"
    img = plt.imread(image_path)

    if num <= 0:
        num = 5

    clust = cluster.KMeans(n_clusters=num)
    clust.fit(img.reshape(-1, 3))

    colours = clust.cluster_centers_
    if num >= 30:
        height = 700
    else:
        height = 500
    col_bar = np.zeros((height, 150, 3), np.uint8)
    steps = height / num

    cols = []

    for idx, col in enumerate(colours):
        plt.axis('off')
        col_bar[int(idx * steps):(int((idx + 1) * steps)), :, :] = col
        hex_code = rgb_to_hex(int(col[0]), int(col[1]), int(col[2]))
        plt.text(x=5, y=((idx * steps)+steps), s=hex_code, fontsize='small')
        c = [(col[0], col[1], col[2]), hex_code]
        cols.append(c)
    plt.imshow(col_bar)
    fig = plt.savefig('static/images/colours.jpg')
    plt.close()
    return render_template('result.html', colours=cols, img=image_path, final=fig)


if __name__ == "__main__":
    app.run(debug=True)
