from flask import Flask, render_template, request, Markup
from siteHandler import *

app = Flask(__name__)

MAX_MB = 50
app.config['UPLOAD_FOLDER'] = getUploadFolder()
app.config['MAX_CONTENT_LENGTH'] = MAX_MB * 1024 * 1024

#defines variables for server deployment or running locally (change for purpose)
LOCAL = False

if LOCAL:
    ip = 'localhost'
    port = 5000
    host = ip
else:
    ip = 'dogclassifier.herokuapp.com'
    port = 80
    host = '0.0.0.0'

address = ip+":"+str(port)
print(address)

@app.route("/")
def index():
   return render_template("index.html", address=address)

@app.route('/feedback', methods = ['POST'])
def saveFeedback():
    select = request.form['select']
    image = request.form['image']
    manualEntry = request.form['other']
    if select == "other":
        select = manualEntry
    writeFeedbackToFile(select,image)
    return render_template('index.html', text="Thank you for your feedback. It will be used to retrain the model and improve the system", address=address)

@app.route('/process', methods = ['POST'])
def processRequest():
    print("PROCESS")
    message = "File not found"
    imageLocation = ""
    if 'file' in request.files:
        try:
            file = request.files['file']
            if allowed_file(file.filename):
                newFilename = str(str(int(time.time()))+"."+getExtension(file.filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFilename))
                imageLocation = UPLOAD_FOLDER+"/"+newFilename
            else:
                message = "File must be .png, .jpg or .jpeg"
        except:
            message = "File could not be opened"
    if len(imageLocation) == 0:
        return render_template('index.html', text=message)
    else:
        predicitions = classifyImage(imageLocation)
        text = getClassifyHTML(predicitions)
        result = getFeedbackHTML(predicitions, imageLocation.split("/")[1])
        return render_template('prediction.html', text=text,result=result,address=address)

if __name__ == '__main__':
    app.run(host=host,port=port,debug=True)
