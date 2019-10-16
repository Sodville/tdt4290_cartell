# Running docker

## Build image
```
 docker build -t apitest .
```

## Run image
```
 docker run -p 5000:5000 apitest:latest
```

Add `-d` to detach it from the terminal
