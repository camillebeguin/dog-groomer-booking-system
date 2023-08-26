.ONESHELL:

CONTAINER_EXECUTOR = docker exec -w /wl/app booking-api

# Deployment
.PHONY: up
up:
	 docker compose -f ./docker-compose.yml up -d
.PHONY: down
down:
	 docker compose -f ./docker-compose.yml down -v

.PHONY: build
build:
	docker compose -f docker-compose.yml build

.PHONY: downgrade-db
downgrade-db:
	$(CONTAINER_EXECUTOR) alembic downgrade -1

.PHONY: migrate-db
migrate-db:
	$(CONTAINER_EXECUTOR) alembic upgrade head

.PHONY: autogenerate-migration
autogenerate-migration:
	$(CONTAINER_EXECUTOR) alembic revision --autogenerate -m $(revision_message)