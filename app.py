from flask import Flask, request, jsonify
from flask.helpers import send_file
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import subprocess
import sys

app = Flask(__name__, static_url_path='/', static_folder='web')

    
@app.route("/")
def indexPage():
    return send_file("web/index.html")

@app.route('/upload', methods=['POST'])
def upload_image():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
    processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")

      # Get the uploaded image from the request
    image_file = request.files['image']
    
    image = Image.open(image_file)
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_caption)
       
    # Save the image to disk (optional)
    #image_file.save('uploaded_image.jpg')

    return jsonify({
        "generated_caption": generated_caption,
    })