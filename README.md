Random value token payment 
======

This repository comprises code and instructions to run the prototype implementing the random-value token payment solution introduced in the paper "Random-value payment tokens for on-chain privacy-preserving payments". 


Requirements:
----
* truffle 
* ganache-cli
* python version>3 

Set up the environment:
----
```pip3 install requirements.txt```

Launch the platform: 
----
* (1) Launch the ganache test blockchain using the following command: 
```./scripts/launch.sh```
* (2) Then, launch the following script to execute the scenario:
```cd back && python3 test_scenario.py```
* (3) From the front end, you can (i) generate a new payment token, (ii) launch token payments upon request, and (iii) disable the token after the collaboration between two participants terminates.   

Contact and support information:
---
Please contact tiphaine.henry@orange.com or julien.hatin@orange.com if you have any question regarding the code. 
