FROM python:3.13-slim
LABEL org.opencontainers.image.source=https://github.com/path-coverage/schemas

RUN pip install --no-cache-dir --root-user-action=ignore jsonschema==4.26.0

COPY validate.py /schemas/
COPY v1 /schemas/v1
COPY v2 /schemas/v2
COPY v3 /schemas/v3

ENTRYPOINT ["python", "/schemas/validate.py"]
