FROM fedora:latest

VOLUME /opt/robotframework/tests

# Basic OS and Phyton dependencies
RUN dnf upgrade -y
RUN dnf install -y python38
RUN dnf module install -y nodejs:12
# Database dependencies PostgreSQL
RUN dnf install -y libpq-devel
# FTSA installation
RUN pip install ftsa-tjpb && ftsa install

WORKDIR /opt/robotframework/tests