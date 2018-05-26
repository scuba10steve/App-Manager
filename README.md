# App-Manager  
Built with Travis CI and analyzed with codacy
[![Build Status](https://travis-ci.org/scuba10steve/App-Manager.svg?branch=master)](https://travis-ci.org/scuba10steve/App-Manager) 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3bc6bf2c2e7745dfae80ad74054fedcd)](https://www.codacy.com/app/scuba10steve/App-Manager?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=scuba10steve/App-Manager&amp;utm_campaign=Badge_Grade)


A pythonic application manager to manage applications as if they were packages.

## Installation (manual right now)
###Dependencies:
Make sure you have ```python``` installed and available on the path. You can check this on linux with the ```which``` command, or with the ```where``` command on windows.

---  
A good distribution to use is [miniconda](https://conda.io/miniconda.html).  Grab a distribution for your system (version 3.6 is most compatible) and install it, it will help you with installation.


To install the application [Grab the latest release](https://github.com/scuba10steve/App-Manager/releases)
### Linux:
If downloading the ```.tar``` archive use ```tar -xf [-v for verbose]``` 

---
If downloading the ```.zip``` archive use ```unzip```

### Windows:
If downloading the ```tar``` extract with [7-zip](https://www.7-zip.org/) or a similar other tool.

### Application dependencies:
If you didn't use miniconda from above this step might be troublesome...

---
After downloading and installing the sources, you'll have to grab all the dependencies such as ```flask``` which the app requires to run.  Provided in the releases is a ```environment.yml``` file, this contains the spec for what the app needs to run, to download and install all the dependencies for the app, run the ``conda env create -f=environment.yml`` command (note: the equals ```=``` sign is required). Afterward follow the prompt on the screen, see example below:
```bash
#
# To activate this environment, use:
# > source activate default
#
# To deactivate an active environment, use:
# > source deactivate
#
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