# 1. Storer - Minimalist storage class for any purpose.

- [1. Storer](#1-storer)
  - [1.1. Quick start](#11-quick-start)
  - [1.2. Few examples](#12-few-examples)
  - [1.3. Contribution](#13-contribution)
  - [License](#-license)

The main idea of the Storer is to provided only few methods for powerful manupulating and keeping the data in the files.
Particularly methods `put` and `get` are enough for quick start.

## 1.1. Quick start

## Installation:
`
pip3 install Storer
`

1. Create an Storer instance: `s = Storer()`
2. Put something: `s.put(what=<what_ever_you_like>, name=<name_of_object>)`
3. Get something: `s.get(name=<name_of_object>)`
4. Look at internal data of the instance: `s.show()` or `output = s.show(get_string=True)`


## 1.2. Few examples

```python
>>> from storer import Storer
>>> s = Storer()
>>> s.put(what="string", name="my_string")
>>> s.get(name="my_string")
'string'
>>> 
```

```python
>>> from storer import Storer
>>> s = Storer(dump_path="~/my_folder_for_dumps", dump_name="dumps", verbose=True)
[Storer v.1.0.6 [55]] is initialized!
Dump folder: [~/my_folder_for_dumps]
[Storer] No data is available for loading...
>>> s.put(what=[i for i in range(10)], name="my_range")
>>> s.put(what={v:v*2 for v in range(5)}, name="my_dict")
>>> s.dump()
[Storer] ~/my_folder_for_dumps dumps dumping...  # at this point you have you data stored (force)
>>> 
```

However you can use just `put` methods and the Store will dump your data automatically:

```python
>>> from storer import Storer
>>> s = Storer(dump_path="~/my_folder_for_dumps", dump_name="dumps", verbose=True)
[Storer v.1.0.6 [55]] is initialized!
Dump folder: [~/my_folder_for_dumps]
[Storer] No data is available for loading...
>>> s.put(what=[i for i in range(10)], name="my_range")
>>> s.put(what={v:v*2 for v in range(5)}, name="my_dict")
>>> exit()
[Storer] ~/my_folder_for_dumps dumps dumping...
```


## 1.3. Contribution

Feel free to contribute to the project, but please create initially an issue with detailed problem and way to resolve it. 

## License
----

MIT
