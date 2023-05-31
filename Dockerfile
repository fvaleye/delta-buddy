FROM python:3.11-buster

# Prerequisites
RUN rm -rf /var/lib/apt/lists/* & apt-get -y update && apt-get -y --no-install-recommends install python3 python3-pip

# Python
RUN pip install --upgrade pip

COPY . ./delta-buddy
WORKDIR ./delta-buddy

# Install tracarbon
RUN pip install -r requirements.txt

# Run tracarbon
ENTRYPOINT ["PYTHONPATH=.", "chainlit", "run", "app/chainlit_main.py"]