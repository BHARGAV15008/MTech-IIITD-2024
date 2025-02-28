**Summary of "MineHunter: A Practical Cryptomining Traffic Detection Algorithm
Based on Time Series Tracking"**

**Authors and Publication**
This research paper "MineHunter: A Practical Cryptomining Traffic Detection Algorithm
Based on Time Series Tracking" is written by Shize Zhang, Zhiliang Wang, Jiahai Yang,
Xin Cheng, Xiaoqian Ma, Hui Zhang, Bo Wang, Zimu Li, and Jianping Wu from Tsinghua
University, China and Beijing Wuzi University, China. It was published in the Annual
Computer Security Applications Conference (ACSAC '21), December 6–10, 2021, Virtual
Event, USA. The paper is available at ACM Digital Library with DOI
https://doi.org/10.1145/3485832.3485835.

**Introduction**
Cryptojacking is when hackers secretly use other people's computers to mine
cryptocurrency like Bitcoin or Monero. This makes the computer slow, uses a lot of
electricity, and internet becomes slow. Many people do not know their computer is
mining for hackers.

Old methods to stop cryptojacking include antivirus software and browser plugins, but
these are not good for big networks like schools, offices, and companies. Installing
software on every computer is difficult.

To solve this problem, MineHunter was developed. It is a new system that can detect
cryptojacking at the network level. It does not need installation on computers and works
by checking network traffic at the main router.

This research tested MineHunter in a real-world campus network with 28 TB of data and
30 billion network packets. The system found cryptojacking with 97% accuracy and
99.7% recall.

**Methodology and Results**
MineHunter uses a smart technique to find cryptojacking by checking time series
tracking. It looks at when cryptocurrency blocks are created and compares this with
internet traffic. If a computer sends mining requests at the same time as block creation,
it is probably mining.

MineHunter works in 3 steps:

1. Traffic Collection – It monitors network traffic at the gateway and collects data.
2. Block Creation Tracking – It connects to cryptocurrency networks (like Bitcoin,
Monero) and tracks block creation times.
3. Detection Algorithm – It compares network traffic with block creation and detects
mining activity.


**Challenges**
MineHunter faces many challenges in cryptojacking detection:

- Cryptojacking traffic is very small – Normal traffic is huge, but mining traffic is very
little (only 1 in 200,000 packets).
- Hackers try to hide mining – They use VPNs, proxies, and encryption to make mining
invisible.
- Too many false alarms – If too many computers are wrongly detected, it is hard for
administrators.
- Fast detection is needed – The system must work in real-time for big networks.

**Results**
MineHunter was tested in a big school network. It analyzed 28 terabytes of data over
one month and found:

- 97.0% precision – If MineHunter says a computer is mining, it is correct 97 times out
of 100.
- 99.7% recall – It detects almost all mining computers in the network.
- Fast processing – It can analyze 350,000 packets per second and work on high-speed
networks.

**Conclusion**
MineHunter is very useful to detect cryptojacking in big networks like schools, offices,
and companies. It does not need software installation and can find even hidden
cryptojacking. However, it cannot tell if mining is legal or illegal.

In the future, researchers want to improve MineHunter using AI and machine learning.
They also want to automatically block cryptojacking when detected.

MineHunter is a fast, accurate, and powerful system to protect big networks from
cryptojacking attacks.

**Reference**
Shize Zhang, Zhiliang Wang, Jiahai Yang, Xin Cheng, Xiaoqian Ma, Hui Zhang, Bo Wang,
Zimu Li, and Jianping Wu. "MineHunter: A Practical Cryptomining Traffic Detection
Algorithm Based on Time Series Tracking." Annual Computer Security Applications
Conference (ACSAC '21), December 6–10, 2021, Virtual Event, USA.
DOI: https://doi.org/10.1145/3485832.


