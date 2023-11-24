# autoarch

crontab:   
  - permet de conserver les dconf à restaurer  
    - Raccourci clavier pour gérer les fenêtres sans barre titre, barre cinnamon  
  - permet de conserver les crontab à restaurer
kopia: backup des données non gitable sur S3. (dossier .config, .local, .ssh, dconf, crontab, etc...)

run_autoarch.sh: exemple de commande à rouler pour lancer l'installation avec certains préalables 
  - install_os.py: installe les paquets systèmes pour tous les utilisateurs
  - user.py: installe les configs conservées sur S3 par Kopia et autres configs utilisateur

#TODO avant user.py

-- ajouter dans installation
pacman -S --needed base-devel openssl zlib xz tk

-- forcer la création de dossier parent
ERROR error restoring: restore error: error copying: copy file: error creating file: open /home/pylan1/.config/variety/variety.conf: no such file or directory

-- backuper et restaurer dossier powerlevel10k
/home/pylan1/.zshrc:source:73: aucun fichier ou dossier de ce type: /home/pylan1/powerlevel10k/powerlevel10k.zsh-theme

-- vpn ul pas là
backuper restaurer /etc/NetworkManager/system-connections
chmod 600 /etc/NetworkManager/system-connections/output.nmconnection
chown root:root /etc/NetworkManager/system-connections/output.nmconnection

-- application au démarrage:
copier .config/autostart

-- installer discord postman lingot pavucontrol 
yay discord postman-bin lingot pavucontrol-qt 
note: lingot: compilation courte

-- install minikube kubectl kubectx cmctl kubeflow-kfctl-bin 

# Desktop

## Disposition des écrans:
.config/cinnamon-monitors.xml

## Configuration de la barre des tâches
.config/cinnamon/spices/*
.local/cinnamon/*
.local/locale/*
dconf modifié

## Configuration du navigateur de fichier
dconf modifié

## Thème Adapta-Nokto
dconf modifié
.local/share/themes/Adapta-Nokto

## Suppression de la barre titre des application
copier .config_gtk-3.0_gtk.css dans le bon dossier et voilà!

## Raccourci clavier
copier ~/bin
copier ~/.xsession
dconf modifié

## Le keyring
.local/share/keyrings
.pki

## TODO
dans /etc/security/faillock.conf
deny = 0 

fs.inotify.max_user_watches = 524288  
/etc/sysctl.d/jetbrains  
https://youtrack.jetbrains.com/issue/IDEA-126491
https://gist.github.com/ntamvl/7c41acee650d376863fd940b99da836f  

fstab:
//ul.ca/Dti/Projets/P395-PULSAR
smb://pylan1@ul.ca/dti/projets/P447-Valeria

# yay multicore
There is a variable in /etc/makepkg.conf which does exactly that for every package: MAKEFLAGS="-j4"
https://www.reddit.com/r/archlinux/comments/494c84/comment/d0owvy4/?utm_source=share&utm_medium=web2x&context=3

### pour accéder au tty platformio / arduino...
sudo usermod -a -G uucp $USER


# poetry kde wallet
https://stackoverflow.com/questions/64570510/why-does-pip3-want-to-create-a-kdewallet-after-installing-updating-packages-on-u
python3 -m keyring --disable

# crontab example
```
# Sauvegarde de dconf
*/15 * * * * dconf dump / > $HOME/.config/dconf/dconf.ini
*/15 * * * * crontab -l > $HOME/.config/crontab/crontab
```
