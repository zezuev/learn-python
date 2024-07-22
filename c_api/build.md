# Building Arbitrary Values
**Py_BuildValue()** is declared as follows:

    PyObject *Py_BuildValue(const char *format, ...);

The arguments must not be pointers, just values. It returns a new Python object, suitable for returning from a C function called from Python. It builds a tuple if its format string contains two or more format units. If the format string is empty, it returns **None**.