# autoarch

# Desktop

## Disposition des écrans:
.config/cinnamon-monitors.xml

## Configuration de la bar des tâches
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


