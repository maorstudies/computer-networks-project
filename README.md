# computer-networks-project
Computer Networks final project: DNS/TCP traffic analysis with Wireshark and Python client-server application.

## Project Structure

### Part 1 - DNS/TCP Traffic Analysis (Wireshark + Jupyter)
- group01_dns_input.csv - DNS messages input file
- raw_tcp_ip_notebook_fallback_annotated_v1.ipynb - Jupyter notebook for packet creation and analysis
- group01_dns_capture.pcap - Wireshark capture of generated DNS/TCP traffic

### Part 2 - TCP Client-Server Chat Application
- server.py - TCP chat server
- client.py - TCP chat client
- part2_chat_tcp_capture.pcap - Wireshark capture of chat application traffic

### Report
- Final_project_report.pdf

## How to Run
Start the server:
python server.py

Then open a separate terminal for each user:
python client.py

Enter a username, then type another user's name to start chatting.
Use @username to send to someone specific, /change to switch.
