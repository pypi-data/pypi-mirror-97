Trite support for code predicates, presently just the context manager `post_condition`.

*Latest release 20210306*:
Package install_requires fix.

Interested people should also see the `icontract` module.

## Function `post_condition(*predicates)`

Context manager to test post conditions.

Predicates may either be a tuple of `(description,callable)`
or a plain callable.
For the latter the description is taken from `callable.__doc__`
or `str(callable)`.
Raises `AssertionError` if any predicates are false.

# Release Log



*Release 20210306*:
Package install_requires fix.

*Release 20190221*:
One bugfix, other tiny changes.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
Initial release with post_condition context manager.
