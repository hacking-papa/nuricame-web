# nuricame-web

Make a contour by pictures, Web version.

- [Environment](#environment)
- [How to](#how-to)
  - [Develop](#develop)
  - [Deploy](#deploy)

## Environment

- Google App Engine
  - Python3
  - OpenCV

## How to

### Develop

```shell
pip install --upgrade -r requirements.txt
```

### Deploy

```shell
gcloud app deploy --project nuricame-web
```

And then, you can browse `https://nuricame-web.appspot.com/`, or type below.

```shell
gcloud app browse --project nuricame-web
```

If you want to check logs, type below.

```shell
gcloud app logs tail -s default
```
