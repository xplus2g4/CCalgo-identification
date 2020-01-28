#!/usr/bin/env bash

# edit in the test_(algo) methods below, update the path to each algo if needed
delay=1
dst_ip=18.136.106.11

action=$1
algo=$2
run_number=$3

[ -z action ] || [ -z algo ] || [ -z run_number ] && exit 1

test_bbr(){
  rtt=$(ping -c 4 ${dst_ip} | tail -1| awk '{print int($4)}' | cut -d '/' -f 2)
  echo -e "[${green}RTT in delay and link shell= ${yellow}${rtt}ms${plain}]"
  sudo tcpdump -i ingress -w data/sender-${rtt}-${run_number}.pcap &
  iperf3 -c ${dst_ip} -t 15
  echo -e "[${green}Converting sender data to .csv format${plain}]"
  tshark -r data/sender-${rtt}-${run_number}.pcap -T fields -e frame.number -e frame.time_relative -e frame.len -e ip.dst -E header=y -E separator=, -E quote=d -E occurrence=f > data/sender-${rtt}-${run_number}.csv
  rm -f data/sender-${rtt}-${run_number}.pcap
}

test_vivace(){
  rtt=$(ping -c 4 ${dst_ip} | tail -1| awk '{print int($4)}' | cut -d '/' -f 2)
  echo -e "[${green}RTT in delay and link shell= ${yellow}${rtt}ms${plain}]"
  sudo tcpdump -i ingress -w data/sender-${rtt}-${run_number}.pcap &
  timeout 15 ./PCC-Uspace/src/app/pccclient send ${dst_ip} 9000
  echo -e "[${green}Converting sender data to .csv format${plain}]"
  tshark -r data/sender-${rtt}-${run_number}.pcap -T fields -e frame.number -e frame.time_relative -e frame.len -e ip.dst -E header=y -E separator=, -E quote=d -E occurrence=f > data/sender-${rtt}-${run_number}.csv
  rm -f data/sender-${rtt}-${run_number}.pcap
}

test_copa(){
  rtt=$(ping -c 4 ${dst_ip} | tail -1| awk '{print int($4)}' | cut -d '/' -f 2)
  echo -e "[${green}RTT in delay and link shell= ${yellow}${rtt}${plain}]"
  sudo tcpdump -i ingress -w data/sender-${rtt}-${run_number}.pcap &
  ./genericCC/sender serverip=${dst_ip} offduration=0 onduration=15000 cctype=markovian delta_conf=do_ss:auto:0.5 traffic_params=deterministic,num_cycles=1
  echo -e "[${green}Converting sender data to .csv format${plain}]"
  tshark -r data/sender-${rtt}-${run_number}.pcap -T fields -e frame.number -e frame.time_relative -e frame.len -e ip.dst -E header=y -E separator=, -E quote=d -E occurrence=f > data/sender-${rtt}-${run_number}.csv
  rm -f data/sender-${rtt}-${run_number}.pcap
}

if   [ "${action}" == "start" ]; then
  mm-delay ${delay} "./localize_bottleneck.sh" inside_delay ${algo} ${run_number}
elif [ "${action}" == "inside_delay" ]; then
  sudo tcpdump -i ingress -w data/recv${run_number}.pcap &
  mm-link ./trace.txt ./trace.txt "./localize_bottleneck.sh" inside_link ${algo} ${run_number}
elif [ "${action}" == "inside_link" ]; then
  test_${algo}
fi
