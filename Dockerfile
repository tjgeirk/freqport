FROM freqtradeorg/freqtrade:latest
RUN pip install ta && freqtrade install-ui && freqtrade webserver
