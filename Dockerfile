FROM alpine:3.1

ENV PREFIX=/opt/application

COPY . ${PREFIX}/.

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install -r ${PREFIX}/requirements.txt

# # Bundle app source
# COPY simpleapp.py /src/simpleapp.py

EXPOSE  8080
CMD ["python", "${PREFIX}/app.py", "-p 8080"]