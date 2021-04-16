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

Optionally create a `.misc` directory and a `.template` directory.  These will be used as default files for CTFs.  Files in `.misc` will be copied to each challenge, possibly debuggers or note templates. Files in `.template` will be copied to a new CTF's root folder and each new challenge will copy that instance.  This is performed so you can customize a template script (and flag format) per CTF.

Start a new ctf:
```bash
vctf --init pwnable.kr
workon pwnable.kr
```

Start a new challenge while within the virtualenv, use `addchallenge [category] [challenge name]`:
```bash
(pwnable.kr) ~/ctf/pwnable.kr$ vctf --add toddlers bof
(pwnable.kr) ~/ctf/pwnable.kr$ cd toddlers/bof/
(pwnable.kr) ~/ctf/pwnable.kr/toddlers/bof$ ls
flag  flag.txt  template.py
```

To allow all new bash instances to start working on the "active" CTF, add this to your `~/.bashrc`:
```bash
source /usr/local/bin/active_ctf.sh
```
This will add a `.active_ctf` file in `$PROJECT_HOME` containing the name of the CTF.

If you wish to disable this after the CTF, run `endctf` which will simply delete the `.active_ctf` file.
