# chemdataextractor-api
A wrapper around ChemDataExtractor providing a REST API

## Getting started

### Docker 

> docker pull lfoppiano/chemdataextractor-api:0.0.1

> docker run -p 8080:8080 lfoppiano/chemdataextractor-api:0.0.1

### Local version 

> conda create --name cde pip python=3.7

> pip install -r requirements.txt

> cde data download 

> python cde_service.py 

The service can be called with the following parameters:

```
usage: cde_service.py [-h] [--host HOST] [--port PORT]

Chemdataextractor API

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  Hostname to be bound the service
  --port PORT  Port to be listening to
```


## API 

  URL    | Parameter name | Parameter type |
---------|----------------|----------------| 
`/process`| text          |   form-data    | 


Example: 

> curl --location --request POST 'localhost:8080/process' \
--form 'text="The material BaFe 2 As 2 3 Ba has been studied for years. "'

will return 
```
[{"start": 13, "end": 29, "label": "BaFe 2 As 2 3 Ba"}]
```


## To be implemented
 - expose the additional methods for processing HTML and PDFs