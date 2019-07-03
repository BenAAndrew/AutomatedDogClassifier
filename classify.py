from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import pickle
import cv2
import fetchModel
import os

MODEL = fetchModel.details['model']
LABELS = fetchModel.details['labels']
#MODEL = "model.model"
#LABELS = "label.pickle"
#minimum probability to be worth outputting a response for 
MIN_PROB = 0.1
IMG_DIMENSIONS = (96,96)
DELETE_IMAGE = True

def classify(imagePath):
	global MODEL,LABELS,MIN_PROB,IMG_DIMENSIONS

	# load the image
	image = cv2.imread(imagePath)
	
	# pre-process the image for classification
	image = cv2.resize(image, IMG_DIMENSIONS)
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	if DELETE_IMAGE:
		os.remove(imagePath)

	# load the trained model and the labels
	model = load_model(MODEL)
	mlb = pickle.loads(open(LABELS, "rb").read())

	# classify the input image
	pred = model.predict(image, verbose=0)[0]

	# convert result to dictionary and ensure each result is above min probability
	predictions = dict()
	for (label, p) in zip(mlb.classes_, pred):
		if p >= MIN_PROB:
			predictions[label] = p * 100

	#predictions dict sorted by probability confidence with score appended
	output = list()
	for label in sorted(predictions, key=predictions.get, reverse=True):
		output.append("{}: {:.2f}%".format(label, predictions[label]))

	print(output)
	return output