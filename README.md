# Запуск

``` bash
curl -O https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ru.300.bin.gz && gunzip cc.ru.300.bin.gz && mv cc.ru.300.bin ./server/models/

docker compose build
docker compose up
```

Клиент будет доступен на 3000 порту