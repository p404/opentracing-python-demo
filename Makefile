start:
	docker-compose -f ./jaeger-elasticsearch-compose/docker-compose.yml up -d 
	docker-compose build
	docker-compose up

clean:
	docker-compose down -v
	docker-compose -f ./jaeger-elasticsearch-compose/docker-compose.yml down -v
