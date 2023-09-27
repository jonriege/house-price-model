FROM continuumio/anaconda3
LABEL authors="Jon Riege"

ENV PORT 8080
EXPOSE 8080

WORKDIR /app

COPY environment.yaml environment.yaml

RUN conda env create -f environment.yaml

COPY . .

CMD ["conda", "run", "-n", "house-price-model-env", "gunicorn", "-b", "0.0.0.0:8080", "app.run:app"]
