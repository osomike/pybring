FROM python:3.8-slim

# Install basic requirements
RUN apt-get update
RUN	apt-get install -y gcc vim
RUN /usr/local/bin/python -m pip install --upgrade pip

# COPY Copy files
COPY app/requirements.txt ./app/requirements.txt

# Install requirements
RUN pip install -r ./app/requirements.txt

# Copy other files
COPY app/credentials/bringapi-92345de4ed45.json app/credentials/bringapi-92345de4ed45.json
COPY app/app.py app/app.py
COPY app/pybring.py app/pybring.py

# Only the last command will be executed
CMD ["python", "app/app.py"]
#CMD ["jupyter", "notebook", "--port=8888", "--notebook-dir=\"/app\"", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
# docker build . -t pybring

#To run jypyter notebook:
# jupyter notebook --port=8888 --notebook-dir=/app"--no-browser --ip=0.0.0.0 --allow-root
# docker run -p 8888:8889 pybring

# To run the app:
# python app.py
# docker pybring
