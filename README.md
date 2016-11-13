# PokemonGo Map
### A Pokémon Map Service which shows real-time info of nearby catchable Pokémons

- Front-end: Html/Javascript/CSS/Bing Map, Hosted by Github Pages
- Back-end: Python, Django/Docker/Postgresql/Redis/Google S2, Hosted by AWS services: Elastic BeanStalk, RDS, SQS
- Front and Back end Connected through API Gateway
- Mock crawling apis used only due to legal issues


### Back-end architecture
- Two clusters of servers, one cluster for handling requests, the other for crawling data
- Two clusters communicate through message queue(AWS SQS)
- Web-server cluster receives requests, query Redis and Postgresql database for currently catchable pokemons of this area, whcich have already been crawled and put the requests into the message queue
- Crawler-server cluster get requests from the message queue, do crawling, store crawled data into database and delete expired data periodically
- Redis is used for deduplication of repeated query: Web-server breaks the requested area to cells using Google S2 and check if the requested cell has already requested several seconds ago, if yes, no need to crawl again



