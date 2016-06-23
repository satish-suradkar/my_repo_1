#!/bin/bash -ex

echo "enter number"
read N1 
read N2

SUM=`expr $N1 + $N2`
echo "SUM="$SUM
