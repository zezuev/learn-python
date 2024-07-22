# Errors and Exceptions
When a function fails, it should set an exception condition and return an error value.

Exception information is stored in three members of the interpreter's thread state. These are **NULL** if there is no exception. Otherwise they are the C equivalents of the members of the Pythn tuple returned by **sys.exc_info()**. These are the exception type, exception instance, and a traceback object.

The most common function to set an exception is **PyErr_SetString()**. Its arguments are an exception object and a C string. The exception object is usually a predefined object like **PyExc_ZeroDivisionError**. The C string indicates the cause of the error and is converted to a Python string object and stored as the associated value of the exception.

You can test non-destructively whether an exception has been set with **PyErr_Occurred()**. This returns the current exception object, or **NULL** if no exception has occurred.

When a function *f* that calls another function *g* detects that the latter fails, *f* should itself return an error value. It should not call one of the **PyErr_\*** functions. Once the error reaches the Python interpreter's main loop, this aborts the currently executing Python code and tries to find an exception handler specified by the Python programmer.

To ignore an exception set by a function call that failed, the exception condition must be cleared explicitly with **PyErr_Clear()**.

Every failing **malloc()** or **realloc()** must be turned into an exception. The direct caller must call **PyErr_NoMemory()** and return a failure indicator.

Be careful to clean up garbage by making **Py_XDECREF()** or **Py_DECREF()** calls for objects you have already created when you return an error indicator.

There are predeclared C objects corresponding to all built-in Python exceptions. You can also define a new exception that is unique to your module. For this, you usually declare a static object variable at the beginning of your file:

    static PyObject *SpamError;

And initialize it in your module's initialization function with an exception object:

    PyMODINIT_FUNC
    PyInit_spam(void)
    {
        PyObject *m;

        m = PyModule_Create(&spammodule);
        if (m == NULL)
            return NULL;
        
        SpamError = PyErr_NewException("spam.error", NULL, NULL);
        Py_XINCREF(SpamError);
        if (PyModule_AddObject(m, "error", SpamError) < 0) {
            Py_XDECREF(SpamError);
            Py_CLEAR(SpamError);
            Py_DECREF(m);
            return NULL;
        }

        return m;
    }

You can then raise it in your extension module as follows:

    static PyObject *
    spam_system(PyObject *self, PyObject *args)
    {
        const char *command;
        int sts;

        if (!PyArg_ParseTuple(args, "s", &command))
            return NULL;
        sts = system(command);
        if (sts < 0) {
            PyErr_SetString(SpamError, "System command failed");
            return NULL;
        }
        return PyLong_FromLong(sts);
    }