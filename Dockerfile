FROM python:3.10.11-slim-buster
# RUN mkdir -p /backend
RUN mkdir -p /backend 
WORKDIR /backend
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir /backend/mount_cont
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
VOLUME ["/mount_cont"]




# docker ps
# docker images

#  docker build . -t tag_name

# docker run  --name  container_name --rm --it -p 3000:3000/tcp tag_name:latest
# docker exec -it container_name bash

# docker run --name file_share_cont --rm -it -d -v /Users/anirudh.agarwal/Desktop/file_sharing_project/mount:/mount_cont -p 3000:3000/tcp file_share_flask:latest