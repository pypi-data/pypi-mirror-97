==========
Validators
==========

Validators are components that validate submitted data. This is certainly not
a new concept, but in the previous form frameworks validation was hidden in
many places:

* Field/Widget Validation

  The schema field consists of a ``validate()`` method. Validation is
  automatically invoked when converting a unicode string to a field value
  using ``fromUnicode()``. This makes it very hard to customize the field
  validation. No hooks were provided to exert additional restriction at the
  presentation level.

* Schema/Form Validation

  This type of validation was not supported at all initially. ``zope.formlib``
  fixed this problem by validating against schema invariants. While this was a
  first good step, it still made it hard to customize validators, since it
  required touching the base implementations of the forms.

* Action Validation

  ``zope.formlib`` supports the notion of action validatos. Actions have a
  success and failure handler. If the validation succeeds, the success handler
  is called, otherwise the failure handler is chosen. We believe that this
  design was ill-conceived, especially the default, which required the data to
  completely validate in order for the action to successful. There are many
  actions that do not even care about the data in the form, such as "Help",
  "Cancel" and "Reset" buttons. Thus validation should be part of the data
  retrieval process and not the action.

For me, the primary goals of the validator framework are as follows:

* Assert additional restrictions on the data at the presentation
  level.

  There are several use cases for this. Sometimes clients desire additional
  restrictions on data for their particular version of the software. It is not
  always desireable to adjust the model for this client, since the framework
  knows how to handle the less restrictive case anyways. In another case,
  additional restrictions might be applied to a particular form due to limited
  restrictions.

* Make validation pluggable.

  Like most other components of this package, it should be possible to control
  the validation adapters at a fine grained level.

  * Widgets: context, request, view, field[1], widget

  * Widget Managers: context, request, view, schema[2], manager

  [1].. This is optional, since widgets must not necessarily have fields.
  [2].. This is optional, since widget managers must not necessarily have
  manage field widgets and thus know about schemas.

* Provide good defaults that behave sensibly.

  Good defaults are, like in anywhere in this pacakge, very important. We have
  chosen to implement the ``zope.formlib`` behavior as the default, since it
  worked very well -- with exception of action validation, of course.

For this package, we have decided to support validators at the widget and
widget manager level. By default the framework only supports field widgets,
since the validation of field-absent widgets is generally not
well-defined. Thus, we first need to create a schema.

  >>> from pyramid.testing import setUp, tearDown, DummyRequest
  >>> config = setUp(hook_zca=True)

  >>> from cornice import includeme as include_cornice
  >>> include_cornice(config)
  >>> from pyams_utils import includeme as include_utils
  >>> include_utils(config)
  >>> from pyams_site import includeme as include_site
  >>> include_site(config)
  >>> from pyams_i18n import includeme as include_i18n
  >>> include_i18n(config)
  >>> from pyams_form import includeme as include_form
  >>> include_form(config)

  >>> from pyams_form import interfaces, util, testing
  >>> testing.setup_form_defaults(config.registry)

  >>> from pyams_layer.interfaces import IFormLayer

  >>> import zope.interface
  >>> import zope.schema
  >>> class IPerson(zope.interface.Interface):
  ...     login = zope.schema.TextLine(
  ...         title='Login',
  ...         min_length=1,
  ...         max_length=10,
  ...         required=True)
  ...
  ...     email = zope.schema.TextLine(
  ...         title='E-mail')
  ...
  ...     @zope.interface.invariant
  ...     def isLoginPartOfEmail(person):
  ...         if not person.email.startswith(person.login):
  ...             raise zope.interface.Invalid("The login not part of email.")
  >>> @zope.interface.implementer(IPerson)
  ... class Person(object):
  ...     login = None
  ...     email = None


Widget Validators
-----------------

Widget validators only validate the data of one particular widget. The
validated value is always assumed to be an internal value and not a widget
value.

By default, the system uses the simple field validator, which simply uses the
``validate()`` method of the field. For instantiation, all validators have the
following signature for its discriminators: context, request, view, field, and
widget

  >>> request = testing.TestRequest()

  >>> from pyams_form import validator
  >>> simple = validator.SimpleFieldValidator(
  ...     None, request, None, IPerson['login'], None)

A validator has a single method ``validate()``. When the validation is
successful, ``None`` is returned:

  >>> simple.validate('srichter')

A validation error is raised, when the validation fails:

  >>> simple.validate('StephanCaveman3')
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.TooLong: ('StephanCaveman3', 10)

Let's now create a validator that also requires at least 1 numerical character
in the login name:

  >>> import re
  >>> class LoginValidator(validator.SimpleFieldValidator):
  ...
  ...     def validate(self, value):
  ...         super().validate(value)
  ...         if re.search('[0-9]', value) is None:
  ...             raise zope.interface.Invalid('No numerical character found.')

