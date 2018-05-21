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

    # C# installation
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
    echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
    sudo apt update

    # Install docker
    sudo apt install -y docker;
fi;

if [ "$2" == "1" ]; then
    echo "source ${PWD}/bash/export_vars.sh ~" >> ~/.bashrc;
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
