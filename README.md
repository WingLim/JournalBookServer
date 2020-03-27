# JournalBook Server

A Serverside for [JournalBook](https://github.com/WingLim/JournalBook)

## Deploy

### Deploy with docker

```bash
$ docker run -itd \
	-v /your/path/data:/root/data \
	-e TOKEN=yourtoken \
    -p 5000:5000 \
	--restart always
```

### Deploy manually 

1. Clone code
```bash
$ git clone https://github.com/WingLim/JournalBookServer.git
```

2. Install requirements
```bash
$ pip install -r requirements.txt
```

3. Edit config.py
```python
pwd = "yourtoken"
```

4. Run server
```bash
$ pyhon api.py
```

## Usage

Open https://journalxbook.netlify.com/settings/

Input server url and the token you set

**Notes: The server url should have / in last**