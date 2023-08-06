"""
Automatically list fields from django models.

Based on https://djangosnippets.org/snippets/2533/
"""
import inspect

from django.db import models
from django.utils.encoding import force_text
from django.utils.html import strip_tags


def process_docstring(app, what, name, obj, options, lines):
    """
    Process docstrings for django models.

    Process docstrings for django models and add field description from
    their help_text attribute.
    """
    # Only look at objects that inherit from Django's base model class
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        # Grab the field list from the meta class
        fields = obj._meta.get_fields()

        for field in fields:
            if field.name == "id":
                continue

            if not hasattr(field, "help_text") and not hasattr(field, "verbose"):
                # XXX: log these?
                continue

            help_text = strip_tags(force_text(field.help_text))
            verbose_name = force_text(field.verbose_name).capitalize()

            if help_text:
                # Add the model field to the end of the docstring as a param
                # using the help text as the description
                lines.append(":param {}: {}".format(field.attname, help_text))
            else:
                # Add the model field to the end of the docstring as a param
                # using the verbose name as the description
                lines.append(":param {}: {}".format(field.attname, verbose_name))

            # Add the field's type to the docstring
            if isinstance(field, models.ForeignKey):
                to = field.remote_field.model
                lines.append(
                    ":type {}: {} to :class:`~{}.{}`".format(
                        field.attname, type(field).__name__, to.__module__, to.__name__
                    )
                )
            else:
                lines.append(":type {}: {}".format(field.attname, type(field).__name__))

    # Return the extended docstring
    return lines


def setup(app):
    """Register the docstring processor with sphinx."""
    app.connect("autodoc-process-docstring", process_docstring)
