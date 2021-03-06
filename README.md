# AutomatedDogClassifier - A Machine Learning Project 
<h2>http://dogclassifier.herokuapp.com</h2>

<h2>Quick note</h2>
This project is designed as a learning tool for those interested in machine learning and I've done my best to explain my work but I am not an expert and I highly reccomend studing the area further.
Also if you use this work in a project please let me know as I would be really happy if anyone finds this useful and would love to hear about others projects.

<h2>Introduction</h2>

This project covers everything from <b>data fetching</b> to <b>training</b> and building a <b>web app</b> for users to interact with.
It uses Keras as its main library and multi-class image classification. 

Even if you're new to machine learning or some the technologies used in this I will do my best to explain everything and point to useful resources where possible.

The example of Dog's is <b>not</b> important and serves only as an example. The resources and methods used can be adapted for classifying for anything you wish.

<h2>An introduction to machine learning</h2>
<b>Disclaimer:</b> I'm not an expert on machine learning but have completed a few projects in the field. I'll do my best to explain all key points and hopefully help simplify complicated topics, but always research more about the concepts and libraries you use!

Machine learning is a big buzzword in computer science at the moment and can be confusing to approach. 
In leyman's terms it's where computers execute a task <b>without explicit instructions</b>, and instead <b>identify patterns</b> to learn. What this means is that a system can learn to identify features (from text/images typically) without the programmer ever actually teaching the system anything about what it should be looking for. Here's a fun video explaining this pretty well; https://www.youtube.com/watch?v=R9OHn5ZF4Uo

For example past eye analysis tools would involve programming constraints and features to analyse images and make decisions manually, probably with the help of a doctor who would explain what features programmers should analyse. However with the growth of machine learning & AI, systems can now be given image datasets and through analysing features of thousands of images, learn for themselves what image features correlate to what they're looking to analyse.

By using this new systems can be developed more quickly and with <b>less human biases</b> (decisions/thoughts humans may have that could be wrong) impacting the system. Here's an article talking about the Deepmind team developing a system to do this very thing;  https://www.theverge.com/2018/8/13/17670156/deepmind-ai-eye-disease-doctor-moorfields

This project aims to take you through how to build a system like this, which can idenify image features and automatically classify whatever it is you wihs (in this example <b>what dog breed is found in an image</b>)

<h2>Project variables</h2>
Before I get into the project I just wanted to mention that the bulk of the project properties are held in the <b>projectProperties.ini</b> file. This is where you should change settings for the project such as your classification settings and resources. This is handled by the <b>projectProperties.py</b> script which will download web resources (for model & labels discussed later) and is imported by other python files to get access to these variables. 

This is all important to know as you will likely be modifying the project for your needs, and through this file is the ideal place.

<h2>Project breakdown</h2>
<h3>Step 1: Building the dataset (imageFetcher.py)</h3>
<ul>
  <li>In case you're not aware a dataset is simply a collection of data. In this case images of dogs from different breeds</li>
  <li>Getting a premade dataset is the easiest solution but you can also build your own (as we will)</li>
