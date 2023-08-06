======================
The asynctools library
======================

.. py:module:: asyncstdlib.asynctools
    :synopsis: core asynctools variants

The :py:mod:`asyncstdlib.asynctools` library implements the core toolset used by
:py:mod:`asyncstdlib` itself and similar utilities.
All documented members of this module are separate from internal implementation
and stable regardless of :py:mod:`asyncstdlib` internals.

.. versionadded:: 1.1.0

Iterator lifetime
=================

.. autofunction:: borrow(iterator: async iter T) -> async iter T

.. autofunction:: scoped_iter(iterable: (async) iter T)
    :async-with: :async iter T

Async transforming
==================

.. autofunction:: await_each(awaitables: iter await T)
    :async-for: :T

    .. versionadded:: 3.9.1

.. autofunction:: apply(func: (*T, **T) -> R, *args: await T, **kwargs: await T) -> R
    :async:

    .. versionadded:: 3.9.1
