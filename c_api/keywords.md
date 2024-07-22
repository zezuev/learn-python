# Keyword Parameters for Extension Functions
The **PyArg_ParseTupleAndKeywords()** function is declared as follows:

    int PyArg_ParseTupleAndKeywords(PyObject *arg, PyObject *kwdict, const char *format, char *kwlist[], ...);

The *arg* and *format* parameters are identical to those of the **PyArg_ParseTuple()** function. The *kwdict* parameter is the dictionary of keywords received as the third parameter from the Python runtime. The *kwlist* is a **NULL**-terminated list of strings which identify the parameters; the names are matched with the type information from *format* from left to right. Keywords parameters passed in which are not present in the *kwlist* will cause **TypeError** to be raised.

    static PyObject *
    keywdarg_parrot(PyObject *self, PyObject, *args, PyObject *keywds)
    {
        int voltage;
        const char *state = "a stiff";
        const char *action = "voom";
        const char *type = "Norwegian Blue";

        static char *kwlist[] = {"voltage", "state", "action", "type", NULL};

        if (!PyArg_ParseTupleAndKeywords(args, keywds, "i|sss", kwlist, &voltage, &state, &action, &type))
            return NULL;
        
        printf("-- This parrot wouldn't %s if you put %i Volks through it.\n", action, voltage);
        printf("-- Lovely plumage, the %s -- It's %s\n", type, state);

        Py_RETURN_NONE;
    }

    static PyMethodDef keywdarg_methods[] = {
        // the cast of the function is necessary since PyCFunction values only take two PyObject* parameters, and keywdarg_parrot() takes three
        {"parrot", (PyCFunction)(void(*)(void))keywdarg_parrot, METH_VARARGS | METH_KEYWORDS, "Print a lovely skit to standard output."},
        {NULL, NULL, 0, NULL} // sentinel
    };

    static struct PyModuleDef keywdargmodule = {
        PyModuleDef_HEAD_INIT,
        "keywdarg",
        NULL,
        -1,
        keywdarg_methods,
    };

    PyMODINIT_FUNC
    PyInit_keywdarg(void)
    {
        return PyModule_Create(&keywdargmodule);
    }