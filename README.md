# Website Sentiment Analisis Judul Berita

## Installation

1. Clone this project

```sh
git clone https://github.com/defrindr/2024-websentiment.git
```

2. Create Virtual Environment

```sh
python3 -m venv myvenv
```

3. Activate Virtual Environment

```sh
source myvenv/bin/activate
```

3. Go to directory src

```sh
cd src
```

4. Install requirements

```sh
pip install -r requirements.txt
```

4. Atur database, konfigurasi ada di .flaskenv

5. Jalankan Migration

```sh
alembic upgrade head
```

5. Running project

```sh
flask run
```
