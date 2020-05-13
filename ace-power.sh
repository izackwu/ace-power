help()
{
   echo ""
   echo "Usage: $0 [start | stop] num"
   echo -e "\t num: number of instances to start"
   exit 1 # Exit script after printing help
}

if [ "$1" == "start" ] && [ ! -z "$2" ]; then
  mkdir -p log
  for i in $(seq -f "%02g" 0 $(($2-1))) ; do
    echo "Start application: ace-power-$i"
    uvicorn server:app --proxy-headers --uds /tmp/ace-power-$i.sock &> log/ace-power-$i.log &
  done
elif [ "$1" == "stop" ]; then
  echo "Stop all!"
  pkill -f uvicorn
else
  echo "Incorrect usage!"
  help
fi


