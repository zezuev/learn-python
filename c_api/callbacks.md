# Calling Python Functions from C
Calling Python functions from C is especially useful for libraries that support callback functions.

The Python interpreter is easily called recursively, and there is a standard interface to call a Python function. First, the Python program must somehow pass the Python function object to the C code. A function should be provided to do this. When this function is called, a pointer to the Python function object is saved in a global variable.

    static PyObject *my_callback = NULL;

    static PyObject *
    my_set_callback(PyObject *dummy, PyObject *args)
    {
        PyObject *result = NULL;
        PyObject *temp;

        if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
            if (!PyCallable_Check(temp)) {
                PyErr_SetString(PyExc_TypeError, "parameter must be callable");
                return NULL;
            }
            Py_XINCREF(temp); // add a reference to new callback
            Py_XDECREF(my_callback); // dispose of previous callback
            my_callback = temp;
            // boilerplate to return None
            Py_INCREF(Py_None);
            result = Py_None;
        }
        return result;
    }

Later, when it is time to call the function, you call the C function **PyObject_CallObject()**. This function has two arguments, both pointer to arbitrary Python objects: the Python function, and the argument list. The argument list must always be a tuple object, whose length is the number of arguments the function takes. **Py_BuildValue()** returns a tuple when its format string consists of zero or more format codes between parentheses.

    int arg;
    PyObject *arglist;
    PyObject *result;
    arg = 123;
    arglist = Py_BuildValue("(i)", arg);
    result = PyObject_CallObject(my_callback, arglist);
    Py_DECREF(arglist);

**PyObject_CallObject()** returns a Python object pointer. This is the return value of the Python function. It is reference-count-neutral with respect to its arguments, which is why the newly created tuple was **Py_DECREF()**-ed immediately after the call. The return value of the call is new, either it is a brand new object, or it is an existing object whose reference count has been incremented. Unless you want to save it in a global variable, you should therefore **Py_DECREF()** the result.

You may also call a function with keyword arguments by using **PyObject_Call()**, which supports arguments and keyword arguments.

    PyObject *dict;
    dict = Py_BuildValue("{s:i}", "name", val);
    result = PyObject_Call(my_callback, NULL, dict);
    Py_DECREF(dict);
    if (result == NULL)
        return NULL;
    Py_DECREF(result);