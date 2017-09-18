# Sites Monitoring Utility

Check sites for respond 200 and domain expiration time is less then month (expiration check is not passed in this situation)

# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

# How it work

```bash
python check_sites_health.py
```
```bash
Filepath to file with urls
```

# Output

```bash
http://ning.com Respond is 200 Expiration check passed
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
