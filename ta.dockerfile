FROM freqtradeorg/freqtrade:latest
RUN pip install pip -U && pip install ta
RUN sh /freqtrade/strategies/.pull
