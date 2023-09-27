FROM continuumio/anaconda3
LABEL authors="Jon Riege"

ENV PORT 8080
EXPOSE 8080

WORKDIR /app

COPY environment.yaml environment.yaml

RUN conda env create -f environment.yaml

COPY . .

CMD ["conda", "run", "-n", "house-price-model-env", "gunicorn", "--access-logfile", "'-'", "--error-logfile", "'-'", "app.run:app"]
