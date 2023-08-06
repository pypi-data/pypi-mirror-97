# enShroud

![](/img/enShroud.png)

## Introduction

A steganography tool to hide secret texts in white space.

## Usage:

- To encode:

```python
enShroud -e -p PATH_TO_TEXT_FILE -o PATH_TO_OUTPUT -s "SECRET_MESSAGE_IN_QUOTES"
```

- To decode:

```python
enShroud -d -p PATH_TO_TEXT_FILE
```

**NOTE**: Add the path where enShroud is installed to your PATH variable.

## Alternate Method:

- Download the .whl file from <a href="https://pypi.org/project/enshroud/#files">pypi downloads</a> section.
- In the directory where the .whl file is downloaded, run:

```python
pip install file_name.whl
```
