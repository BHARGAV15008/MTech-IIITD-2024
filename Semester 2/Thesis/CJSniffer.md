# **CJ-Sniffer: Measurement and Content-Agnostic Detection of Cryptojacking Traffic**

## **1. Introduction**

Cryptojacking is the unauthorized use of computing resources to mine cryptocurrency. Attackers infect devices with mining scripts or malware, leading to power consumption and financial losses. CJ-Sniffer is a novel detection system that differentiates cryptojacking traffic from legitimate user-initiated cryptomining while maintaining privacy and efficiency.

## **2. Key Contributions**

1. **Content-Agnostic Detection** - CJ-Sniffer does not inspect packet payloads, preserving user privacy.
2. **Distinguishing Cryptojacking vs. User-Initiated Mining** - Unlike previous methods that block all mining traffic, CJ-Sniffer selectively detects unauthorized mining.
3. **Efficient Deployment** - Can be installed at network gateways to monitor and protect entire networks in real-time.
4. **Public Dataset** - First labeled, packet-level cryptomining dataset made available for research.

## **3. CJ-Sniffer's Three-Phase Detection Approach**

### **Phase 1: Rapid Filtration**

- Filters out irrelevant traffic based on packet size and protocol.
- Groups packets into connections for further analysis.
- Uses a sliding time window to check for cryptomining characteristics.

### **Phase 2: Cryptomining Detection**

- Uses packet interval distributions to identify cryptomining traffic.
- Employs the **Two-Sample Kolmogorov–Smirnov (KS) test** to compare intervals with labeled cryptomining traffic.
- High accuracy in detecting mining activity with minimal data collection.

### **Phase 3: Cryptojacking Detection**

- Uses **Long Short-Term Memory (LSTM)** neural networks to analyze variations in result submission frequency.
- Cryptojacked devices often have unstable mining rates due to execution priority and system constraints.
- Outputs classifications as cryptojacking, user-initiated mining, or normal traffic.

## **4. Dataset and Evaluation**

- Collected over **750 hours** of cryptomining traffic across different CPUs and GPUs.
- Measured against **real-world campus and lab traffic** (316GB data).
- **Achieved over 99% accuracy** with minimal false positives.
- **Detects other Proof-of-Work (PoW) cryptocurrencies** (ETH, BTC, ZEC) but struggles with Proof-of-Space mining (e.g., CHIA).

## **5. Comparisons with Other Methods**

| Approach       | Content-Agnostic | Detects Cryptojacking? |
| -------------- | ---------------- | ---------------------- |
| DPI-based      | ❌                | ❌                      |
| Cisco Solution | ✅                | ❌                      |
| MineHunter     | ✅                | ❌                      |
| CJ-Sniffer     | ✅                | ✅                      |

## **6. System Efficiency**

- Time Complexity: **O(n)** (linear with the number of packets).
- Processes **200-400 packets in under 400ms**, making it suitable for real-time detection.
- Works efficiently on **1 Gbps to 10 Gbps network links**.

## **7. Limitations and Open Issues**

- Less effective when cryptojacked devices have stable hash rates.
- Struggles with non-PoW mining algorithms.
- Requires **periodic model updates** for emerging mining techniques.

---

# **Possible Questions & Answers for Presentation**

### **1. What is cryptojacking, and why is it a problem?**

- Cryptojacking is the unauthorized use of computing resources to mine cryptocurrency. It leads to increased power consumption, system slowdowns, and financial losses.

### **2. How does CJ-Sniffer differ from traditional cryptomining detection methods?**

- Unlike traditional methods that block all mining traffic, CJ-Sniffer distinguishes between cryptojacking and user-initiated mining while maintaining user privacy.

### **3. What is the role of the Kolmogorov-Smirnov (KS) test in CJ-Sniffer?**

- The KS test compares packet interval distributions to determine if traffic resembles cryptomining activity.

### **4. Why does CJ-Sniffer use an LSTM model?**

- LSTMs are effective for time-series data, allowing CJ-Sniffer to detect unstable mining behavior typical of cryptojacking.

### **5. What are the three phases of CJ-Sniffer's detection approach?**

1. **Rapid Filtration** - Filters irrelevant connections.
2. **Cryptomining Detection** - Identifies mining traffic using KS testing.
3. **Cryptojacking Detection** - Uses LSTM to distinguish cryptojacking from user-initiated mining.

### **6. How does CJ-Sniffer protect user privacy?**

- It only analyzes anonymized metadata (packet size, timestamps) and does not inspect payload contents.

### **7. Can CJ-Sniffer detect all types of cryptomining?**

- It effectively detects PoW-based mining (e.g., BTC, ETH, XMR) but struggles with Proof-of-Space mining (e.g., CHIA).

### **8. What are the limitations of CJ-Sniffer?**

- Ineffective when cryptojacked devices have stable hash rates.
- Requires frequent model updates for new mining techniques.

### **9. How does CJ-Sniffer compare with MineHunter?**

- Both achieve high detection rates, but CJ-Sniffer has lower false positives and is the only method that distinguishes cryptojacking from legitimate mining.

### **10. How can CJ-Sniffer be deployed in a real-world setting?**

- It can be installed at a network gateway or as a cloud-based IDS service to protect all devices in a network.

---

This document provides a comprehensive understanding of CJ-Sniffer and prepares you for an in-depth presentation.

