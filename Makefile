install:
	pip install --upgrade pip  &&\
	pip install -r requirements.txt &&\
	sudo apt update && sudo apt install ffmpeg -y &&\
	sudo apt install espeak -y

format:
	black *.py #format all files	
