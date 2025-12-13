from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os
import glob

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class VisionAi:
    def __init__(self, model_path='model/keras_model.h5', labels_path='model/labels.txt'):
        if not os.path.exists(model_path) or not os.path.exists(labels_path):
            raise FileNotFoundError('Do not found the file of model')

        self.model = load_model(model_path, compile=False)

        with open(labels_path, 'r') as f:
            self.class_names = f.readlines()

        print('Network is ready to work')

    def check_image(self, image_path):
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        try:    
            image = Image.open(image_path).convert("RGB")

        except Exception as e:
            print(f'Cant open the image {image_path}: {e}')
            return False

        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array

        prediction = self.model.predict(data)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        print(f'Prediction: {class_name} | Confidence: {confidence_score:.0%}')

        return 'Clean' in class_name
    
    def get_latest_photo(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f'Created folder {folder_path}')
            return None
        
        files_list = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG']:
            path_pattern = os.path.join(folder_path, ext)
            files_list.extend(glob.glob(path_pattern))

        if not files_list:
            print(f'Folder {folder_path} is empty')
            return None
        
        latest_file = max(files_list, key=os.path.getmtime)
        return latest_file

if __name__ == '__main__':
    try:
        ai = VisionAi()

        photo_path = ai.get_latest_photo('photos')

        if photo_path:
            is_clean = ai.check_image(photo_path)

            if is_clean:
                print('It is clean')
            else:
                print('It is dirty')

    except Exception as e:
        print(f'Startup error: {e}')
