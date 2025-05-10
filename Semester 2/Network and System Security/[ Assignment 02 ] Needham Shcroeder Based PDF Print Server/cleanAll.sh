#!/bin/bash

# cleanCompiledBinaries
echo "Cleaning binaries..."
make clean

# cleanLogFiles
echo "Cleaning log files..."
rm -f server.log

echo "Cleanup complete."