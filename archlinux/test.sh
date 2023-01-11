#!/bin/bash
export SSHPASS=passw0rd

until sshpass -e ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no arch@localhost -p 2222
do
echo "Trying" 
sleep 5 
done