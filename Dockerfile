FROM continuumio/anaconda3
LABEL authors="Jon Riege"

EXPOSE 8000

WORKDIR /app

COPY environment.yaml environment.yaml

RUN conda env create -f environment.yaml

COPY . .

CMD ["conda", "run", "-n", "house-price-model-env", "gunicorn", "-b", "0.0.0.0:8000", "app.run:app"]
