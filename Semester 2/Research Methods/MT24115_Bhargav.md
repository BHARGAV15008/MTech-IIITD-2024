# CJ-Sniffer: Measurement and Content-Agnostic Detection of Cryptojacking Traffic

## Authors and Publication
This research paper, *CJ-Sniffer: Measurement and Content-Agnostic Detection of Cryptojacking Traffic*, is written by **Yebo Feng, Jun Li, and Devkishen Sisodia** from the **University of Oregon, USA**. It was published in the **25th International Symposium on Research in Attacks, Intrusions, and Defenses (RAID 2022)**, held in **Limassol, Cyprus**. The paper is available in the ACM Digital Library.

## Introduction
**Cryptojacking** is an attack where hackers secretly use computing resources to mine cryptocurrency, such as Bitcoin or Monero, without permission. This slows down devices, increases electricity bills, and affects system performance. Many victims do not realize their devices are being misused.

Traditional detection methods, such as antivirus software and browser extensions, are ineffective for large networks (e.g., offices, universities). Managing software on multiple endpoints is difficult.

To solve this problem, **CJ-Sniffer** was developed. It is a **network-based system** that detects cryptojacking without inspecting private data. Instead of analyzing content, it monitors **network traffic patterns** to identify cryptojacking activity.

## Methodology and Results
CJ-Sniffer works in **three phases**:

1. **Traffic Filtration** – Removes irrelevant network traffic (e.g., general browsing, emails, media streaming) to focus on suspicious activity.
2. **Cryptomining Detection** – Uses **packet interval analysis** and a **Kolmogorov-Smirnov (KS) test** to detect mining activities.
3. **Cryptojacking Detection** – Uses a **Long Short-Term Memory (LSTM) machine learning model** to differentiate between **user-initiated mining** and **unauthorized cryptojacking**.

### **Key Findings**
- **CJ-Sniffer achieves 99% accuracy** in detecting cryptojacking.
- **Fast real-time detection** makes it ideal for large networks.
- **Privacy-focused** – Does not inspect packet content, ensuring user privacy.

## Challenges
CJ-Sniffer faces the following challenges:
- **Cryptojacking traffic is small** – Hard to detect compared to general internet traffic.
- **Hackers use evasion techniques** – Attackers use encryption, VPNs, and proxies to hide mining activity.
- **Balancing speed and accuracy** – Needs to operate in real-time while keeping false positives low.

## Results
- **CJ-Sniffer successfully detects cryptojacking with 99% accuracy**.
- **Real-time processing ensures quick detection in enterprise networks**.
- **Unlike traditional methods, CJ-Sniffer differentiates between legal and unauthorized mining**.

## Conclusion
CJ-Sniffer is an effective tool for detecting cryptojacking in **large-scale networks**. Unlike traditional methods, it does not block all cryptocurrency mining but specifically targets **unauthorized mining**.

### **Future Improvements**
- Expanding detection to **more cryptocurrencies**.
- Enhancing resistance to **advanced evasion techniques**.

CJ-Sniffer provides a **robust, privacy-preserving, and efficient** solution to protect networks from cryptojacking attacks.

## Reference
Yebo Feng, Jun Li, Devkishen Sisodia. *CJ-Sniffer: Measurement and Content-Agnostic Detection of Cryptojacking Traffic.* 25th International Symposium on Research in Attacks, Intrusions, and Defenses (RAID 2022), October 26–28, 2022, Limassol, Cyprus. DOI: [https://doi.org/10.1145/3545948.3545973](https://doi.org/10.1145/3545948.3545973)

