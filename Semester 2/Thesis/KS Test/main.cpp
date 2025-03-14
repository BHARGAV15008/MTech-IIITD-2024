/**
 * @file Main.cpp
 * @brief Entry point for the Kolmogorov-Smirnov test based cryptomining detector
 * 
 * This file contains the main function and example usage for the KS test
 * based cryptomining traffic detection system.
 */

 #include "KsTest.hpp"
 #include "PacketAnalyzer.hpp"
 #include <iostream>
 #include <vector>
 
 /**
  * @brief Example usage of the cryptomining detection system
  */
 void exampleUsage() {
     // Example packet timestamps (in milliseconds since epoch)
     std::vector<double> suspiciousTraffic = {
         1000.0, 1014.5, 1029.2, 1044.1, 1058.4, 1072.9, 1087.3, 1101.8
     };
     
     // Known cryptomining traffic packet timestamps
     std::vector<double> knownCryptominingTraffic = {
         2000.0, 2014.6, 2029.1, 2043.5, 2058.1, 2072.6, 2087.2, 2101.8
     };
     
     // Initialize packet analyzer with known cryptomining pattern
     PacketAnalyzer analyzer(knownCryptominingTraffic);
     
     // Detect if suspicious traffic is cryptomining
     bool result = analyzer.detectCryptominingTraffic(
         suspiciousTraffic,
         0.10,       // Significance level (alpha)
         100         // Granularity (k)
     );
     
     // Output detection result
     if (result) {
         std::cout << "Detected: Traffic matches cryptomining patterns" << std::endl;
     } else {
         std::cout << "Not Detected: Traffic does not match cryptomining patterns" << std::endl;
     }
 }
 
 /**
  * @brief Main function
  * 
  * In a production environment, this would be integrated with packet capture
  * libraries like libpcap to analyze live network traffic.
  */
 int main() {
     // Example usage demonstration
     exampleUsage();
     
     return 0;
 }