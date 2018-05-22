if [[ "$#" -lt 2 || ( "$1" -ne 1 && "$1" -ne 0 ) || ( "$2" -ne 1 && "$2" -ne 0 ) ]] ; then
    echo "Call script like 'source init/init_dirs.sh reinstall? add_to_bashrc? [--write-local-settings]'"
    return 1
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
    sudo apt install -y python python3 python-dev python-pip

    # C# installation
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
    echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
    sudo apt update

    # Install docker
    sudo apt install -y docker;
    
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

if [ "$3" == "--write-local-settings" ]; then
    # Create dummy local_settings.py file.
    printf "SECRET_KEY = 'vsdjhv093rvo32l2mlfk32l2VJsvormkm'\n\n\
    DATABASES = {\n\
        'default': {\n\
          'ENGINE': 'django.db.backends.postgresql_psycopg2',\n\
          'NAME': 'lidi_db',\n\
          'USER': 'admin_lidi',\n\
          'PASSWORD': 'testpwd1',\n\
          'HOST': 'localhost',\n\
          'PORT': ''\n\
        }\n\
    }\n\
    EMAIL_HOST = ''\n\
    EMAIL_HOST_USER = ''\n\
    EMAIL_HOST_PASSWORD = ''\n\
    DEFAULT_FROM_EMAIL = ''\n" > lidi/lidi/local_settings.py
 fi;

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

if [ "$3" == "--write-local-settings" ]; then
    echo "\n================================================\n"
    echo "Fill in lidi/lidi/local_settings.py to enable mail communication!\n"
fi;
