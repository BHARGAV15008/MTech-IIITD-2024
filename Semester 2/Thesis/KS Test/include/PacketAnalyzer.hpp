/**
 * @file PacketAnalyzer.hpp
 * @brief Header file for packet analysis and cryptomining detection
 * 
 * This file declares the PacketAnalyzer class which provides methods
 * for analyzing network packets and detecting cryptomining traffic.
 */

 #ifndef PACKET_ANALYZER_HPP
 #define PACKET_ANALYZER_HPP
 
 #include "KsTest.hpp"
 #include <vector>
 
 /**
  * @class PacketAnalyzer
  * @brief Analyzes network packets to detect cryptomining traffic
  * 
  * This class provides methods to process network packets and determine
  * if they match known cryptomining traffic patterns using KS test.
  */
 class PacketAnalyzer {
 public:
     /**
      * @brief Constructor that takes known cryptomining traffic pattern
      * 
      * @param knownMiningPackets Vector of packet timestamps from known cryptomining traffic
      */
     PacketAnalyzer(const std::vector<double>& knownMiningPackets);
     
     /**
      * @brief Extract inbound packet intervals from a list of packets
      * 
      * This method takes a vector of packet timestamps and calculates the time
      * differences between consecutive packets, which represent the intervals.
      * 
      * @param packets Vector of packet timestamps (in microseconds)
      * @return Vector of time intervals between consecutive packets
      */
     std::vector<double> extractInboundIntervals(const std::vector<double>& packets);
     
     /**
      * @brief Detects if traffic matches cryptomining patterns
      * 
      * This method implements the main detection algorithm from the CJ-Sniffer paper.
      * It takes packet timing information and determines if the traffic matches
      * known cryptomining patterns using the KS test.
      * 
      * @param testPackets Vector of packet timestamps to be tested
      * @param alpha Significance level (typically 0.10 as per the paper)
      * @param granularity Number of points to use for KS statistic calculation
      * @return true if traffic is identified as cryptomining, false otherwise
      */
     bool detectCryptominingTraffic(const std::vector<double>& testPackets,
                                   double alpha = 0.10, 
                                   int granularity = 100);
 
 private:
     // Known cryptomining packet timestamps
     std::vector<double> knownMiningPackets;
     
     // Known cryptomining packet intervals (calculated once during construction)
     std::vector<double> knownMiningIntervals;
     
     // KS test implementation
     KsTest ksTest;
 };
 
 #endif // PACKET_ANALYZER_HPP