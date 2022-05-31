# SLI detection app

A flask web app that allows the user to input their speech sample and detect SLI.

The main endpoint is /model/prediction where the user uploads their sample speech in the form and gets processed. The processed speech sample is then pickled and stored. The trained model is loaded and predicts whether SLI is present or not.

### Get started

1. Clone the repo

2.  Create and activate the virtual environment 

     virtualenv env

     . env/bin/activate

3.  Install the requirements
    pip install -r req.txt

4.  Go to the folder containing app.py and start the server

    flask run

   

