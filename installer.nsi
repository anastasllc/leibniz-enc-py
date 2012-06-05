# define name of installer
outFile "LeibnizEncryption.exe"
 
# define installation directory
installDir "$PROGRAMFILES\Leibniz Encryption"
 
# start default section
section
	setOutPath $INSTDIR

 	file "leibnizwx.exe"
	file "cyphers.txt"
	file "gear.txt"

	createShortCut "$DESKTOP\Leibniz Encryption.lnk" "$INSTDIR\leibnizwx.exe"
sectionEnd