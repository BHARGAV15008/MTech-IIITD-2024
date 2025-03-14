#!/bin/bash
# KillExistingInstances
pkill -9 kdcServer 2>/dev/null
pkill -9 prnSrv 2>/dev/null
sleep 1  # Wait for ports to release

# StartFreshServers
./bin/kdcServer &
./bin/prnSrv &

# WaitForInitialization
sleep 2

# RunClientWithInputFile
if [ $# -eq 1 ]; then
    ./bin/client "$1"
else
    echo "Usage: $0 <filename>"
fi

# Cleanup
pkill -9 kdcServer
pkill -9 prnSrv