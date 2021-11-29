**************
Wagtail Lottie
**************

.. image:: https://img.shields.io/pypi/v/wagtail_lottie
    :target: https://pypi.org/project/wagtail_lottie/

.. image:: https://img.shields.io/pypi/pyversions/wagtail_lottie
    :target: https://pypi.org/project/wagtail_lottie/


`Wagtail <https://github.com/wagtail/wagtail>`_ + `Lottie <https://github.com/airbnb/lottie-web>`_
is a Wagtail package
for playing `Adobe After Effects <https://www.adobe.com/products/aftereffects.html>`_ animations
exported as json with `Bodymovin <https://exchange.adobe.com/creativecloud.details.12557.html>`_.

.. image:: https://static.snoweb.io/media/wagtail-lottie.gif

Usage
#####

1. Export your animation from Adobe After Effect with Bodymovin.
2. Compress the folder in zip format.
3. Create a Lottie animation from Wagtail and add this zip file.

Can be used like this at Wagtail page level :

.. code-block:: python

    from wagtail_lottie.models import LottieAnimation
    from wagtail_lottie.widgets import LottieAnimationChooser
    from wagtail_lottie.blocks import LottieAnimationChooserBlock


    class HomePage(Page):
        lottie_animation_foreign_key = models.ForeignKey(LottieAnimation, on_delete=models.SET_NULL)
        lottie_animation_stream_field = StreamField([
            ('lottie_animation_block', LottieAnimationChooserBlock()),
            ('rich_text', blocks.RichTextBlock())
        ])

        content_panels = [
            FieldPanel('lottie_animation_foreign_key', widget=LottieAnimationChooser),
            StreamFieldPanel('lottie_animation_stream_field')
        ]


And rendered this way at html level :

.. code-block:: html


    <!-- For ForeignKey -->
    {% include 'wagtail_lottie/lottie_animation.html' with value=page.lottie_animation_foreign_key %}

    <!-- For StreamField -->
    {% for block in page.lottie_animation_stream_field %}
        {% include_block block %}
    {% endfor %}

    <!-- These scripts are required to launch animations -->
    <script src="{% static 'wagtail_lottie/lottie-player.js' %}"></script>
    <script src="{% static 'wagtail_lottie/lottie-animation.js' %}"></script>


Setup
#####

Install with pip :

.. code-block::

    pip install wagtail_lottie

Add **wagtail_lottie** to Django apps installed :

.. code-block:: python

    INSTALLED_APPS = [
        'wagtail_lottie',
        'wagtail.contrib.modeladmin',
        'generic_chooser',
        ...
    ]

Run some Django commands :

.. code-block::

    python manage.py collectstatic
    python manage.py migrate

Set if needed **Wagtail Lottie** download folder in the Django settings (default value is 'wagtail_lottie') :

.. code-block:: python

    WAGTAIL_LOTTIE_UPLOAD_FOLDER = 'custom_location'

