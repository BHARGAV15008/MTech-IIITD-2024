/**
 * @file KsTest.cpp
 * @brief Implementation of the Kolmogorov-Smirnov test
 * 
 * This file contains the implementation of the KsTest class methods
 * for performing the two-sample KS test.
 */

 #include "KsTest.hpp"
 #include <algorithm>
 #include <cmath>
 #include <iostream>
 
 bool KsTest::performTest(const std::vector<double>& sampleP, 
                          const std::vector<double>& sampleQ, 
                          double alpha, 
                          int granularity) {
     // Check if samples are valid
     if (sampleP.empty() || sampleQ.empty()) {
         std::cerr << "Error: Empty sample provided to KS test" << std::endl;
         return false;
     }
     
     // Find range of the second sample (Q)
     double minQ = *std::min_element(sampleQ.begin(), sampleQ.end());
     double maxQ = *std::max_element(sampleQ.begin(), sampleQ.end());
     double range = maxQ - minQ;
     
     // Generate points for CDF evaluation based on granularity
     std::vector<double> evaluationPoints;
     for (int i = 0; i <= granularity; i++) {
         double point = minQ + (i * range / granularity);
         evaluationPoints.push_back(point);
     }
     
     // Calculate CDFs for both samples at evaluation points
     std::vector<double> cdfP = calculateCdf(sampleP, evaluationPoints);
     std::vector<double> cdfQ = calculateCdf(sampleQ, evaluationPoints);
     
     // Find maximum difference between CDFs (KS statistic)
     double maxDifference = 0.0;
     for (size_t i = 0; i < evaluationPoints.size(); i++) {
         double difference = std::abs(cdfP[i] - cdfQ[i]);
         if (difference > maxDifference) {
             maxDifference = difference;
         }
         
         // Optimization: if we've reached CDF = 1 for sample P, we can stop
         if (cdfP[i] >= 1.0) {
             break;
         }
     }
     
     // Calculate critical value based on sample sizes and significance level
     double criticalValue = calculateCriticalValue(sampleP.size(), sampleQ.size(), alpha);
     
     // Decision: accept null hypothesis if KS statistic <= critical value
     // This means the samples likely come from the same distribution
     return maxDifference <= criticalValue;
 }
 
 std::vector<double> KsTest::calculateCdf(const std::vector<double>& sample, 
                                         const std::vector<double>& points) {
     std::vector<double> cdf;
     
     for (const double& x : points) {
         // Count how many elements are less than or equal to x
         int count = 0;
         for (const double& value : sample) {
             if (value <= x) {
                 count++;
             }
         }
         
         // CDF value is the proportion of elements <= x
         double cdfValue = static_cast<double>(count) / sample.size();
         cdf.push_back(cdfValue);
     }
     
     return cdf;
 }
 
 double KsTest::calculateCriticalValue(int sizeP, int sizeQ, double alpha) {
     // c(alpha) calculation as per equation in the paper
     double cAlpha = std::sqrt(-std::log(alpha / 2.0) / 2.0);
     
     // Critical value calculation based on sample sizes and c(alpha)
     return cAlpha * std::sqrt((static_cast<double>(sizeP + sizeQ)) / (sizeP * sizeQ));
 }