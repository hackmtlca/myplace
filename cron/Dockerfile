FROM joyzoursky/python-chromedriver:3.6-alpine3.7-selenium
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80

CMD ["python3", "__main__.py"]