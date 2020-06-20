FROM continuumio/anaconda3:4.4.0

RUN pip install --upgrade pip && \
    pip install janome==0.3.10

RUN python -m nltk.downloader book

WORKDIR /workdir
RUN git clone https://github.com/mack-the-psych/plimac3.git

RUN echo "/workdir/plimac3/Lib" > /opt/conda/lib/python3.6/site-packages/plimac-custom.pth
RUN echo "/workdir/plimac3/Tools" >> /opt/conda/lib/python3.6/site-packages/plimac-custom.pth

WORKDIR /workdir/plimac3/Resource/OANC
RUN python compile_shelve.py

WORKDIR /workdir/plimac3/Resource/BCCWJ_frequencylist_suw_ver1_0
RUN python compile_shelve.py

WORKDIR /workdir
