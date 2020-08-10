# start from an official image
FROM ubuntu:20.04

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev && \
    apt-get install -y wget


RUN python3 -m pip install --upgrade pip
RUN rm -f /usr/bin/python 
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip 
    
# Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt install -y ./google-chrome-stable_current_amd64.deb



# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt


# copy our project code
COPY . /opt/services/djangoapp/src



# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
# CMD ["/bin/sh", "./container-start.sh"]
# CMD ["/bin/bash","enter.sh"]
#ENTRYPOINT [ "enter.sh" ]
# CMD ["/bin/bash"]

CMD ["gunicorn", "--chdir", "app", "--bind", ":8000", "app.wsgi:application"]


