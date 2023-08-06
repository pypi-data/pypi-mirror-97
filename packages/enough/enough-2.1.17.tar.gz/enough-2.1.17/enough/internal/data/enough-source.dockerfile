ARG IMAGE_NAME
FROM ${IMAGE_NAME}

COPY Pipfile Pipfile.lock /tmp/
RUN . /opt/venv/bin/activate ; cd /tmp ; PIPENV_VERBOSITY=-1 pipenv install --ignore-pipfile

COPY dist/* .
RUN pip3 install *.tar.gz

RUN python -m enough.internal.cmd install api/data/enough.service > /etc/systemd/system/enough.service && systemctl enable enough

CMD [ "help" ]
ENTRYPOINT [ "python", "-m", "enough.internal.cmd" ]
