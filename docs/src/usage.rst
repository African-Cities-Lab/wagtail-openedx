=====
Usage
=====

To use Wagtail openedX in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtail_openedx.apps.WagtailOpenedxConfig',
        ...
    )

Add Wagtail openedX's URL patterns:

.. code-block:: python

    from wagtail_openedx import urls as wagtail_openedx_urls


    urlpatterns = [
        ...
        url(r'^', include(wagtail_openedx_urls)),
        ...
    ]
