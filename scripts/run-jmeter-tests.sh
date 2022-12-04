#!/bin/sh
for ARGUMENT in "$@"
do
   KEY=$(echo $ARGUMENT | cut -f1 -d=)

   KEY_LENGTH=${#KEY}
   VALUE="${ARGUMENT:$KEY_LENGTH+1}"

   export "$KEY"="$VALUE"
done

./apache-jmeter-5.5/bin/jmeter -n -t ../repos/imputation-web-service/tests/MainTest.jmx -l ./results/$METHOD/$N_USERS-users/results.jtl
./apache-jmeter-5.5/bin/JMeterPluginsCMD.sh --generate-csv ./results/$METHOD/$N_USERS-users/aggregate-results.csv --input-jtl ./results/$METHOD/$N_USERS-users/results.jtl --plugin-type AggregateReport

