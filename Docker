FROM python:3.10.14

WORKDIR /Intern/

# Install pip requirements
COPY final_predict/requirements02.txt /
RUN pip install -r /requirements02.txt

# Create directory for final results
RUN mkdir -p /Intern/final_results

# Copy Python script and other necessary files
COPY final_predict/result01.py ./final_predict/
COPY final_predict/interpolatedca.csv final_predict/interpolatedgl.csv final_predict/interpolatedHb.csv final_predict/RandomForest_ModelCa.joblib final_predict/RandomForest_ModelGl.joblib final_predict/RandomForest_ModelHb.joblib final_predict/result01.html ./final_predict/

EXPOSE 5000

# Specify the entry point for the container
ENTRYPOINT ["python", "./final_predict/result01.py"]
