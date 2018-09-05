#!/usr/bin/env bash

echo "<<<INSTALL DEPENDENCIES>>>"
apt update
apt-get install -y -q python-pip python2.7-dev python-tk
python -m pip install --upgrade pip
echo "Pip ... OK"
apt-get purge -y -q python-numpy
pip install --ignore-installed six
pip install pandas
pip install numpy
pip install scipy
pip install skopt
pip install matplotlib
pip install colorama
pip install seaborn
pip install scikit-learn
pip install scikit-optimize
pip install tinydb
pip install statistics
echo "Python Dependencies ... OK"

rm -r ./vmtouch
git clone https://github.com/hoytech/vmtouch.git
cd vmtouch
make
sudo make install
cd ..
rm -r ./vmtouch
echo "VMTouch ... OK"

# CHECK GRAALVM DEPENDENCY
if [ -d "./graalvm" ]; then
   echo "GraalVM ... OK"
else
    echo "GraalVM ... MISSING"
    wget https://github.com/oracle/graal/releases/download/vm-1.0.0-rc3/graalvm-ce-1.0.0-rc3-linux-amd64.tar.gz
    tar -xvzf graalvm-ce-1.0.0-rc3-linux-amd64.tar.gz
    rm graalvm-ce-1.0.0-rc3-linux-amd64.tar.gz
    mkdir ./graalvm
    mv ./graalvm-ce-1.0.0-rc3/* ./graalvm/
    rm -r ./graalvm-1.0.0-rc3
    echo "GraalVM ... INSTALLED"
fi

# CHECK SCALABENCH DEPENDENCY
if [ -f "scalabench.jar" ]; then
   echo "ScalaBench ... OK"
else
    echo "ScalaBench ... MISSING"
    wget http://repo.scalabench.org/snapshots/org/scalabench/benchmarks/scala-benchmark-suite/0.1.0-SNAPSHOT/scala-benchmark-suite-0.1.0-20120216.103539-3.jar
    mv scala-benchmark-suite-0.1.0-20120216.103539-3.jar scalabench.jar
    echo "ScalaBench ... INSTALLED"
fi

echo "<<<JVM VERSION>>>"
./graalvm/bin/java -version