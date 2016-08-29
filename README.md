# CalExams
CalExams is a web application that aims to stream line the process of searching for/downloading past midterms and finals for UC Berkeley classes, currently it only supports computer science classes. CalEaxms pulls the download links from the HKN (https://hkn.eecs.berkeley.edu/exams/) and the Tau Beta Pi (https://tbp.berkeley.edu/courses/) exam archive pages using the Python package BeautifulSoup. In the future, support for other classes will be added as well. The web application uses Django as the web framework, and Angular.js as the front end framework

## Get Started
Clone the repository with:
```
$ git clone https://github.com/LennyDong/CalExams.git
```

Next, please install virtualenv:
```
$ pip install virtualenv
```
and create a virtual environment within the repository directory:
```
$ cd CalExams
$ virtualenv venv
```

Start the virtual environment with:
```
$ source venv/bin/activate
```

Please add your Python3 to the virtual environment with:
```
$ virtualenv -p /usr/bin/PYTHON3_DIRECTORY venv
```

Next, install all required packages:
```
$ pip install -r requirements.txt
```

## Usage
To start running the server, enter:
```
$ python manage.py runserver
```

Open a browser, and visit the local port the server is currently running on
