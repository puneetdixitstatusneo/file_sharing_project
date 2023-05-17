FROM python:3.10.11-slim-buster
RUN mkdir -p /backend 
WORKDIR /backend
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir /volumeA
RUN mkdir /volumeB

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


################################## DOCKER COMMANDS ######################################################
# docker ps
# docker images
# docker build . -t tag_name
# docker run  --name  container_name --rm --it -p 3000:3000/tcp tag_name:latest
# docker run --name file_share_cont --rm -it -d -v /Users/anirudh.agarwal/Desktop/file_sharing_project/mount:/mount_cont -p 3000:3000/tcp file_share_flask:latest
# docker exec -it container_name bash

################################## DOCKER MAC ######################################################

# docker run --name file_share_cont --rm -it -d -v /Users/anirudh.agarwal/Desktop/file_sharing_project/volumeA:/volumeA -v /Users/anirudh.agarwal/Desktop/file_sharing_project/volumeB:/volumeB -p 5000:5000/tcp flask_file_share:latest


# docker build . -t flask_file_share:latest

################################## DOCKER WINDOWS  ######################################################


#########################################################################################
# NGINX
# docker pull nginx
# docker run --name nginx–test –d nginx:latest
# docker exec -it nginx-test /bin/bash
# docker attach nginx-test

# docker inspect -f "{{ .NetworkSettings.IPAddress }}" container_name
# 172.17.0.2
#########################################################################################


# To use mysql with command line
# export PATH=${PATH}:/usr/local/mysql/bin



#########################################################################################
# List All Environment Variables: # printenv
# echo $[variable name]
# echo $PATH

# /Library/Frameworks/Python.framework/Versions/3.10/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin  ( without env activated )
# /Users/anirudh.agarwal/Desktop/file_sharing_project/venv/bin:/Library/Frameworks/Python.framework/Versions/3.10/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin  ( with env activated )

####################################################
# Set Temporary Environment Variable:
# export [variable_name]=[variable_value]


# The export command also allows you to add new values to existing environment variables:
# export [existing_variable_name]=[new_variable_value]:$[existing_variable_name]
# export PATH=/Users/test/test_folder:$PAT
####################################################

# Set Permanent Environment Variable
# 1. Find the path to .bash_profile by using:    ~/.bash-profile
# 2. Open the .bash_profile file with a text editor of your choice.
# 3. Scroll down to the end of the .bash_profile file.
# 4. Use the export command to add new environment variables:
# export [variable_name]=[variable_value]
# 5. Save any changes you made to the .bash_profile file.
# 6. Execute the new .bash_profile by either restarting the terminal window or using:  source ~/.bash-profile

#########################################################################################
