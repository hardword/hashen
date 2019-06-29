### Descripton

This server is to provide base64 encoded value of sha-512 hash from the string(password) after waiting for a certain(default 5) seconds. It also supports end-points for a graceful shutdown and statistics about number of requests it processed and average time taken for the requests.

### Running the server

1. Building the Docker Image

    ```shell
    $ docker build -t hashen:latest .
    ```
2. Running the Docker Container

    ```shell
    $ docker run -d -p 8080:8080 hashen
    ```
3. Checking the Docker Container (with a sample output)
    
    ```shell
    $ docker ps --format "{{.ID}}|{{.Image}}|{{.Status}}|{{.Ports}}"
    ff16972aae5d|hashen|Up 5 seconds|0.0.0.0:8080->8080/tcp
    ```

### Functions (with sample outputs)

- Getting `based64` encoded `sha-512` hash of password
    
    ```shell
    $ curl --data "password=angryMonkey" http://localhost:8080/hash
    ZEHhWB65gUlzdVwtDQArEyx+KVLzp/aTaRaPlBzYRIFj6vjFdqEb0Q5B8zVKCZ0vKbZPZklJz0Fd7su2A+gf7Q==
    ```
- Getting the statisics data

    ```shell
    $ curl http://localhost:8080/stats
    {"average":1.0044774327959334,"total":14}
    ```
- Shutting Down the server (and checking)

    ```shell
    $ curl http://localhost:8080/shutdown
    Server shutting down...
    
    $ docker ps -a --format "{{.ID}}|{{.Image}}|{{.Status}}|{{.Ports}}"
    ff16972aae5d|hashen|Exited (0) 5 seconds ago|
    ```

