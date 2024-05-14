FROM python:3.10.14

WORKDIR /Intern/

# Install pip requirements
COPY /requirements01.txt ./
RUN pip install -r /requirements02.txt

RUN mkdir -p /Intern/

# Copy Python script and other necessary files
COPY /result.py ./
COPY /interpolatedca.csv /interpolatedgl.csv /interpolatedHb.csv /RandomForest_ModelCa.joblib /RandomForest_ModelGl.joblib /RandomForest_ModelHb.joblib /result.html ./

EXPOSE 5000

# Specify the entry point for the container
ENTRYPOINT ["python", "./result.py"]
