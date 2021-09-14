python=python

all:
	-$(python) ioliu.py 170
	-$(python) json2sh.py
	-bash bing.sh
	-$(python) rmsame.py
	-$(python) bing.py

.PHONY: install format test clean

install:
	-sudo apt install -y curl
	-curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
	-$(python) /tmp/get-pip.py
	-$(python) -m pip install -U -r requirements.txt

format:
	@-find $^ -regex '.*\.\(cpp\|hpp\|cu\|c\|h\)' -exec clang-format --verbose -style=file -i {} \;
	@-black --pyi -S $(shell find $^ -regex '.*\.\(py\)')

test:
	-kill -9 `pgrep -f bing.py`
	-$(python) bing.py

clean:
	-git clean -dfX
