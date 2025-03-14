/**
 * @file KsTest.hpp
 * @brief Header file for the Kolmogorov-Smirnov test implementation
 * 
 * This file declares the KsTest class which provides methods to perform
 * the two-sample Kolmogorov-Smirnov test for comparing distributions.
 */

 #ifndef KS_TEST_HPP
 #define KS_TEST_HPP
 
 #include <vector>
 
 /**
  * @class KsTest
  * @brief Implements the Kolmogorov-Smirnov statistical test
  * 
  * This class provides methods to perform the two-sample KS test to determine
  * if two samples come from the same distribution.
  */
 class KsTest {
 public:
     /**
      * @brief Default constructor
      */
     KsTest() = default;
     
     /**
      * @brief Performs the Two-Sample Kolmogorov-Smirnov test
      * 
      * This method implements the KS test to determine if two samples come from
      * the same distribution. It calculates the maximum difference between the
      * empirical distribution functions and compares with a critical value.
      * 
      * @param sampleP Vector of values from the first sample
      * @param sampleQ Vector of values from the second sample
      * @param alpha Significance level (typically 0.05 or 0.10)
      * @param granularity Number of points to use for CDF comparison
      * @return true if samples likely come from the same distribution, false otherwise
      */
     bool performTest(const std::vector<double>& sampleP, 
                      const std::vector<double>& sampleQ, 
                      double alpha, 
                      int granularity);
 
 private:
     /**
      * @brief Calculates the Cumulative Distribution Function (CDF) of a given sample
      * 
      * @param sample Vector of values
      * @param points Vector of points at which to evaluate the CDF
      * @return Vector of CDF values corresponding to each point
      */
     std::vector<double> calculateCdf(const std::vector<double>& sample, 
                                     const std::vector<double>& points);
     
     /**
      * @brief Calculates the critical value for the KS test
      * 
      * @param sizeP Size of the first sample
      * @param sizeQ Size of the second sample
      * @param alpha Significance level
      * @return The critical value for the given parameters
      */
     double calculateCriticalValue(int sizeP, int sizeQ, double alpha);
 };
 
 #endif // KS_TEST_HPP