#! /bin/sh
mkdir ./Code/simulation_cpp/src
cp ./Code/codeMicrocontroleur/ControleFunibot/* ./Code/simulation_cpp/src
cd ./Code/simulation_cpp/src

for f in *.ino
do
    [ -f "$f" ] && mv -f "$f" "${f%ino}cpp"
done
