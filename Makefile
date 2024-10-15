build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose pull
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose build

deploy:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose up

cleanup:
	docker compose down
	docker compose --file docker-compose-testing.yaml --project-name ayomi-tests down

PYTEST_ARGS ?= -c tests/pytest.ini

exec-tests:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose --file docker-compose-testing.yaml --project-name ayomi-tests build

	docker compose --file docker-compose-testing.yaml --project-name ayomi-tests run --rm server /docker-entrypoint.sh pytest $(PYTEST_ARGS) /src-volume/$(filter-out $@, $(MAKECMDGOALS)); \
