COMPOSE = docker compose -f env/docker-compose.yml

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

ps:
	docker ps

reset:
	$(COMPOSE) down -v

# -------------------------
# DB COMMANDS
# -------------------------

db-shell:
	docker exec -it ops-postgres psql -U admin

load-schema:
	docker exec -i ops-postgres psql -U admin -d postgres < sql/generated_schema.sql

load-data:
	docker exec -i ops-postgres psql -U admin -d postgres < sql/load.sql

# -------------------------
# BACKUP
# -------------------------

backup:
	mkdir -p backup

	docker exec ops-postgres pg_dump -U admin -d postgres > backup/db.sql

# -------------------------
# RESTORE
# -------------------------

restore:
	cat backup/db.sql | docker exec -i ops-postgres psql -U admin -d postgres