</ul>
<h3>(Optional Step): Verifying your dataset (verifier.py)</h3>
<ul>
  <li>If you've built your own dataset there's a likelyhood there's some invalid data</li>
  <li>To help clean this you may be able to use antoher machine learning tool such as Yolo (https://pjreddie.com/darknet/yolo/) to help you out</li>
</ul>
<h3>Step 2: Training (Train.ipynb)</h3>
<ul>
  <li>This is the big and essential step where we create our system which learns how to classify images</li>
  <li>This file is in a jupyter notebook which makes it easier to run through step by step and customise for your project</li>
  <li>I've included explanations of the steps inside this notebook so those new to machine learning pay close attention to this</li>
</ul>
<h3>Step 3: Prediction (classify.py)</h3>
<ul>
  <li>Once you've built and optimised your machine learning model we can use it to then guess what class (breed) a new image is</li>
  <li>This is the final product of your work in training and with good design can reliably predict what class an image is</li>
</ul>
<h3>Step 4: Web app (app.py)</h3>
<ul>
  <li>A nice way to round off a project is to turn it into a web app users can interact with</li>
  <li>This step is technically optional as by this stage you have built your model, and how you choose to use it is up to you</li>
</ul>

<h2>Setup</h2>
Before starting I would urge you to set up a vitual environment to work in. They are extremely useful for python projects like these and will greatly help with keeping track of libraries.
The two most popular options for virtual environments are;
<ul>
  <li> Anaconda (windows & linux): https://www.anaconda.com/ </li>
  <li> virtualenv (linux): https://virtualenv.pypa.io/ </li>
</ul>

I won't go into detail on how to install these as they're are tons of guides on how to do this but once you have installed one of these, create an environment in terminal and activate it.<b>Ensure you use python 3.7!</b>

Then download this project either using git clone or zip and change location in terminal to this downloaded directory.

Now we can install the needed libraries either by running;
```
pip install -r "requirements.txt"
```
which will automatically install all the libraries or by individually pip installing the following libraries (explanations of what they're for in brackets);
<ul>
  <li><b>keras</b> (Neural network library we'll use for model training, runs on top of tensorflow)</li>
  <li><b>tensorflow</b> (Google's open source machine learning library)</li>
  <li><b>opencv-python-headless</b> (Library for computer vision and image analysis (headless is smaller))</li>
  <li><b>argparse</b> (Library for passing arguments in terminal)</li>
  <li><b>imutils</b> (Library for basic image manipulation functions)</li>
  <li><b>google_images_download</b> (Library to download images for step 1)</li>
  <li><b>flask</b> (Framework for running python webservers for step 4)</li>
 </ul>
 
So long as these all install fine you're ready to go.

<h2>Step 1: Building the dataset</h2>
If you have a pre-made dataset (i.e. a dataset of images split into folders where the name of each folder is the class name) you can skip this step. 


A machine learning model needs data from which to learn. The more data we can get the more reliable the model will be. In this project our data needs to be images, sorted into their categories. In this case my categories are dog breeds held in the <b>breeds.txt</b> file found in the train folder (where all the resources for this step are found).


Running <b>imageFetcher.py</b> will google image search each line in this text file and save the first 100 matching jpg files to a directory with the same name as the search term inside a folder called datasets. 
Let me break down the code so you can customise this as you wish;

Line 8 fetches the list of search terms from "breeds.txt"
```
breeds = [line.rstrip('\n') for line in open("breeds.txt")]
```
If you wish to change the text file from which the search terms are read simply change the file in this line.
Below this line the images per breed (class) and max threads are speicifed. 

Unfortunately with the google_images_download it seems you're capped at a maximum of 100 images unless you pass it a chromedriver executable to handle the requests. Hopefully in a later revision I'll find an alternative library to use for this reason. 

Also you'll see a max threads argument. This allows multiple different image fetching threads to work similtanously using 
```
with concurrent.futures.ThreadPoolExecutor(max_workers=max_similtaneous_threads) as executor:
  executor.map(downloadimages, breeds)
```
This is a input thread handling class which allows multiple function calls of downloadimages to be called with each argument in the breeds list. max sure to decrease the max_similatenous_threads depending on your computers hardware.

Other than that the file is relatively self explanatory with the downloadImages function simply contatining the configuration arguments (set to medium file size and jpg file extension by default) and calling the library's download function.

Run this method with your own text file (remember to change line 8) and you should see your dataset folder filled with several folders of images.

<h2>Optional Step: Verifying dataset</h2>

Google images is fairly reliable in giving us the correct images for a search, but this is not always the case. Try searching any dog breed you like and you'll see some images that may cause issues for our model such as drawings or images that simply don't contain the breed in question. Obviously a classifier for whatever your looking to classify doesn't currently exist (otherwise you probably wouldn't bother making your own) but that doesn't mean there's nothing we can do to check data.

Yolo is a real-time object classification project that has achieved fantastic results on classifying common world objects. This means that although it cannot tell dog breeds apart, it can identify a dog in an image. Thanks to this we can pass every image in our dataset through Yolo to get a list of images that may not contain a dog.

open the <b>verifier.py</b> file in the train project to see how this works ... [TO BE CONTINUED]

<h2>Step 2: Training</h2>
You'll note the Train file in the train folder is not a .py extension. This is because it's a jupyter notebook which is a kind of document that contains python code and markdown text split into cells. These are widely used to build data analysis projects because they allow for better explanation of code. To open this firstly install jupyter by running;

```
conda install jupyter notebook
```
if using the anaconda terminal or 
```
pip3 install jupyter
```
if using virtualenv.
Once done type <b>jupyter notebook</b> into console and the jupyter application should open in your default browser. Select the Train notebook in the train folder and a new window should open with the jupyter report in it. 

I'll avoid talking any further about the training stage here as all the details and explanations can be found in the Train notebook

<h2>Step 3: Prediction</h2>
By this stage all the training is over and you have a model and labels file to show for it. This step involves now using these to predict on new images, and this as we'll see later can be integrated into a web app.

The key file here is <b>classify.py</b> that you'll find in the root directory of this project but <b>fetchModel.py</b> is also used here as I'll explain quickly now.

<h4>fetchModel.py</h4>
fetchModel is a seperate python file which has the job of reading the <b>modelDetails.ini</b> config file and using these properties to download your model and labels file from url's.
<h4>Why do we need to download  the model & labels seperately</h4>
Well technically you don't need to at this stage but becuase the model file is so large (exceeding 100MB) it made interaction with git a little tricker (search git lfs for help with this) but more importantly it meant the project couldn't be deployed to heroku (step 4). For this reason I created the the config and fetchModel.py files to handle downloading these as a one off when the app is run, if the files cannot be found in the current directory. Also the fetchModel file script holds the model and labels file names in its details dictionary which is used by classify.py and hence why I had to explain this now.

<h4>classify.py</h4>
Firstly the sole puropse of classify.py is to take a image url and to read and predict its classes, with a list of these predictions being returned to the calling location. I explain in this file some of the stages but I'll explain in more depth here.

```
MODEL = fetchModel.details['model']
LABELS = fetchModel.details['labels']
```
These two constants hold the names of the model and labels files (which should be saved in the projects root directory). They get their names from fetchModel.py's details dictionary (explained above) but if you don't want to use this instead just replace these two with the name of your model/label files (see classify.py for an commented example).

```
MIN_PROB = 0.1
IMG_DIMENSIONS = (96,96)
```
Also included are two key variables. The first 'MIN_PROB' holds the minimum probability for what we should consider a viable possibility to show to the user. For example if the prediction returns a probability >= 10% (0.1) of something being a certain class, we will show this to the user, otherwise we will ignore it. Also 'IMG_DIMENSIONS' holds what dimension the image should be converted to for prediction (must match models dimensions).

Inside the sole function <b>classify(image)</b> the image location passed is loaded by opencv and converts this in a similar way to as discussed in Training. The model and labels are then loaded using keras and pickle. 

```
pred = model.predict(image, verbose=0)[0]
```
This line is where the prediction is made. It uses our trained model 'model' and predicts on the loaded image. the simgle index [0] is used here as we only predict for a simple image and therefore only get a single result back in the array.

After this the results are paired with classes in the following for statement
```
for (label, p) in zip(mlb.classes_, pred):
```
and saved to a predictions dictionary if above the minimum probability discussed earlier. The function finsihes by sorting the dictionary by score (highest probability first) and saving it to a list with class and probability concatenated, which is what is returned 

i.e. ["A: 60%","B: 30%"] may be a typically returned list where class 'A' was found to have a 60% likelyhood of being the class in the image, and class 'B' had a 30% probability.

This is the work of the predictor done and how you use its result is up to you. In the next step I'll go through how I integrated this into a web app.

<h2>Step 4: Web app</h2>
The last step in the project (if you wish to) is to now wrap all of what we've done inside a web app, so we can share it with the world and allow users to test it out and give feedback.

<h4>Website</h4>
The bulk of the files in the repository are for this step but are not particually complex. The majority are files for our website with the pages in the <b>templates</b> folder and the assets (images & css) in the <b>static</b> folder.

You may notice when looking at the webpages that they use this <b>{{double curly brace structure}}</b> in a few places. This is to do with <b>flask</b> which is the library which handles our website and allows us to integrate python into the backend of the site. The curly braces are recognised by flask as placeholders for some resource. For example;
```
href="{{ url_for('static', filename = 'assets/css/main.css') }}"
```
returns the directory for the main.css within the flask folder structuring into the page, so that it has css. This isn't so important as it's just to do with the webpage but there are also placeholders for where we want to place something in the page;
```
<form action="http://{{ address|safe }}/process" ...
```
This tells flask when we render the page we will pass it a variable called <b>address</b> into this position. We also tell it that the text is <b>safe</b> (second argument seperated by |) which means we tell flask not to escape this string. What this means is that for example if address was set to "localhost:5000" then action would be "http://localhost:5000/process" when the page is rendered. This example is found in index.html but if you look in prediction.html we see another;
```
<ul>
  {{ text|safe }}		
</ul>
```
This returns the variable <b>text</b> into this position of the page. We use this to return multiple list items (\<li\>) for all the classes the prediction returned. That's all you need to know about the pages really but just bear in mind this is how flask works if you wish to create your own pages and output variables to them.
  
<h4>App</h4>
The <b>app.py</b> file is where the page processing decisions are made. You can see we import the all important Flask library as well as <b>siteHandler.py</b> which we'll discuss after this. We firstly declare the Flask app object and add configurations for the uploadFolder and maxLength. These variables as well as many others are set the the projectProperties.ini file.

After this a boolean LOCAL decides whether the run the app locally (through localhost on your machine) or on a server (as I'll explain later). For now make sure this value is <b>true in projectProperties.ini</b> because we always want to test locally first. This variable sets others to define the address variables decidng what ip and port the project runs on.

Now we'll get into what happens when the user requests a page. If the user simply goes to the home address i.e. localhost:5000 this requests the root directory (/). We can define what should happen when this request is made like this;
```
@app.route("/")
def index():
   return render_template("index.html", address=address)
```
This says that when someone requests the root directory (/) it should execute our index function. This function simply returns the index.html using <b>render_template</b> and also includes the address we're using (localhost:5000)

The next path the site will use is <b>process</b>. This will be called when the user uploads an image to the page and presses submit, thus executing the form. This function may look very complex but once we break it down it shouldn't be too bad. Firstly we define the function and some variables 
```
@app.route('/process', methods = ['POST'])
def processRequest():
    print("PROCESS")
    errorMessage = "File not found"
    imageLocation = ""
```
You'll note that the method in the route is set to post as this is how our form submits it's data. The errorMessage variable is the message we'll output if there is any issue with the image, and imageLocation will be what is passed to our predictor if there is no error.
```
if 'file' in request.files:
```
This simply checks if there is an input called 'file' (name of our image input) found in the forms request inside files. 
```
try:
  file = request.files['file']
  if allowed_file(file.filename):
```
We use a try statement here as we are now trying to get the image and errors may occur. Firstly we save the passed image to a variable called file, and then we check the file is accepted using allowed file <b>(defined in siteHandler.py)</b>.
```
newFilename = str(str(int(time.time()))+"."+getExtension(file.filename))
file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFilename))
imageLocation = UPLOAD_FOLDER_RELATIVE+"/"+newFilename
```
If this is the case the image is accepted. Firstly I rename the image to the current timestamp it's being uploaded at. This isn't entirely neccersairy but does avoid issues with duplicate names that may arise. The extension remains the same. I then save the image to the UPLOAD_FOLDER defined directory with its new name. os.path.join is required to get the absolute directory of the folder in the system. I then also define the relative directory which is what is passed to the predictor.
The else and except under this simply outlines what type of error occured if there was one. If there was an error imageLocation will be empty so we can use that in a check to output an error;
```
if len(imageLocation) == 0:
  return render_template('index.html', text=message)
```
This says that if imageLocation is empty then return index.html with the errorMessage being passed as a flask variable called text. <b>text</b> is added to a javascript alert message which is output if not empty (see index.html line 31). However if there is no error the following is execute;
```
predicitions = classifyImage(imageLocation)
text = getClassifyHTML(predicitions)
result = getFeedbackHTML(predicitions, imageLocation.split("/")[1])
```
This firstly calls classifyImage which uses <b>classify.py</b>, and then formats what is passed back using two other functions found in <b>siteHandler</b>. For know all you need to know is that this converts the result to HTML to be shown on the page.
```
return render_template('prediction.html', text=text,result=result,address=address)
```
This is what finally returns our prediction.html page with the text and result variables outputting the results of our prediction to the user.
