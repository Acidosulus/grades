
	Знает что такое pod, namespase, ingress, контролеры. Умеет читать логи OpenShift (Kibana), мониторинг
	Наблюдение в практической деятельности + Интервью (при необходимости рассказывает и раскрывает концепцию)

### В контексте Kubernetes/OpenShift:

#### 1. **Pod**

Под – это минимальная и базовая единица развертывания в Kubernetes, которая представляет собой один или несколько контейнеров (чаще всего один) с общими ресурсами:

- **Общая сеть:** контейнеры внутри одного пода могут общаться между собой через `localhost`.
- **Общее хранилище:** могут совместно использовать монтируемые тома.
- **Назначение:** Поды обычно представляют одно приложение или компонент, который должен запускаться на определенном узле кластера.

**Примеры использования:**

- Веб-сервер с логическим контейнером для логов.
- Микросервис, работающий на основе одного контейнера.

#### 2. **Namespace**

Пространство имен Kubernetes разделяет ресурсы кластера на логические группы. Это помогает организовывать и изолировать рабочие нагрузки.

**Особенности и преимущества:**

- Позволяет запускать несколько приложений или сред (например, dev/stage/prod) в одном кластере без конфликтов.
- Разделяет доступ для пользователей и сервисов.
- Каждый namespace имеет свои поды, службы, конфигурации и другие ресурсы.

**Типичные примеры:**

- `kube-system` для системных компонентов Kubernetes.
- `default` для ресурсов по умолчанию.
- `custom-namespace` для пользовательских приложений.

#### 3. **Ingress**

Ingress управляет внешним доступом к сервисам внутри кластера через HTTP и HTTPS, предоставляя правила маршрутизации для входящего трафика.

**Основные функции:**

- Маршрутизация запросов на основе пути URL или имени хоста.
- Поддержка SSL/TLS для шифрования трафика.
- Балансировка нагрузки.

**Пример:**

- Запросы на `app.example.com/api` перенаправляются в сервис `backend`, а запросы на `app.example.com/frontend` – в сервис `frontend`.

#### 4. **Контроллеры**

Контроллеры в Kubernetes автоматизируют управление состоянием приложений и ресурсов, следят за тем, чтобы текущий статус соответствовал желаемому.

**Популярные контроллеры:**

- **Deployment Controller:** управляет развертыванием подов и поддерживает желаемое количество реплик.
- **ReplicaSet:** гарантирует, что запущено указанное количество подов.
- **StatefulSet:** используется для приложений, требующих устойчивой идентификации подов и стабильного хранилища (например, базы данных).
- **DaemonSet:** гарантирует, что на каждом узле в кластере будет запущен один экземпляр пода (например, лог-сборщики).
- **Job/CronJob:** управление одноразовыми или периодическими заданиями.

#### **Общий поток работы:**

1. Создание ресурсов через манифесты (YAML).
2. Kubernetes применяет манифесты и следит за состоянием через контроллеры.
3. Поды запускаются внутри заданных пространств имен и взаимодействуют с внешним миром через Ingress.

## Kinaba

### Запуск Kibana локально

```yaml
version: '3.4'

services:
  elasticsearch:
    image: elasticsearch:7.17.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - ELASTIC_PASSWORD=your_password_here
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - esdata:/usr/share/elasticsearch/data

  kibana:
    image: kibana:7.17.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=elastic
      - ELASTICSEARCH_PASSWORD=your_password_here
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  esdata:
```

```sh
docker-compose up
```


### заполняем kibana тестовыми данными
```sh
pip install "elasticsearch[async]"
```

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=("elastic", "your_password_here"),
)

if not es.ping():
    raise ValueError("Connection failed")

print("Connected to Elasticsearch!")

index_name = "test_index"
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)
    print(f"Index '{index_name}' created.")

def add_document(index, doc_id, data):
    try:
        response = es.index(index=index, id=doc_id, document=data)
        print(f"Document {doc_id} added: {response['result']}")
    except Exception as e:
        print(f"Error adding document {doc_id}: {e}")

documents = [
    {"name": "John Doe", "age": 30, "city": "New York"},
    {"name": "Jane Smith", "age": 25, "city": "San Francisco"},
    {"name": "Alice Johnson", "age": 28, "city": "Los Angeles"},
]

for i, doc in enumerate(documents, start=1):
    add_document(index_name, i, doc)

print("Data successfully sent to Elasticsearch!")
```

### работа с Kibana

далее в web-интерфейсе
http://localhost:5601/app/home#/

Manage index lifecycles](http://localhost:5601/app/management/data/index_lifecycle_management) - добавляем индекс для "test_index"

и в home -> discover  можем его смотреть и выполнять к нему запросы
