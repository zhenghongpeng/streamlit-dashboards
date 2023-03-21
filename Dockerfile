from python:3.9.0
expose 8501
cmd mkdir -p /app/streamlit-dashboard
WORKDIR /app/streamlit-dashboard
copy ${PWD} /app/streamlit-dashboard
run pip3 install -r /app/streamlit-dashboard/requirements.txt
ENTRYPOINT ["streamlit", "run"]
CMD ["/app/streamlit-dashboard/app.py"]