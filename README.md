# userrecon-py
Username recognition on various websites.

[![powered by](https://img.shields.io/badge/powered%20by-WhatsMyName-black.svg?style=flat&logo=github)](https://github.com/WebBreacher/WhatsMyName)
[![demo](https://img.shields.io/badge/asciinema-demo-red.svg?style=flat)](https://asciinema.org/a/272560)
![websites](https://img.shields.io/badge/websites-193-green.svg?style=flat)
[![donate](https://img.shields.io/badge/paypal-donate-blue.svg?style=flat&logo=paypal)](https://paypal.me/decoxviii)

---

## Installation

#### With `pip3`
```bash
# Linux
sudo -H pip3 install git+https://github.com/decoxviii/userrecon-py.git --upgrade
userrecon-py --help
```

#### Build from source
```bash
# Linux
git clone https://github.com/decoxviii/userrecon-py.git ; cd userrecon-py
sudo -H pip3 install -r requirements.txt
python3 setup.py build
sudo python3 setup.py install
```
---

## Usage
Start by printing the available actions by running `userrecon-py --help`. Then you can perform the following tests:
```bash
# print all results.
userrecon-py target decoxviii --all -o test


# print positive results.
userrecon-py target decoxviii --positive -o test


# print negative results.
userrecon-py target decoxviii --negative  -o test
```

---

**decoxviii**

**[MIT](https://github.com/decoxviii/userrecon-py/blob/master/LICENSE)**



