
Running development version
================================

To examine in development virtual environment:

   pip install Mercurial==«X-Y-Z»
   pip install dbus-python
   pip install keyring

then install ``mercurial_extension_utils`` and ``mercurial_keyring`` (possibly by
``pip --edit``).

Note that ``dbus-python`` is not enforced by dependencies but it's presence makes
various Linux backends available.
