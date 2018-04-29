# Anbi Recognizer

I sometimes forget to which good causes I've donated, that's why I made a simple tool in which you
can try to analyze your transactions for donations that are tax deductible.

Not all donations are recognized. For instance, it fails to recognize my WikiMedia Foundation donation.

# Running

```
sudo apt-get install python3-tabulate
chmod +x anbi_recognizer.py
./anbi_recognizer.py [your_csv]
```

or for non-Debian based distros:

```
pip3 install -r requirements.txt
chmod +x anbi_recognizer.py
./anbi_recognizer.py [your_csv]
```
