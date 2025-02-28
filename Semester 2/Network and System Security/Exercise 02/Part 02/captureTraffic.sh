#!/bin/bash
# captureTraffic.sh - Captures network traffic using tcpdump

source aesConfig.sh

case "$1" in
  start)
    echo "Starting packet capture on ports $SERVER_PORT and $CLIENT_PORT..."
    
    # Check if running as root (required for tcpdump)
    if [ "$(id -u)" -ne 0 ]; then
      echo "Error: This script must be run as root to capture packets."
      echo "Try: sudo $0 start"
      exit 1
    fi
    
    # Start tcpdump in background to capture traffic on specified ports
    tcpdump -i lo -w "$PCAP_FILE" "port $SERVER_PORT or port $CLIENT_PORT" &
    
    # Save PID for stopping later
    echo $! > tcpdump.pid
    
    echo "Capture started. Run 'sudo $0 stop' to end capture."
    echo "Traffic is being saved to $PCAP_FILE"
    ;;
    
  stop)
    if [ ! -f tcpdump.pid ]; then
      echo "Error: No capture process found. Start capture first."
      exit 1
    fi
    
    # Check if running as root
    if [ "$(id -u)" -ne 0 ]; then
      echo "Error: This script must be run as root to stop the capture."
      echo "Try: sudo $0 stop"
      exit 1
    fi
    
    # Kill the tcpdump process
    echo "Stopping packet capture..."
    kill $(cat tcpdump.pid)
    rm tcpdump.pid
    
    echo "Capture stopped. Captured packets saved to $PCAP_FILE"
    
    # Show a summary of the captured packets
    echo "Capture summary:"
    tcpdump -r "$PCAP_FILE" -n | head -10
    echo "..."
    echo "Use 'wireshark $PCAP_FILE' to view the full capture."
    ;;
    
  *)
    echo "Usage: $0 [start|stop]"
    echo ""
    echo "start - Begin capturing traffic on ports $SERVER_PORT and $CLIENT_PORT"
    echo "stop  - Stop capturing and save the results"
    ;;
esac