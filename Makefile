include .env
export

.PHONY: runserver setup

setup: requirements.txt
	$(PYTHON_CMD) -m pip install -r requirements.txt
	$(PYTHON_CMD) -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. grpc/feedback.proto
	$(PYTHON_CMD) -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. grpc/interpretation.proto

runserver: MyChartExtension/manage.py
	$(PYTHON_CMD) MyChartExtension/manage.py runserver > web_server.log &
	$(PYTHON_CMD) Workers/grpc/interpret.py 1 > interpretation.log &
	$(PYTHON_CMD) Workers/grpc/feedback.py 1 > feedback.log &

clean:
	killall $(PYTHON_CMD)