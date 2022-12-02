# webapp. 


A web application using FastAPI, which is a modern, fast, web framework for building APIs with Python.

###  Dependencies
require python >=3.7 for dependency with yield
Install the FastAPI:
```
        pip install "fastapi[all]"
```
for more install options, check this <a href="https://fastapi.tiangolo.com/tutorial/" class="internal-link" target="_blank">tutorial</a>.

### Run the code:
```
        uvicorn main:app --reload
```

## Deploy
### Virtual environment with venv
* create a virtual environment in a directory using Python's venv module:
```
        python -m venv env
```
* That will create a directory ./env/ with the Python binaries and then you will be able to install packages for that isolated environment.
###Activate the environment
```
        source ./env/bin/activate
```
To check it worked, use:
```
        which pip
```
If it shows the pip binary at env/bin/pip then it worked

### pip
install all the dependencies and local FastAPI in the local environment
```
        pip install -e .[dev,doc,test]
```
