
include .env
export

.PHONY: runserver setup

setup: requirements.txt
	$(PYTHON_CMD) -m pip install -r requirements.txt

runserver: MyChartExtension/manage.py
	$(PYTHON_CMD) MyChartExtension/manage.py runserver --noreload &> web_server.log &

clean:
	killall Python
