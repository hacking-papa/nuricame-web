# nuricame-web

Make a contour by pictures, Web version.

- [Dependencies](#dependencies)
- [How to](#how-to)
  - [Develop](#develop)
  - [Test](#test)
  - [Deploy](#deploy)
- [Misc](#misc)
  - [License](#license)

## Dependencies

- Google App Engine
  - Python3
    - OpenCV
    - NumPy

## How to

### Develop

```shell
pip install --upgrade -r requirements.txt
```

### Test

```shell
pytest
```

The above command will search for all `test_*.py` to test.

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

## Misc

### License

[GOOD HACKING DADDY LICENSE](LICENSE.md)
