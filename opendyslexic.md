# ajout à la liste des paquets
apt install fonts-opendyslexic

# fixe les fichiers manquants
wget -O /tmp/opendys.zip https://github.com/antijingoist/opendyslexic/releases/download/v0.91.12/opendyslexic-0.910.12-rc2-2019.10.17.zip
unzip -o opendys.zip -d /usr/share/fonts/woff/opendyslexic/
