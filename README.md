# Wagtail openedX

[![Build Status](https://github.com/African-Cities-Lab/wagtail-openedx/workflows/tests/badge.svg?branch=main)](https://github.com/African-Cities-Lab/wagtail-openedx/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/African-Cities-Lab/wagtail-openedx/branch/main/graph/badge.svg?token=SUqrfqOQEG)](https://codecov.io/gh/African-Cities-Lab/wagtail-openedx)

Lightweight CMS for openedX portals.

## Usage

1. Add `wagtail_openedx` to the `INSTALLED_APPS` setting as in:

    ```python
    INSTALLED_APPS = [
        ...
        "wagtail_openedx",
    ]
    ```

2. Add the `OPENEDX_API_URL` setting pointing to the URL of the target openedX API, e.g.:

    ```python
    OPENEDX_API_URL = "https://demo.africancitieslab.org/api"
    ```

3. Include the URL in the project `urls.py` as in:


    path("catalog/", include("wagtail_openedx.urls")),

4. Run ``python manage.py migrate`` to create the models.

5. Start the development server and go to `https://localhost:8000/catalog/sync-courses`

See [African-Cities-Lab/wagtail-openedx-site](https://github.com/African-Cities-Lab/wagtail-openedx-site) for an example production-ready django site using `wagtail-openedx`.


## Acknowledgments

[![Built with Cookiecutter Django Package](https://img.shields.io/badge/built%20with-cookiecutter%20djangopackage-ff69b4.svg?logo=cookiecutter)](https://github.com/pydanny/cookiecutter-djangopackage/)
