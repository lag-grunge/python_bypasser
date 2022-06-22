FROM python:3.8-buster

RUN apt-get update && apt-get autoclean && apt-get -y install libxss1 libu2f-udev libvulkan1  \
    && wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i /tmp/google-chrome-stable_current_amd64.deb; apt-get -y -f install

WORKDIR  /usr/src/app
COPY . .
RUN mv -v ./dep/requirements.txt /tmp/requirements.txt && pip install --no-cache-dir -r /tmp/requirements.txt && python ./tools/install_driver.py \
    && mv -v ./dep/fake_useragent_0.1.11.json /tmp/fake_useragent_0.1.11.json

ENV headless 1
CMD ["python", "./src/main_bigjpg_parser.py"]