Let's now try our new validator:

  >>> login = LoginValidator(None, request, None, IPerson['login'], None)

  >>> login.validate('srichter1')

  >>> login.validate('srichter')
  Traceback (most recent call last):
  ...
  zope.interface.exceptions.Invalid: No numerical character found.

We can now register the validator with the component architecture, ...

  >>> config.registry.registerAdapter(LoginValidator,
  ...       required=(None, None, None, zope.schema.interfaces.IField, None),
  ...       provided=interfaces.IValidator)

and look up the adapter using the usual way:

  >>> config.registry.queryMultiAdapter((None, None, None, IPerson['login'], None),
  ...                                   interfaces.IValidator)
  <LoginValidator for IPerson['login']>

Unfortunately, the adapter is now registered for all fields, so that the
E-mail field also has this restriction (which is okay in this case, but not
generally):

  >>> config.registry.queryMultiAdapter((None, request, None, IPerson['email'], None),
  ...                                   interfaces.IValidator)
  <LoginValidator for IPerson['email']>

The validator module provides a helper function to set the discriminators for
a validator, which can include instances:

  >>> validator.WidgetValidatorDiscriminators(
  ...     LoginValidator, field=IPerson['login'])

Let's now clean up the component architecture and register the login validator
again:

  >>> tearDown()
  >>> config = setUp(hook_zca=True)

  >>> config.registry.registerAdapter(LoginValidator,
  ...       provided=interfaces.IValidator)

  >>> config.registry.queryMultiAdapter(
  ...     (None, None, None, IPerson['login'], None),
  ...     interfaces.IValidator)
  <LoginValidator for IPerson['login']>

  >>> config.registry.queryMultiAdapter(
  ...     (None, None, None, IPerson['email'], None),
  ...     interfaces.IValidator)


Ignoring unchanged values
~~~~~~~~~~~~~~~~~~~~~~~~~

Most of the time we want to ignore unchanged fields/values at validation.
A common usecase for this is if a value went away from a vocabulary and we want
to keep the old value after editing.
In case you want to strict behaviour, register ``StrictSimpleFieldValidator``
for your layer.

  >>> simple = validator.SimpleFieldValidator(
  ...     None, None, None, IPerson['login'], None)

NOT_CHANGED never gets validated.

  >>> from pyams_utils.interfaces.form import NOT_CHANGED, IDataManager
  >>> simple.validate(NOT_CHANGED)

Current value gets extracted by ``IDataManager``
via the widget, field and context

  >>> from pyams_form.datamanager import AttributeField
  >>> config.registry.registerAdapter(AttributeField,
  ...       required=(zope.interface.Interface, zope.schema.interfaces.IField),
  ...       provided=IDataManager)

  >>> request = testing.TestRequest()
  >>> from pyams_form import widget
  >>> widget = widget.Widget(request)
  >>> context = Person()

  >>> widget.context = context
  >>> zope.interface.alsoProvides(widget, interfaces.form.IContextAware)

  >>> simple = validator.SimpleFieldValidator(
  ...     context, request, None, IPerson['login'], widget)

OK, let's see checking after setup.
Works like a StrictSimpleFieldValidator until we have to validate a different value:

  >>> context.login = 'john'
  >>> simple.validate('carter')
  >>> simple.validate('hippocratiusxy')
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.TooLong: ('hippocratiusxy', 10)

Validating the unchanged value works despite it would be an error.

  >>> context.login = 'hippocratiusxy'
  >>> simple.validate('hippocratiusxy')

Unless we want to force validation:

  >>> simple.validate('hippocratiusxy', force=True)
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.TooLong: ('hippocratiusxy', 10)

Some exceptions:

``missing_value`` gets validated

  >>> simple.validate(IPerson['login'].missing_value)
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.RequiredMissing: login


Widget Validators and File-Uploads
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

File-Uploads behave a bit different than the other form
elements. Whether the user did not choose a file to upload
``NOT_CHANGED`` is set as value. But the validator knows
how to handle this.

The example has two bytes fields where File-Uploads are possible, one
field is required the other one not:

  >>> class IPhoto(zope.interface.Interface):
  ...     data = zope.schema.Bytes(
  ...         title='Photo',
  ...         required=True)
  ...
  ...     thumb = zope.schema.Bytes(
  ...         title='Thumbnail',
  ...         required=False)

There are several possible cases to differentiate between:

No widget
+++++++++

If there is no widget or the widget does not provide
``interfaces.IContextAware``, no value is looked up from the
context. So the not required field validates successfully but the
required one has an required missing error, as the default value of
the field is looked up on the field:

  >>> simple_thumb = validator.StrictSimpleFieldValidator(
  ...     None, request, None, IPhoto['thumb'], None)
  >>> simple_thumb.validate(NOT_CHANGED)

  >>> simple_data = validator.StrictSimpleFieldValidator(
  ...     None, request, None, IPhoto['data'], None)
  >>> simple_data.validate(NOT_CHANGED)
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.RequiredMissing: data

