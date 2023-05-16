FROM python:3.10.11-slim-buster
# RUN mkdir -p /backend
RUN mkdir -p /backend/test_container 
WORKDIR /backend
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
VOLUME ["/test_container"]




# docker ps
# docker images

#  docker build . -t tag_name

# docker run  --name  container_name --rm --it -p 3000:3000/tcp tag_name:latest
# docker exec -it container_name bash

# docker run --name file_share_cont --rm -it -d -v /Users/anirudh.agarwal/Desktop/file_sharing_project/mount:/test_container -p 3000:3000/tcp file_share_flask:latest2