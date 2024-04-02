include .env
export

.PHONY: runserver
runserver: MyChartExtension/manage.py
	$(PYTHON_CMD) MyChartExtension/manage.py runserver