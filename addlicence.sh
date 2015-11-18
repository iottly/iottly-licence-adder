#py
./addheader.py apache2.py.tmpl ../ -fre '.*\.py$'

#js
./addheader.py apache2.js.tmpl ../ -fre '.*\.js$' -dre '^((?!vendor).)*$'

#html
./addheader.py apache2.html.tmpl ../ -fre '.*\.html$' -dre '^((?!iottly-xmpp-broker).)*$'

#java
./addheader.py apache2.java.tmpl ../ -fre '.*\.java$'

#docker compose
./addheader.py apache2.docker.tmpl ../ -fre '.*\.yml'

#docker files
./addheader.py apache2.docker.tmpl ../ -fre '.*Dockerfile$'
