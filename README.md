# App-Manager
Built with Travis CI and analyzed with codacy
[![Build Status](https://travis-ci.org/scuba10steve/App-Manager.svg?branch=master)](https://travis-ci.org/scuba10steve/App-Manager) 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3bc6bf2c2e7745dfae80ad74054fedcd)](https://www.codacy.com/app/scuba10steve/App-Manager?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=scuba10steve/App-Manager&amp;utm_campaign=Badge_Grade)


A pythonic application manager to manage applications as if they were packages.

## Installation (manual right now)
### Dependencies:
Make sure you have ```python``` installed and available on the path. You can check this on linux with the ```which``` command, or with the ```where``` command on windows.

---  
To install the application [Grab the latest release](https://github.com/scuba10steve/App-Manager/releases)
### Linux:
If downloading the ```.tar``` archive use ```tar -xf [-v for verbose]``` 

---
If downloading the ```.zip``` archive use ```unzip```

### Windows:
If downloading the ```tar``` extract with [7-zip](https://www.7-zip.org/) or a similar other tool.

### Application dependencies:
After downloading and installing the sources, you'll have to grab all the dependencies such as ```flask``` which the app requires to run.  Provided in the releases is a `requirements.txt` file, this contains the spec for what the app needs to run, to download and install all the dependencies for the app. See example below:
You'll want to use `virtualenv` to generate a virtual environment and install the dependencies (not a requriement but is recommended).

```bash
python -m virtualenv ./venv
# If on *nux:
. ./venv/bin/activate

# If on Windows
. ./venv/Scripts/activate

# install dependencies
```
You should now be prepared to run the app
## Running

To run the application open up a terminal and run 
```bash
export FLASK_APP=app.py && export PORT=8080 && flask run --port $PORT --host 0.0.0.0
```

You should see some output similar to this:
```bash
Initializing...
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
```

Now you're ready to install some apps!