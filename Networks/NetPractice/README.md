*This activity has been created as part of the 42 curriculum by mel-shdo.*

## Description
NetPractice is a general practical exercise designed to introduce the basics of computer networking. The goal of this activity is to solve networking problems and configure small-scale networks to make them function properly. It helps build an understanding of how TCP/IP addressing works, including concepts such as the subnet mask and the default gateway, by simulating networks in a training interface. I learned to configure IP addresses, connect devices through a router, and understand the role of a gateway within a network.

## Instructions
1. Download the file attached to the activity's page and extract the files into a folder of your choice.
2. In this folder, run the `run.sh` script to launch a local web server and open the training interface in your preferred web browser. 
3. If the `run.sh` script does not function properly due to browser security constraints, you can run the server manually: `python3 -m http.server 49242` (you may change the port), then navigate to `http://localhost:49242` in your web browser.
4. Enter your login in the training interface to use your personal configuration. Alternatively, use the "evaluation" tab to generate a random configuration.
5. You must complete 10 levels (10 exercises). For each level, modify the unshaded fields until your network configuration is correct. Use the **Check again** button to verify whether your configuration is correct.
6. Once a level is completed, export your configuration by clicking the **Get my config** button.

### Submission Details
You must submit 10 exported configuration files (one file per level). These 10 files must be placed at the root of your Git repository. Don't forget to enter your login in the training interface before exporting.

## Resources
The following networking concepts are studied in this project:
- **TCP/IP addressing**: Understanding IP addresses and how networks communicate. : https://www.geeksforgeeks.org/computer-networks/tcp-ip-model/
- **Subnet masks**: Defining the boundaries of the local network. : https://www.geeksforgeeks.org/computer-networks/introduction-to-subnetting/
- **Default gateways**: Routing traffic outside the local network. : https://www.geeksforgeeks.org/computer-networks/default-gateway-in-networking/
- **Routers and switches**: Devices used to connect networks and forward data packets.: https://www.cisco.com/site/us/en/learn/topics/small-business/network-switch-vs-router.html
- **OSI layers**: Understanding the theoretical model of network communication. : https://www.imperva.com/learn/application-security/osi-model/

*AI Usage Description:*
Used AI as a guide through the main principles of networking, did not use it heavily at all and made sure to not get the exact piece of information im looking for from AI
