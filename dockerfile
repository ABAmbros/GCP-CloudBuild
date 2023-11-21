FROM python:3.7-alpine
COPY app_web/ app_web/ 
WORKDIR /app_web 
RUN pip install -r requirements.txt

CMD ["python", "programa.py"]