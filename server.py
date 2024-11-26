import flask
import os
from flask import Flask, jsonify, send_file
import json

from main import ProduceOutput

app = Flask(__name__)

lot_id = '12345' # Hardcoded for testing
ProduceOutput(lot_id) # Hardcoded for testing

# upload image to server
@app.route('/upload', methods=['POST'])
def upload():
    try:
        
        if 'image' not in flask.request.files:
            return jsonify({'error': 'No image part in the request'}), 400

        imagefile = flask.request.files['image']
        lot_id = flask.request.headers['lotID']  
        
        
        if imagefile.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        
        lot_folder = os.path.join('upload_folder', lot_id)
        if not os.path.exists(lot_folder):
            os.makedirs(lot_folder)

        # Save the file inside the 'lot_id' folder
        filename = os.path.join(lot_folder,
                                f'{lot_id}.jpeg') 
        imagefile.save(filename)
        ProduceOutput(lot_id)
        return jsonify({'message': 'Image uploaded successfully'}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500



@app.route('/lots', methods=['GET'])
def get_all_lots():
    with open('lots.json', 'r') as file:
        parking_lots = json.load(file)

    return parking_lots


@app.route('/data/<lot_id>', methods=['GET'])
def get_parking_data(lot_id):
    try:
        
        file_path = os.path.join('upload_folder', lot_id, 'out', 'parking_status.json')

        
        if not os.path.exists(file_path):
            return "Parking data not found", 404

        
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data

    except Exception as e:
        print(f"Error getting parking data: {e}")
        return "Internal Server Error", 500


# get image specific to lot
@app.route('/image/<lot_id>', methods=['GET'])
def get_image(lot_id):
    try:
        
        file_path = os.path.join('upload_folder', lot_id, 'out', '12345.jpeg')

       
        if not os.path.exists(file_path):
            return "Image not found", 404

        
        return send_file(file_path, mimetype='image/jpeg'), 200, {'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        print(f"Error getting image: {e}")
        return "Internal Server Error", 500


if __name__ == "__main__":
    # Run the Flask app
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=8080)