# Pascal installation
sudo apt-get install fp-compiler;

# Java installation
sudo apt-get install default-jre;
sudo apt-get install default-jdk;

# Fortran 77 installation
sudo apt-get install fort77;

# C# installation
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF;
echo "deb http://download.mono-project.com/repo/debian wheezy main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list;
sudo apt-get update;
sudo apt-get install mono-complete;

# Export directory names
# You have to append a line to .bashrc... Will figure something
# out to automate it
source $HOME/.bashrc;

# Install chroot utils
sudo apt-get install dchroot debootstrap;

# Make directories for files.
mkdir -p $CG_FILES_DIR;
mkdir $CG_FILES_PROBLEMS;
mkdir $CG_FILES_PROBLEMS_TMP;
mkdir $CG_FILES_TESTCASES;
mkdir $CG_FILES_TESTCASES_SOL;
mkdir $CG_FILES_SOLUTIONS;
mkdir $CG_FILES_UPLOADED;
