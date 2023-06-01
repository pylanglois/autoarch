# autoarch

crontab:   
  - permet de conserver les dconf à restaurer  
    - Raccourci clavier pour gérer les fenêtres sans barre titre, barre cinnamon  
  - permet de conserver les crontab à restaurer
kopia: backup des données non gitable sur S3. (dossier .config, .local, .ssh, dconf, crontab, etc...)

run_autoarch.sh: exemple de commande à rouler pour lancer l'installation avec certains préalables 
  - install_os.py: installe les paquets systèmes pour tous les utilisateurs
  - user.py: installe les configs conservées sur S3 par Kopia et autres configs utilisateur

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