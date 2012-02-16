all: data.json

caniuse-data.json:
	wget -N https://github.com/Fyrd/caniuse/raw/master/data.json -O $@

mobilehtml5-data.json:
	wget http://mobilehtml5.org/ -O mobilehtml5.html
	@tidy --show-errors 0 --force-output yes -m -n -asxml -q mobilehtml5.html || echo "ignoring tidy errors"
	xsltproc extract-mobilehtml5-data.xsl mobilehtml5.html |json_xs > $@
	rm mobilehtml5.html

data.json: caniuse-data.json mobilehtml5-data.json local-data.json merge-data.py
	python merge-data.py | json_xs> $@