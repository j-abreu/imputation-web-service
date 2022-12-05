#!/bin/sh
for ARGUMENT in "$@"
do
   KEY=$(echo $ARGUMENT | cut -f1 -d=)

   KEY_LENGTH=${#KEY}
   VALUE="${ARGUMENT:$KEY_LENGTH+1}"

   export "$KEY"="$VALUE"
done

cd ~/tests/results/$METHOD
N_TESTS=$(ls | wc -l)
echo "----------------------------"
echo "CURRENT TESTS: $N_TESTS"
ls
echo ""

echo "LAST AGGREAGATE REPORT"
cd ./$N_USERS-users
cat aggregate-results.csv
echo ""

