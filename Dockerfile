FROM python:3.5-jessie
# Use jessie rather than slim because slim removes gcc and other build tools which are needed by some of the python deps

ADD . /ephemeral
WORKDIR /ephemeral
RUN pip install . --upgrade

# Use tests as entry point for now
CMD ["nosetests"]
