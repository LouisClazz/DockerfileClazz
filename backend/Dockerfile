FROM python:3
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG PORT=9091
CMD [ "sh","-c" ,"/app/manage.py runserver 0.0.0.0:$PORT" ] 
