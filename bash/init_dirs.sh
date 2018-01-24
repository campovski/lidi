if [ $1 == "1" ]; then
# Update and upgrade prior to doing anything...
sudo apt-get update && sudo apt-get upgrade -y

# Pascal installation
sudo apt-get install -y fp-compiler;

# Java installation
sudo apt-get install -y default-jre;
sudo apt-get install -y default-jdk;

# Fortran 77 installation
sudo apt-get install -y fort77;

# C# installation
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF;
echo "deb http://download.mono-project.com/repo/debian wheezy main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list;
sudo apt-get update;
sudo apt-get install -y mono-complete;

# Export directory names
# You have to append a line to .bashrc... Will figure something
# out to automate it
source $HOME/.bashrc;

# Install chroot utils
sudo apt-get install -y dchroot debootstrap;
fi;

sudo bash export_vars.sh /home/campovski;
echo '$CG_FILES_DIR='$CG_FILES_DIR;
# Make directories for files.
mkdir -p $CG_FILES_DIR;
mkdir $CG_FILES_PROBLEMS;
mkdir $CG_FILES_PROBLEMS_TMP;
mkdir $CG_FILES_TESTCASES;
mkdir $CG_FILES_TESTCASES_SOL;
mkdir $CG_FILES_SOLUTIONS;
mkdir $CG_FILES_UPLOADED;
