# virtualenvwrapper_ctf

Virtualenvwrapper plugin to automate environment setup for participating in CTF competitions and related challenges.


## Installation

You can install the library through pip:
```
pip3 install .
```


Make sure `virtualenvwrapper` is installed and `$PROJECT_HOME` is set to your CTF directory.  This can be done in `~/.bashrc`:
```bash
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'
source /usr/local/bin/virtualenvwrapper.sh

export PROJECT_HOME=~/ctf
```


The `$PROJECT_HOME` directory should have an associated virtualenv, as this will be added to a new CTF's virtualenv.
```bash
~/ctf$ mkvirtualenv ctf
(ctf) ~/ctf$ pip3 install pwntools angr
```

Optionally you can create a `.misc` directory and a `.template` directory.  These will be used to copy default files for CTFs.
The files in `.misc` will be copied to each challenge. These could possibly debuggers or note templates.
Files in `.template` will be copied to a new CTF's root folder and each new challenge will copy a CTF's instances.  This is performed so you can customize a template script (and flag format) per CTF.


To set all new bash instances to start working on the "active" CTF, add this to your `~/.bashrc`:
```bash
if [ ! -z "$PROJECT_HOME" ]
then
    if [ -s "$PROJECT_HOME/.active_ctf" ]
    then
        workon `cat $PROJECT_HOME/.active_ctf`
    fi
fi
```
This will use the `.active_ctf` file in `$PROJECT_HOME` containing the name of the CTF.

If you wish to disable this after the CTF, run `endctf` which will simply delete the `.active_ctf` file.

## Example

Start a new ctf:
```bash
vctf init pwnable.kr
workon pwnable.kr
```

Start a new challenge while within the virtualenv, use `addchallenge [category] [challenge name]`:
```bash
(pwnable.kr) ~/ctf/pwnable.kr$ vctf add toddlers bof
(pwnable.kr) ~/ctf/pwnable.kr$ cd toddlers/bof/
(pwnable.kr) ~/ctf/pwnable.kr/toddlers/bof$ ls
flag  flag.txt  template.py
```
