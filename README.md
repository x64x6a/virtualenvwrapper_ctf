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

## Examples

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

### CTF Platform Support

There is also integration with some CTF scoreboard platforms to automatically download challenges as well as making a directory structure.

Example with local CTFd instance:
```bash
$ vctf init local -u test -p test -d http://127.0.0.1:4000 -f ctfd
...

$ vctf list
   id   category           name  value  solves  solved_by_me
0   2        pwn      Exploit I    100       1          True
1   3  reversing    Reversing I    100       0         False
2   1       misc    Challenge I    200       1          True
3   4  reversing   Reversing II    200       0         False
4   6        pwn     Exploit II    200       0         False
5   5  reversing  Reversing III    300       0         False

$ vctf pull
Challenge: pwn - Exploit_I (2): ~/ctf/local/pwn/Exploit_I
 [+] Added file for challenge 2 '~/ctf/local/pwn/Exploit_I/exploit_i'
Challenge: reversing - Reversing_I (3): ~/ctf/local/reversing/Reversing_I
 [+] Added file for challenge 3 '~/ctf/local/reversing/Reversing_I/crackme'
Challenge: misc - Challenge_I (1): ~/ctf/local/misc/Challenge_I
 [+] Added file for challenge 1 '~/ctf/local/misc/Challenge_I/misc_i'
Challenge: reversing - Reversing_II (4): ~/ctf/local/reversing/Reversing_II
 [+] Added file for challenge 4 '~/ctf/local/reversing/Reversing_II/crackme_ii'
Challenge: pwn - Exploit_II (6): ~/ctf/local/pwn/Exploit_II
 [+] Added file for challenge 6 '~/ctf/local/pwn/Exploit_II/exploit_ii'
Challenge: reversing - Reversing_III (5): ~/ctf/local/reversing/Reversing_III
 [+] Added file for challenge 5 '~/ctf/local/reversing/Reversing_III/crackme_iii'

$ ls ~/ctf/local/
flag  flag.txt  misc  pwn  reversing  solve.py

$ ls ~/ctf/local/pwn/Exploit_II/
exploit_ii  flag  flag.txt  notes.md  solve.py

$ vctf submit 6 "FLAG{some_flag}"
Correct

$ vctf list
   id   category           name  value  solves  solved_by_me
0   2        pwn      Exploit I    100       1          True
1   3  reversing    Reversing I    100       0         False
2   1       misc    Challenge I    200       1          True
3   4  reversing   Reversing II    200       0         False
4   6        pwn     Exploit II    200       1          True
5   5  reversing  Reversing III    300       0         False
```
