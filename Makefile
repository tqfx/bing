python=python

run:
	-kill -9 `pgrep -f bing.py`
	nohup $(python) bing.py > /dev/null 2>&1 &

test:
	-kill -9 `pgrep -f bing.py`
	-$(python) bing.py

all:
	-$(python) ioliu.py
	-$(python) json_to_sh.py
	-bash bing.sh
	-$(python) rm.py
	-$(python) bing.py

install:
	-curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	-$(python) get-pip.py
	-$(python) -m pip install -U pip requests bs4

clean:
	-rm -rf bing.sh bing.json run.sh img
