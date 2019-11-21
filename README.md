# CEC-python-GUI
The Raspberry Pi 3 has a HDMI CEC on the Tx output, this cec gui allows us to send cec commands to the TV.
To run this program, you need to install pyside. from linux terminal run the install as shown below

Install the following packets
  - sudo apt-get update
  - sudo apt-get install python-pyside
  - sudo apt install cec-utils
  
Run the cec python gui
  - python raspberry_cec
  - from the CEC Demo Gui
    - Set Initiator: AudioSYSTEM
    - Set Follower : TV 
    - Set Opcode   : Standby
      - Your TV should go to standby
 
 Have fun and enjoy.
