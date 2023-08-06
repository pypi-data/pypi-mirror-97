# Mettle #

Bitsmiths-Mettle is the supporting code generators and python libraries for the Mettle project.

See our <a href="https://bitbucket.org/bitsmiths_za/mettle.git">repo</a> and main *README* for more details!


## Requirements ##

Python 3.7+


## Installation ##

```console
$ pip install bitsmiths-mettle

---> 100%
```

## Change History ##

### 2.1.2 ###

| Type | Description |
| ---- | ----------- |
| Bug  | All python database drivers now return empty strings instead of None from null columns. |


### 2.1.1 ###

| Type   | Description |
| ------ | ----------- |
| Bug    | Fixed generated python queries without input parameters not generating exec() methods. |
| Change | The `lock()` methods for database connectors now accept a `Stmnt` object, generated code updated to pass this in. |
| Change | The C++ `connect()` that takes arguments has changed to be more generic. |
| New    | Added `psycopg2` connector. |



## License ##

This project is licensed under the terms of the MIT license.
