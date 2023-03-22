from flask import Flask, request, render_template, jsonify
from flask.helpers import send_file
from transformers import AutoProcessor, AutoModelForCausalLM
import requests
from PIL import Image

app = Flask(__name__, static_url_path='/', static_folder='web')


@app.route("/")
def indexPage():
    return send_file("web/index.html")

@app.route('/upload', methods=['POST'])
def upload_image():
    processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")

    #url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    #image = Image.open(requests.get(url, stream=True).raw)

      # Get the uploaded image from the request
    image_file = request.files['image']
    
    image = Image.open(image_file)
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_caption)
       
    # Save the image to disk (optional)
    image_file.save('uploaded_image.jpg')
    
    # Do something with the image (e.g. process, analyze, etc.)
    # ...

    # Return a response (optional)
    return jsonify({
        "generated_caption": generated_caption,
    })