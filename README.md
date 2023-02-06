## SHOPEE COIN SCRIPT

Script referenced from: https://github.com/arffsaad/shopeeautocoin
Modified the script to work with SG.

### To-do
- Setup and run fully headless. GUI environment required on first login due to CAPTCHA.
- Login multiple users from same script with persistence. Run script with flags to determine which user to login?
- Validation if login details are wrong.

### Pre-requisites
- Python 3.8 or greater (tested on 3.10, but playwright should work fine at 3.8)
- `pip install pytest-playwright`
- `playwright install`
- `playwright install-deps` may need to run this too if it's on a server.

### Usage
- Clone Repository
- Create an empty folder called "persistence" in the cloned repo.
- Run autocoin.py with `python autocoin.py` it will launch the first login routine. Follow the prompts to authorize 2FA, and store your session persistently.
- After completing the steps, schedule the script to run once every day.
  - Windows
    - Open Task scheduler, and create new task.
    - Execute a program > set path as path to python executable.
    - Set parameters as path to autocoin.py
    - Set frequency as repeat daily, select a time where your PC/Laptop will be running.
  - Linux/MacOS
    - Add an entry in crontab with `crontab -e`
    - `0 8 * * * /path/to/python3 /path/to/autocoin.py # example, will run the script at 8AM every day`
    - https://crontab.guru/

- Optional: copy entire folder (with persistence and credentials.txt) to a headless server with SCP (or other tools like Filezilla, winSCP).
- `scp -r shopeeautocoin user@<ip-of-server>:/home/user/`

- If you installed the pre-requisites in a Python virtual environment, write a shell script to activate it.
`#!/bin/bash
source /home/user/pathToVenv/.venv/bin/activate
python /home/user/pathToRepo/shopeeautocoin/autocoin.py`

Open an issue if you are having any issues/questions, pull request welcomed:)
