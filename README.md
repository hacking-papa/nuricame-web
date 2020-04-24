# nuricame-web

![logo](https://user-images.githubusercontent.com/32637762/80259456-96332b00-86c0-11ea-96c1-92ac7be7e228.png)

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

### [Holistically-Nested Edge Detection](https://github.com/s9xie/hed)

Special thanks to Saining Xie.

```text
@InProceedings{xie15hed,
  author = {"Xie, Saining and Tu, Zhuowen"},
  Title = {Holistically-Nested Edge Detection},
  Booktitle = "Proceedings of IEEE International Conference on Computer Vision",
  Year  = {2015},
}
```

![hed prototxt](https://user-images.githubusercontent.com/32637762/79853360-eb421900-8402-11ea-8872-4cf733871fdc.png)

### License

[GOOD HACKING PAPA LICENSE](LICENSE.md)
