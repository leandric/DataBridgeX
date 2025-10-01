# ================================
# Makefile para gerenciamento do Apache Airflow com Docker
# ================================

IMAGE_NAME=databridgex/apache-airflow
TAG=latest

.PHONY: build push up down all airflow-standalone \
        mysql-up mysql-down mysql-logs mysql-bash mysql-restart mysql-cli

export AIRFLOW_HOME := $(HOME)/Documents/airflow

# ---------------- Airflow ----------------

airflow-standalone:
	airflow standalone

# Constrói a imagem Docker
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Faz o push da imagem para o Docker Hub
push: build
	docker push $(IMAGE_NAME):$(TAG)

# Sobe os containers com docker-compose
up:
	docker compose up -d

down:
	docker compose down

# Executa tudo: build, push e up
all: push up

# ---------------- MySQL ----------------

MYSQL_IMAGE=mysql:8.0
MYSQL_CONTAINER=mysql-container
MYSQL_ENV_FILE=.env
MYSQL_PORT=3306
MYSQL_VOLUME=mysql_data

# Sobe o MySQL com variáveis do .env
mysql-up:
	docker run -d --name $(MYSQL_CONTAINER) \
		--env-file $(MYSQL_ENV_FILE) \
		-p $(MYSQL_PORT):3306 \
		-v $(MYSQL_VOLUME):/var/lib/mysql \
		$(MYSQL_IMAGE)

# Para e remove o container e volume
mysql-down:
	docker stop $(MYSQL_CONTAINER) || true
	docker rm $(MYSQL_CONTAINER) || true
	docker volume rm $(MYSQL_VOLUME) || true

# Logs do MySQL
mysql-logs:
	docker logs -f $(MYSQL_CONTAINER)

# Acessa o bash do container
mysql-bash:
	docker exec -it $(MYSQL_CONTAINER) bash

# Reinicia o MySQL
mysql-restart: mysql-down mysql-up

# Conecta no MySQL usando variáveis do .env
mysql-cli:
	docker exec -it $(MYSQL_CONTAINER) \
		mysql -u$$(grep MYSQL_USER $(MYSQL_ENV_FILE) | cut -d '=' -f2) \
		      -p$$(grep MYSQL_PASSWORD $(MYSQL_ENV_FILE) | cut -d '=' -f2) \
		      $$(grep MYSQL_DATABASE $(MYSQL_ENV_FILE) | cut -d '=' -f2)
