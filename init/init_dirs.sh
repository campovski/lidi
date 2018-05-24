#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Call script like 'source init/init_dirs.sh reinstall? add_to_bashrc?"
    return 1
fi;

find init/ "init/local_settings.py";
if [ "$?" -ne "0" ]; then
    echo "Please create init/local_settings.py from init/local_settings_template.py and fill in required information!\n";
    return 1;
fi;

if [ "$1" == "1" ]; then
    # Update and upgrade prior to doing anything...
    sudo apt update && sudo apt upgrade -y

    # Pascal installation
    sudo apt install -y fp-compiler;

    # Java installation
    sudo apt install -y default-jre;
    sudo apt install -y default-jdk;

    # Fortran 77 installation
    sudo apt install -y fort77;
    
    # Install python and pip
    sudo apt install -y python
    sudo apt install -y python3
    sudo apt install -y python-dev
    sudo apt install -y python-pip

    # C# installation
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
    echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
    sudo apt update

    # Install docker
    sudo apt install -y docker;

    # Build docker image
    cd init/
    docker build -t ubuntu:lidi .
    cd ..
    
    # Install postgresql
    sudo apt install -y postgresql;
    sudo service postgresql start;
    
    # Install virtualenv and python dependencies.
    sudo apt install virtualenv;
    virtualenv venv;
    source venv/bin/activate;
    pip install -r init/requirements.txt;
    deactivate;
fi;

if [ "$2" == "1" ]; then
    echo "source ${PWD}/init/export_vars.sh ~" >> ~/.bashrc;
    source ~/.bashrc;
fi;

echo '$CG_FILES_DIR='$CG_FILES_DIR;
# Make directories for files.
mkdir -p $CG_FILES_DIR;
mkdir $CG_FILES_PROBLEMS;
mkdir $CG_FILES_PROBLEMS_TMP;
mkdir $CG_FILES_TESTCASES;
mkdir $CG_FILES_TESTCASES_SOL;
mkdir $CG_FILES_SOLUTIONS;
mkdir $CG_FILES_UPLOADED;

# Move local_settings.py to lidi/lidi/local_settings.py
mv init/local_settings.py lidi/lidi/local_settings.py

# Database initialization.
sudo -u postgres psql -f "${PWD}/init/init.sql"
source venv/bin/activate
cd lidi/
python manage.py makemigrations
python manage.py migrate
python manage.py populate_countries
python manage.py populate_languages
python manage.py populate_proglang
deactivate
cd ..
