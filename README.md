# KazdreamSimple

## Installation

### Build the image
```
docker compose build
```

### Run the container
```
docker compose up
```

## Usage
There are two endpoints, one for parsing and one for retrieving items:
* Parse items - http://127.0.0.1:8000/smartphones/parse
* Retrieve items - http://127.0.0.1:8000/smartphones

Note, that `/smartphone/parse` may take some time. 

