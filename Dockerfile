FROM python:3.13-slim
LABEL org.opencontainers.image.source=https://github.com/path-coverage/schemas

RUN pip install --no-cache-dir --root-user-action=ignore jsonschema==4.26.0

COPY validate.py path_coverage.schema.json path_coverage.source.schema.json /schemas/
COPY samples /schemas/samples

ENTRYPOINT ["python", "/schemas/validate.py"]
