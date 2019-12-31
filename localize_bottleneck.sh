#!/usr/bin/env bash

# edit in the test_(algo) methods below, update the path to each algo if needed
delay=50
dst_ip=3.135.64.30

action=$1
algo=$2
run_number=$3
[ -z action ] || [ -z algo ] || [ -z run_number ] && exit 1

test_bbr(){
  sudo tcpdump -i ingress -w data/sender${run_number}.pcap &
  iperf3 -c ${dst_ip}
}

test_vivace(){
  sudo tcpdump -i ingress -w data/sender${run_number}.pcap &
  timeout 15 ./PCC-Uspace/src/app/pccclient send ${dst_ip} 9000
}

test_copa(){
  sudo tcpdump -i ingress -w data/sender${run_number}.pcap &
  ./genericCC/sender serverip=${dst_ip} offduration=0 onduration=15000 cctype=markovian delta_conf=do_ss:auto:0.5 traffic_params=deterministic,num_cycles=1
}

if   [ "${action}" == "start" ]; then
  mm-delay ${delay} "./localize_bottleneck.sh" inside_delay ${algo} ${run_number}
elif [ "${action}" == "inside_delay" ]; then
  sudo tcpdump -i ingress -w data/recv${run_number}.pcap &
  mm-link ./trace.txt ./trace.txt "./localize_bottleneck.sh" inside_link ${algo} ${run_number}
elif [ "${action}" == "inside_link" ]; then
  test_${algo}
fi