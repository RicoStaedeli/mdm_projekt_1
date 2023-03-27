from flask import Flask, request, jsonify
from flask.helpers import send_file
# from PIL import Image
# from transformers import AutoProcessor, AutoModelForCausalLM
from transformers import SegformerFeatureExtractor, SegformerForImageClassification
from PIL import Image

app = Flask(__name__, static_url_path='/', static_folder='web')

    
@app.route("/")
def indexPage():
    return send_file("web/index.html")

@app.route('/upload', methods=['POST'])
def upload_image():
    
    # Get the uploaded image from the request
    image_file = request.files['image']


    image = Image.open(image_file)
    # processor = AutoProcessor.from_pretrained("microsoft/git-base")
    # model = AutoModelForCausalLM.from_pretrained("microsoft/git-base") 
    # pixel_values = processor(images=image, return_tensors="pt").pixel_values
    # generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    # generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    feature_extractor = SegformerFeatureExtractor.from_pretrained("nvidia/mit-b0")
    model = SegformerForImageClassification.from_pretrained("nvidia/mit-b0")

    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    # model predicts one of the 1000 ImageNet classes
    predicted_class_idx = logits.argmax(-1).item()
    generated_caption = model.config.id2label[predicted_class_idx]

    #generated_caption ="This is fkn nonsense"
    print(generated_caption)
       
    return jsonify({
        "generated_caption": generated_caption,
    })
