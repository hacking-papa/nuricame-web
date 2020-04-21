# nuricame-web

Make a contour by pictures, Web version.

- [Dependencies](#dependencies)
- [How to](#how-to)
  - [Develop](#develop)
  - [Launch](#launch)
  - [Test](#test)
  - [Deploy](#deploy)
- [Misc](#misc)
  - [Holistically-Nested Edge Detection](#holistically-nested-edge-detection)
  - [License](#license)

## Dependencies

- Google App Engine
  - Python3
    - OpenCV
    - NumPy
  - [Bulma CSS](https://bulma.io/)
  - [Alpine.js](https://github.com/alpinejs/alpine)

## How to

### Develop

```shell
export GOOGLE_APPLICATION_CREDENTIALS=[path-to-your-service-accounts-private-key]
```

```shell
pip install --upgrade -r requirements.txt
```

### Launch

```shell
python main.py
```

### Test

```shell
pytest
```

The above command will search for all `test_*.py` to test.

### Deploy

```shell
gcloud app deploy --project [project-id]
```

And then, you can browse `https://[project-id].appspot.com/`, or type below.

```shell
gcloud app browse --project [project-id]
```

If you want to check logs, type below.

```shell
gcloud app logs tail -s default
```

## Misc

### Holistically-Nested Edge Detection

![hed prototxt](https://user-images.githubusercontent.com/32637762/79853360-eb421900-8402-11ea-8872-4cf733871fdc.png)

### License

[GOOD HACKING PAPA LICENSE](LICENSE.md)
