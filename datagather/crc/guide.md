# How to run wiki datagather script on Pitt CRC, transferring data to some computer

CRC doesn't have enough storage for this dataset, I want the data locally for future use, and I'm concerned about my CRC session timing out or getting disconnected. So my solution, which isn't necessarily great but should do what I need it to, is this: 1. Use my laptop to connect to CRC. 2. CRC runs the script and makes the dataset. 3. Borrow my mom's old laptop and have CRC periodically send data to it. Why I need two laptops? Because I don't want my laptop slowed down from heavy file transfers when I'm in classes, trying to do homework, running other code, etc all day and because I need to be on Pitt's VPN to access CRC, and transferring data automatically from CRC to my laptop while my laptop is on a VPN turns out to be a real pain (yes, worse than from the configuration I've settled on).

So here's how to set it all up:
1. To access CRC (when not on campus), you need to be on Pitt's VPN. But, your secondary storage device is on your home wifi. So, you need some address that's accessible from anywhere in the world for you to be able to `ssh`, `sftp`, etc to your computer. The ngrok tool achieves this.
  1. On Mac system preferences, make sure Remote Login in sharing menu is enabled
  1. Install ngrok (look up online)
  2. Create account on ngrok website, sign in locally on storage computer's commandline following instructions on ngrok website
  3. The command `./ngrok tcp 22` creates a forwarding address from an ngrok address to your own computer's port 22. Run this command and just leave it sit.
  4. On the info page that pops up, get hostname, port number and username.
2. On CRC, enter smp module
  1. Run `crc-interactive.py --smp --time=12 --num-cores=16`
  2. Get python 3 `module load python/3.7.0`
  3. Get python 2 `module load python/anaconda2.7-4.2.0`
  4. Get all the libraries installed via `pip install --user {wikipedia, rapidjson-python, paramiko, wikiextractor, etc}`. I know it's silly I'm using both python 2 and 3, but at least this way you don't need to touch my fork of WikiExtractor!
3. Plug the right info into  `paramiko-tuto.py` or the other script, eg <br>
   `python3 get-data-wiki.py <address> <port> <username> 'Documents/wikidata' 1` and off you go!

Or you can also run everything locally on one computer, which is accomplished by the script `get-data-wiki.py` that's not in this CRC directory.
