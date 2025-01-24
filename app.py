from flask import Flask, render_template, request
import numpy as np
import os
import tempfile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the model
model = load_model('./models/apple-224.h5')

def model_predict(img_path, model):
    test_image = image.load_img(img_path, target_size=(224, 224))
    test_image = image.img_to_array(test_image)
    test_image = test_image / 255.0
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    return result

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        image_file = request.files['file']
        tmp.write(image_file.read())
        tmp_path = tmp.name
    
    # Make prediction
    result = model_predict(tmp_path, model)
    
    # Clean up
    os.unlink(tmp_path)

    categories = ['Healthy', 'Multiple Disease', 'Rust', 'Scab']
    pred_class = np.argmax(result)
    output = categories[pred_class]
    
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
