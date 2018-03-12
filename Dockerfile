# Docker file for Fedora 3.8 Utilities
FROM tuttlibrary/python-base
MAINTAINER Jeremy Nelson <jermnelson@gmail.com>

ENV HOME /opt/fedora38-utilities
RUN mkdir -p $HOME/instance
COPY *.py $HOME/
COPY legacy_fedora $HOME/legacy_fedora
COPY instance/. $HOME/instance/

EXPOSE 9455
WORKDIR $HOME
CMD ["nohup", "gunicorn", "-b", "0.0.0.0:9455", "run:application"]

