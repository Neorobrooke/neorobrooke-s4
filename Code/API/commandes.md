# Calibration
cable moteur1:705 moteur4:770
pos
# Déplacement au centre du cadre
go 600:-500:0
pos
# Déplacement en direction x positif
dep x
stop
# Déplacement en diagonal (x et y négatifs)
dep -x-y
# Changement de direction
dep y
stop
clear
# Déplacement dans un coin
go 300:-900:0
pos
# Phénomène de changement de direction du moteur 1
go 900:-500:0
pos
# Autres commandes: voir la position des poteaux
ls
ls moteur1
ls :1
# Autres commandes: aide et documentation des commandes
help
help go
# Remonter les erreurs
dep x
stop
err
clear
# Autres fonctionnalités: appels systèmes
!ls -la
exit