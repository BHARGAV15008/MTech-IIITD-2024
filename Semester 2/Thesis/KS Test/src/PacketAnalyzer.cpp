/**
 * @file PacketAnalyzer.cpp
 * @brief Implementation of packet analysis and cryptomining detection
 * 
 * This file contains the implementation of the PacketAnalyzer class methods
 * for analyzing network packets and detecting cryptomining traffic.
 */

 #include "PacketAnalyzer.hpp"

 PacketAnalyzer::PacketAnalyzer(const std::vector<double>& knownMiningPackets) 
     : knownMiningPackets(knownMiningPackets) {
     // Pre-calculate the intervals for known cryptomining traffic
     // This optimization is mentioned in the paper
     knownMiningIntervals = extractInboundIntervals(knownMiningPackets);
 }
 
 std::vector<double> PacketAnalyzer::extractInboundIntervals(const std::vector<double>& packets) {
     std::vector<double> intervals;
     
     // Need at least 2 packets to calculate intervals
     if (packets.size() < 2) {
         return intervals;
     }
     
     // Calculate time difference between consecutive packets
     for (size_t i = 1; i < packets.size(); i++) {
         double interval = packets[i] - packets[i - 1];
         intervals.push_back(interval);
     }
     
     return intervals;
 }
 
 bool PacketAnalyzer::detectCryptominingTraffic(const std::vector<double>& testPackets, double alpha, int granularity) {
     // Step 1: Extract inbound packet intervals from test traffic
     std::vector<double> testIntervals = extractInboundIntervals(testPackets);
     
     // Step 2: Perform KS test to compare distributions
     // If the distributions are similar enough (based on the significance level),
     // the test will return true, indicating cryptomining traffic
     return ksTest.performTest(testIntervals, knownMiningIntervals, alpha, granularity);
 }