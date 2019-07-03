# USAGE
# python classify.py --model fashion.model --labelbin mlb.pickle --image examples/example_01.jpg

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

model = "model.model"
labels = "label.pickle"
#minimum probabilityt to be worth outputting a response for 
min_prob = 0.1

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
output = imutils.resize(image, width=400)
 
# pre-process the image for classification
image = cv2.resize(image, (96, 96))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# load the trained convolutional neural network and the multi-label
# binarizer
model = load_model(model)
mlb = pickle.loads(open(labels, "rb").read())

# classify the input image then find the indexes of the two class
# labels with the *largest* probability
proba = model.predict(image)[0]
idxs = np.argsort(proba)[::-1][:2]

'''for (i, j) in enumerate(idxs):
	# build the label and draw the label on the image
	label = "{}: {:.2f}%".format(mlb.classes_[j], proba[j] * 100)
	cv2.putText(output, label, (10, (i * 30) + 25), 
		cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# save the output image
cv2.imwrite("Output.jpg", output)'''

# show the probabilities for each of the individual labels
predictions = dict()
for (label, p) in zip(mlb.classes_, proba):
	if p >= min_prob:
		predictions[label] = p * 100

for label in sorted(predictions, key=predictions.get, reverse=True):
	print("{}: {:.2f}%".format(label, predictions[label]))