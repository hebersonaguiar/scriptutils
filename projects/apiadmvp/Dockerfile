FROM python:3.4.9

RUN apt-get update ; \
	    apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev 

WORKDIR /opt

COPY server.py /opt/
COPY requirements.txt /opt

RUN pip install -r requirements.txt

EXPOSE 80

CMD python server.py
