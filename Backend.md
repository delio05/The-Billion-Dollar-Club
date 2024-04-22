# Backend Guide

## Install Python dependencies

1. Install python>=3.10, 3.11.2 is the recommanded version.
2. Run the command `make setup`.

## SETUP Environment Variable

1. Create `.env` file under the **The-Billion-Dollar-Club** directory.
2. Write in `OPENAI_API_KEY=***` (replace `***` by your api key).
3. Write in `GOOGLE_API_KEY=***` (like above).
4. Write in `PYTHON_CMD=python3.*` (replace `*` by your installed python version).
5. Write in `PIP_CMD=pip3.*` (replace `*` by your installed python version).
6. Write in `FEEDBACK_FILE_DIR=***/***` (replace `***/***` by the path to your preferred file to store feedback).

## How to Start Server

Stay in the **THE-BILLION-DOLLAR-CLUB**. Run the command `make runserver`. Quit the server by `CONTROL-C`.
