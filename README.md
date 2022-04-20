# autoarch

```
wget -O /tmp/autoarch.sh https://raw.githubusercontent.com/pylanglois/autoarch/main/autoarch.sh
```

```
sudo pacman -S git
```

```
git clone ssh://git@github.com/pylanglois/autoarch
venv autoarch
pip install plumbum
PYTHONPATH=$PWD python autoarch/customize.py
```

ssh permissions
```
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*
chmod 644 ~/.ssh/*.pub
```

kopia: restaurer le dossier ~/.config/kopia


## TODO

fs.inotify.max_user_watches = 524288  
/etc/sysctl.d/jetbrains  
https://youtrack.jetbrains.com/issue/IDEA-126491  
https://gist.github.com/ntamvl/7c41acee650d376863fd940b99da836f  


