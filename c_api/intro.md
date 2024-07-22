# Extending Python with C
Extension modules can implement new built-in objects, and they can call C library functions and system calls.

To support extensions, the **Python.h** header needs to be included.

## Syscall Example
We can create an extension module called **spam** to be used as follows:

    import spam
    status = spam.system("ls -l")

Inside **spammodule.c**, we can write the following:

    #define PY_SSIZE_T_CLEAN
    #include <Python.h>

    static PyObject *
    spam_system(PyObject *self, PyObject *args)
    {
        const char *command;
        int sts;

        if (!PyArg_ParseTuple(args, "s", &command))
            return NULL;
        sts = system(command);
        return PyLong_FromLong(sts);
    }

The **self** argument points to the module object for module-level functions; for a method it points to the object instance.

The **args** argument is a pointer to a Python tuple object containing the arguments. Each item of the tuple corresponds to an argument in the call's argument list.

The function **PyArg_ParseTuple()** in the Python API checks the argument types and converts them to C values. It uses a template string to determine the required tupes of the arguments. If successful, it copies the values to the arguments to the list of pointers provided. This is a pointer assignment.

Since a Python object must be returned, the C integer is converted to a Python integer with **PyLong_FromLong()**. Even integers are objects on the heap in Python.

If you have a C function that returns no useful argument, the corresponding Python function must return **None**. This is implemented by the **Py_RETURN_NONE** macro:

    Py_INCREF(Py_None);
    return Py_None;

To call **spam_system()** from a Python program, we first need to list its name and address in a method table.

    static PyMethodDef SpamMethods[] = {
        ...
        {"system", spam_system, METH_VARARGS, "Execute a shell command."},
        ...,
        {NULL, NULL, 0, NULL} // Sentinel
    };

The **METH_KEYWORDS** bit may be set in the third field if keyword arguments should be passed to the function. In this case, the C function should accept a third **PyObject \*** parameter which will be a dictionary of keywords. Use **PyArg_ParseTupleAndKeywords()** to parse the arguments to such a function.

The method table must be referenced in the module definition structure:

    static struct PyModuleDef spammmodule = {
        PyModuleDef_HEAD_INIT,
        "spam",  // name of module
        spam_doc,  // module docstring
        -1,  // size of per-interpreter state of the module, or -1 if the module keeps state in global variables
        SpamMethods  // method table
    };

This structure must be passed to the interpreter in the module's initialization function. This function must be named **PyInit_*name*()**, where *name* is the name of the module, and should be the only non-**static** item defined in the module file.

    PyMODINIT_FUNC
    PyInit_spam(void)
    {
        return PyModule_Create(&spammmodule);
    }

When the Python program imports the module for the first time, **PyInit_spam()** is called. **PyModule_Create()** returns a module object, and inserts built-in function objects into the newly created module based upon the table found in the module definition.