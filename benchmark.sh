#!/usr/bin/env bash

algorithm_count=3
algorithms=(bbr vivace copa)

red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'

pcap_to_csv(){
  echo -e "[${green}Converting recv data to .csv format${plain}]"
  tshark -r data/recv$1.pcap -T fields -e frame.number -e frame.time_relative -e frame.len -e ip.dst -E header=y -E separator=, -E quote=d -E occurrence=f > data/recv$1.csv
  rm -f data/recv$1.pcap
}

mkdir -p data

while true
do
echo "Which rate-base CC algorithm you want to benchmark?"
for ((i=1;i<=${#algorithms[@]};i++ )); do
  hint="${algorithms[$i-1]}"
  echo -e "${green}${i}${plain}) ${hint}"
done
read -p "Please enter a number [1-${algorithm_count}]:" selection
case "${selection}" in
  1|2|3|4)
  echo
  echo "You chose = ${algorithms[${selection}-1]}"
  echo
  break
  ;;
  *)
  echo -e "[${red}Error${plain}] Please only enter a number [1-${algorithm_count}]"
  ;;
esac
done

while true
do
echo "How many times you will run it?"
read -p "Please enter a number:" count
case ${count} in
  *[!0-9]* | '')
    echo -e "[${red}Error${plain}] Please only enter a number"
    ;;
  *) echo
  echo "You entered = ${count}"
  echo
  break
  ;;
esac
done

if   [ "${selection}" == "1" ]; then
  for (( i=1; i<=${count}; i++ ))
  do
    clear
    echo -e "[${green}Run number ${yellow}$i${plain}]"
    "./localize_bottleneck.sh" start ${algorithms[${selection}-1]} $i
    wait
    sleep 3
    pcap_to_csv $i
    sleep 3
  done
fi

if   [ "${selection}" == "2" ]; then
  for (( i=1; i<=${count}; i++ ))
  do
    clear
    echo -e "[${green}Run number ${yellow}$i${plain}]"
    "./localize_bottleneck.sh" start ${algorithms[${selection}-1]} $i
    wait
    sleep 3
    pcap_to_csv $i
    sleep 3
  done
fi

if   [ "${selection}" == "3" ]; then
  for (( i=1; i<=${count}; i++ ))
  do
    clear
    echo -e "[${green}Run number ${yellow}$i${plain}]"
    "./localize_bottleneck.sh" start ${algorithms[${selection}-1]} $i
    wait
    pcap_to_csv $i
    sleep 3
  done
fi
