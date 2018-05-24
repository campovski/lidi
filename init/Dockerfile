FROM ubuntu:bionic
MAINTAINER campovski

RUN apt update
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt install -y --no-install-recommends apt-utils
RUN apt install -y gcc
RUN apt install -y g++
RUN apt install -y gnupg
RUN apt install -y fp-compiler
RUN apt install -y default-jre
RUN apt install -y default-jdk
RUN apt install -y fort77
RUN apt install -y python
RUN apt install -y python3
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb https://download.mono-project.com/repo/ubuntu stable-bionic main" | tee /etc/apt/sources.list.d/mono-official-stable.list
RUN apt update

RUN mkdir -p /lidi_files
RUN mkdir -p /lidi_files/prog
RUN mkdir -p /lidi_files/out
RUN mkdir -p /lidi_files/testcases

CMD ["/bin/bash"]