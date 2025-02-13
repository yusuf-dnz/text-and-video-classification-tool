from collections import Counter
from math import ceil
from keras.models import load_model
import tensorflow as tf
import numpy as np
import cv2
from frame_sampling import frames_from_video_file

with open('Networks/label_dict.txt', 'r', encoding='utf-8') as file:
    label_dict = list(map(lambda x: x.strip(), file))


def predict_on_video(video_path, model_name, n_frames=15, output_size=(224, 224), frame_step=12):
    model = load_model("Networks/" + model_name + "/video_net_" + model_name.lower() + ".h5")
    cv_video = cv2.VideoCapture(video_path)
    total_frames = int(cv_video.get(cv2.CAP_PROP_FRAME_COUNT))
    parts = ceil(total_frames / (n_frames * frame_step))
    video_frames = frames_from_video_file(video_path, parts * n_frames, output_size, frame_step)
    predictions = []

    for i in range(0, len(video_frames), n_frames):
        video_part = np.array(video_frames[i:i+n_frames])
        video_part = np.expand_dims(video_part, axis=0)
        predicted = model.predict(video_part)
        predicted_class = np.argmax(predicted)
        predictions.append(predicted_class)
    counter = Counter(predictions)
    predicted_index = counter.most_common(1)[0][0]
    predicted_class = label_dict[predicted_index]
    return predicted_class


video = "deneme.mp4"

print(predict_on_video(video, "3D_CNN"))
