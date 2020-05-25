# virtualenvwrapper_ctf

Virtualenvwrapper plugin to automate environment setup for participating in CTF competitions and related challenges.

## Installation

```
sudo pip3 install .
```

## Example

Make sure `virtualenvwrapper` is installed and `$PROJECT_HOME` is set to your CTF directory.  This can be done in `~/.bashrc`.

The `$PROJECT_HOME` directory should have an associated virtualenv, as this will be added to a new CTF's virtualenv.

```bash
~$ cd ctf
~/ctf$ mkvirtualenv ctf
(ctf) ~/ctf$ pip install pwntools angr
```

Optionally create a `.debug` directory and a `.template` directory.  These will be used as default files for CTFs.  Files in `.debug` will be copied to each challenge. Files in `.template` will be copied to a new CTF's root folder and each new challenge will copy that instance.

Start a new ctf:
```bash
startctf pwnable.kr
workon pwnable.kr
```

Start a new challenge while within the virtualenv, use `addchallenge [category] [challenge name]`:
```bash
(pwnable.kr) ~/ctf/pwnable.kr$ addchallenge toddlers bof
(pwnable.kr) ~/ctf/pwnable.kr$ cd toddlers/bof/
(pwnable.kr) ~/ctf/pwnable.kr/toddlers/bof$ ls
flag  flag.txt  template.py
```

Another feature is to allow all new bash instances to start working on the "active" CTF.  This can be done by adding this to your `~/.bashrc`:
```bash
source /usr/local/bin/active_ctf.sh
```

If you wish to disable this after the CTF, feel free to delete/edit `$PROJECT_HOME/.active_ctf`.  A script will be added in the future to do this.
