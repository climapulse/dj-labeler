=======
Labeler
=======

The most annoying thing about Django models is their verbosity when you want to do things right. As soon as you
have an international audience, you'll need to start marking strings for translation. Labeler was created to reduce
the noise by externalizing a model's labels and help texts; it even provides the same functionality for any Django
form.

Installation
------------

Labeler is available on Pypi as ``dj-labeler``::

    pip install dj-labeler


Example
-------

Imagine our ``bookstore`` models look like this::

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=200)
        published = models.BooleanField(default=False)
        birthdate = models.DateField(blank=True, null=True)


    class Book(models.Model):
        title = models.CharField(max_length=200)
        published_on = models.DateField(blank=True, null=True)
        isbn = models.CharField(max_length=50)
        authors = models.ManyToManyField(Author)


Now you want to branch out into a Dutch-speaking market. Instead of relying on Django's automagical label creation
based on the field name, you'll need to explicitly state your verbose name for each field *and* mark it as a
translatable string. And to avoid any confusion for the people performing the Dutch translation, you want to
provide as much context as possible, because an author's name might not require the same label as the name of
a category.

So you end up with this::


    from django.db import models
    from django.utils.translation import pgettext_lazy

    class Author(models.Model):
        name = models.CharField(pgettext_lazy('author', 'name'), max_length=200)
        published = models.BooleanField(pgettext_lazy('author', 'published'), editable=False)
        birthdate = models.DateField(pgettext_lazy('author', 'birthdate'), blank=True, null=True)

        class Meta:
            verbose_name = pgettext_lazy('author model', 'Author')
            verbose_name_plural = pgettext_lazy('author model (plural)', 'Authors')


    class Book(models.Model):
        title = models.CharField(pgettext_lazy('book', 'title'), max_length=200)
        published_on = models.DateField(pgettext_lazy('book (date)', 'published'), blank=True, null=True)
        isbn = models.CharField(pgettext_lazy('book', 'isbn'), max_length=50)
        authors = models.ManyToManyField(Author, verbose_name=pgettext_lazy('book authors', 'authors'))

        class Meta:
            verbose_name = pgettext_lazy('author model', 'Book')
            verbose_name_plural = pgettext_lazy('author model (plural)', 'Books')


Now add in help text and you've got a lot of noise, making it hard to discern the attributes you as a programmer
care about most when developing, like the maximum length and whether a field is optional.

Labeler will enable apps to use i18nized strings with less noise. Let's move the strings to a separate file
we'll call `i18n.py` (but any name will do) and use Labeler's ``ModelTranslations``::

    # i18n.py
    from django.utils.translation import pgettext_lazy
    from labeler import ModelTranslations

    author = ModelTranslations(
        labels=dict(
            name=pgettext_lazy('author', 'name'),
            published=pgettext_lazy('author', 'published'),
            birthdate=pgettext_lazy('author', 'birthdate')
        )
        help_texts=dict(
            birthdate=pgettext_lazy('author', 'When was the author born?')
        ),
        name=pgettext_lazy('author model', 'Author'),
        name_plural=pgettext_lazy('author model (plural)', 'Authors')
    )

    book = ModelTranslations(
        labels=dict(
            title=pgettext_lazy('book', 'title'),
            published_on=pgettext_lazy('book (date)', 'published'),
            isbn=pgettext_lazy('book', 'isbn'),
            authors=pgettext_lazy('book authors', 'authors')
        ),
        help_texts=dict(
            isbn=pgettext_lazy('book', 'The ISBN will be validated against XYZ database')
        ),
        name=pgettext_lazy('author model', 'Book'),
        name_plural=pgettext_lazy('author model (plural)', 'Books')
    )

That's still a lot of noise, but at least we've got it isolated to a single file in our app. Now, since
``ModelTranslations`` is simply an extension of ``dict``, you could start doing things like this::

    from . import i18n

    class Author(models.Model):
        # as above

        class Meta:
            verbose_name = i18n.author['name']
            verbose_name_plural = i18n.author['name_plural']

But that doesn't cut down on the noise. Instead you should use the ``inject`` method/decorator of ``ModelTranslations``
(or ``FormTranslation`` when dealing with a form). This will make our models become lean and mean::

    # models.py
    from django.db import models
    from labeler.models import label_with
    from . import i18n

    @i18n.author.inject
    class Author(models.Model):
        name = models.CharField(max_length=200)
        published = models.BooleanField(default=False)
        birthdate = models.DateField(blank=True, null=True)


    @i18n.book.inject
    class Book(models.Model):
        title = models.CharField(max_length=200)
        published_on = models.DateField(blank=True, null=True)
        isbn = models.CharField(max_length=50)
        authors = models.ManyToManyField(Author)


The above example is equivalent to our noisy example where we first introduced internationalized strings.


Using ModelTranslations
-----------------------

``ModelTranslations`` is a simple dict with some useful methods and properties added on top. Nothing is required,
but if you specify ``labels`` or ``help_texts``, the keys of those dictionaries should refer to existing model fields.

Example::

    from labeler import ModelTranslations

    my_model = ModelTranslations(
        labels=dict(  # verbose_name of the model's fields
            model_field_a='Something',
            model_field_b='Else'
        ),
        help_texts=dict(  # help_text of the model's fields
            model_field_a='Some help text'
        ),
        name='my model',  # verbose_name of the model
        name_plural='my models',  # verbose_name_plural of the model
        errors=dict(  # Handy dict of error messages for this model
            invalid_state='Some error'
        ),
        messages=dict(  # Handy dict for other kinds of messages
            congrats='Success!'
        ),
        something_else='abc',  # Just a dict; add whatever you want
        my_choices={
            'ok': 'Great',
            'nok': 'Eh, try again'
        }
    )

When everything is good and ready to go, simply inject this on your model::

    from . import i18n

    @i18n.my_model.inject
    class MyModel(models.Model):
        # Your fields and stuff goes here of course

The nested labels, errors, and help_texts dictionaries are also available as properties. This means custom validation
might look like this::

    def clean_fields(self, exclude=None):
        super(MyModel, self).clean_fields(exclude)
        if self.field not in VALID_STATE:
            raise ValidationError({'field': i18n.my_translations.errors['invalid_state']})

If you're dealing with lots of nested dicts, you can use the ``resolve`` method::


    hard_way = i18n.my_model.get('errors', {}).get('fieldname', {}).get('invalid', {}).get('state')
    easier_way = i18n.my_model.resolve('errors.fieldname.invalid.state')
    easier_way == hard_way


Using FormTranslations
----------------------

``FormTranslations`` works exactly like ``ModelTranslations``, but it also supports a nested dictionary
``empty_labels`` to override the default empty label on form fields. Usage::


    # i18n.py
    from labeler import FormTranslations

    article_form = FormTranslations(
        labels=dict(
            title='Title goes here',
            body='Text goes here',
            published='When to publish this article',
            author='Author',
        ),
        help_texts=dict(
            title='Limit to 100 characters please',
            body='Formatting is not supported'
        ),
        empty_labels=dict(
            author='Please select an author'
        )
    )

    # forms.py
    from django import forms
    from . import i18n
    from .models import Article

    @i18n.article_form.inject
    class ArticleForm(forms.ModelForm):

        class Meta:
            model = Article
            fields = ('title', 'body', 'published', 'author')


That's all there is to it.
