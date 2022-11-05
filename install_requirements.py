import os

if os.name == 'nt':
    try:
        os.system("python -m pip install -r requirements.txt --no-dependencies")
    except:
        os.system("py -m pip install -r requirements.txt --no-dependencies")
else:
    try:
        os.system("pip3 install -r requirements.txt --no-dependencies")
    except:
        os.system("python3 -m pip install -r requirements.txt --no-dependencies")