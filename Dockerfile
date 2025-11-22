FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt \
    && pip install --prefix=/install torch==2.2.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

EXPOSE 8000
CMD ["gunicorn", "monprojet.wsgi", "--bind", "0.0.0.0:8000"]