Widget which ignores context
++++++++++++++++++++++++++++

If the context is ignored in the widget - as in the add form - the
behavior is the same as if there was no widget:

  >>> import pyams_form.widget
  >>> widget = pyams_form.widget.Widget(None)
  >>> zope.interface.alsoProvides(widget, interfaces.form.IContextAware)
  >>> widget.ignore_context = True
  >>> simple_thumb = validator.StrictSimpleFieldValidator(
  ...     None, request, None, IPhoto['thumb'], widget)
  >>> simple_thumb.validate(NOT_CHANGED)

  >>> simple_data = validator.StrictSimpleFieldValidator(
  ...     None, request, None, IPhoto['data'], widget)
  >>> simple_data.validate(NOT_CHANGED)
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.RequiredMissing: data

Look up value from default adapter
++++++++++++++++++++++++++++++++++

When the value is ``NOT_CHANGED`` the validator tries to
look up the default value using a ``interfaces.IValue``
adapter. Whether the adapter is found, its value is used as default,
so the validation of the required field is successful here:

  >>> data_default = pyams_form.widget.StaticWidgetAttribute(
  ...     b'data', context=None, request=None, view=None,
  ...     field=IPhoto['data'], widget=widget)
  >>> config.registry.registerAdapter(data_default, name='default')
  >>> simple_data.validate(NOT_CHANGED)


Look up value from context
++++++++++++++++++++++++++

If there is a context aware widget which does not ignore its context,
the value is looked up on the context using a data manager:

  >>> @zope.interface.implementer(IPhoto)
  ... class Photo(object):
  ...     data = None
  ...     thumb = None
  >>> photo = Photo()
  >>> widget.ignore_context = False
  >>> config.registry.registerAdapter(AttributeField,
  ...       required=(zope.interface.Interface, zope.schema.interfaces.IField),
  ...       provided=IDataManager)

  >>> simple_thumb = validator.StrictSimpleFieldValidator(
  ...     photo, request, None, IPhoto['thumb'], widget)
  >>> simple_thumb.validate(NOT_CHANGED)

If the value is not set on the context it is a required missing as
neither context nor input have a valid value:

  >>> simple_data = validator.StrictSimpleFieldValidator(
  ...     photo, request, None, IPhoto['data'], widget)
  >>> simple_data.validate(NOT_CHANGED)
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.RequiredMissing: data

After setting the value validation is successful:

  >>> photo.data = b'data'
  >>> simple_data.validate(NOT_CHANGED)


Clean-up
++++++++

  >>> config.registry.unregisterAdapter(pyams_form.datamanager.AttributeField,
  ...       required=(zope.interface.Interface, zope.schema.interfaces.IField),
  ...       provided=IDataManager)
  True
  >>> config.registry.unregisterAdapter(data_default, name='default')
  True


Ignoring required
~~~~~~~~~~~~~~~~~

Sometimes we want to ignore ``required`` checking.
That's because we want to have *all* fields extracted from the form
regardless whether required fields are filled.
And have no required-errors displayed.

  >>> class IPersonRequired(zope.interface.Interface):
  ...     login = zope.schema.TextLine(
  ...         title='Login',
  ...         required=True)
  ...
  ...     email = zope.schema.TextLine(
  ...         title='E-mail')

  >>> simple = validator.SimpleFieldValidator(
  ...     None, request, None, IPersonRequired['login'], None)

  >>> simple.validate(None)
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.RequiredMissing: login

Ooops we need a widget too.

  >>> widget = pyams_form.widget.Widget(None)
  >>> widget.field = IPersonRequired['login']

  >>> simple = validator.SimpleFieldValidator(
  ...     None, request, None, IPersonRequired['login'], widget)

  >>> simple.validate(None)
  Traceback (most recent call last):
  ...
  zope.schema._bootstrapinterfaces.RequiredMissing: login

Meeeh, need to signal that we need to ignore ``required``:

  >>> widget.ignore_required_on_validation = True

  >>> simple.validate(None)


Widget Manager Validators
-------------------------

The widget manager validator, while similar in spirit, works somewhat
different. The discriminators of the widget manager validator are: context,
request, view, schema, and manager.

A simple default implementation is provided that checks the invariants of the
schemas:

  >>> invariants = validator.InvariantsValidator(
  ...     None, request, None, IPerson, None)

Widget manager validators have the option to validate a data dictionary,

  >>> invariants.validate(
  ...     {'login': 'srichter', 'email': 'srichter@foo.com'})
  ()

or an object implementing the schema:

  >>> @zope.interface.implementer(IPerson)
  ... class Person(object):
  ...     login = 'srichter'
  ...     email = 'srichter@foo.com'
  >>> stephan = Person()

  >>> invariants.validate_object(stephan)
  ()

Since multiple errors can occur during the validation process, all errors are
collected in a tuple, which is returned. If the tuple is empty, the validation
was successful. Let's now generate a failure:

  >>> errors = invariants.validate(
  ...     {'login': 'srichter', 'email': 'strichter@foo.com'})

  >>> for e in errors:
  ...     print(e.__class__.__name__ + ':', e)
  Invalid: The login not part of email.

Let's now have a look at writing a custom validator. In this case, we want to
ensure that the E-mail address is at most twice as long as the login:

  >>> class CustomValidator(validator.InvariantsValidator):
  ...     def validate_object(self, obj):
  ...         errors = super().validate_object(obj)
  ...         if len(obj.email) > 2 * len(obj.login):
  ...             errors += (zope.interface.Invalid('Email too long.'),)
  ...         return errors

Since the ``validate()`` method of ``InvatiantsValidator`` simply uses
``validate_object()`` it is enough to only override ``validate_object()``. Now
we can use the validator:

  >>> custom = CustomValidator(
  ...     None, request, None, IPerson, None)

  >>> custom.validate(
  ...     {'login': 'srichter', 'email': 'srichter@foo.com'})
  ()
  >>> errors = custom.validate(
  ...     {'login': 'srichter', 'email': 'srichter@foobar.com'})
  >>> for e in errors:
  ...     print(e.__class__.__name__ + ':', e)
  Invalid: Email too long.

To register the custom validator only for this schema, we have to use the
discriminator generator again.

  >>> from pyams_form import util
  >>> validator.WidgetsValidatorDiscriminators(
  ...     CustomValidator, schema=util.get_specification(IPerson, force=True))

Note: Of course we could have used the ``zope.component.adapts()`` function
      from within the class, but I think it is too tedious, since you have to
      specify all discriminators and not only the specific ones you are
      interested in.

After registering the validator,

  >>> config.registry.registerAdapter(CustomValidator,
  ...       provided=interfaces.IManagerValidator)

it becomes the validator for this schema:

  >>> config.registry.queryMultiAdapter(
  ...     (None, request, None, IPerson, None), interfaces.IManagerValidator)
  <CustomValidator for IPerson>

  >>> class ICar(zope.interface.Interface):
  ...     pass
  >>> config.registry.queryMultiAdapter(
  ...     (None, None, None, ICar, None), interfaces.IManagerValidator)


The Data Wrapper
----------------

The ``Data`` class provides a wrapper to present a dictionary as a class
instance. This is used to check for invariants, which always expect an
object. While the common use cases of the data wrapper are well tested in the
code above, there are some corner cases that need to be addressed.

So let's start by creating a data object:

  >>> context = object()
  >>> data = validator.Data(IPerson, {'login': 'srichter', 'other': 1}, context)

When we try to access a name that is not in the schema, we get an attribute
error:

  >>> data.address
  Traceback (most recent call last):
  ...
  AttributeError: address

  >>> data.other
  Traceback (most recent call last):
  ...
  AttributeError: other

If the field found is a method, then a runtime error is raised:

  >>> class IExtendedPerson(IPerson):
  ...     def compute():
  ...         """Compute something."""

  >>> data = validator.Data(IExtendedPerson, {'compute': 1}, context)
  >>> data.compute
  Traceback (most recent call last):
  ...
  RuntimeError: ('Data value is not a schema field', 'compute')

Finally, the context is available as attribute directly:

  >>> data.__context__ is context
  True

It is used by the validators (especially invariant validators) to provide a
context of validation, for example to look up a vocabulary or access the
parent of an object. Note that the context will be different between add and
edit forms.

Validation of interface variants when not all fields are displayed in form
--------------------------------------------------------------------------

We need to register the data manager to access the data on the context object:

  >>> from pyams_form import datamanager
  >>> config.registry.registerAdapter(datamanager.AttributeField,
  ...       required=(zope.interface.Interface, zope.schema.interfaces.IField),
  ...       provided=IDataManager)

Sometimes you might leave out fields in the form which need to compute the
invariant. An exception should be raised. The data wrapper is used to test
the invariants and looks up values on the context object that are left out in
the form.

  >>> invariants = validator.InvariantsValidator(
  ...     stephan, request, None, IPerson, None)
  >>> errors = invariants.validate({'email': 'foo@bar.com'})
  >>> errors[0].__class__.__name__
  'Invalid'
  >>> errors[0].args[0]
  'The login not part of email.'


Tests cleanup:

  >>> tearDown()
