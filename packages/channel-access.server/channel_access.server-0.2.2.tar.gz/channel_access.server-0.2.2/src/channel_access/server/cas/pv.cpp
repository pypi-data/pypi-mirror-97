#include "pv.hpp"

#include <memory>
#include <Python.h>
#include <structmember.h>
#include <casdef.h>
#include <gddApps.h>

#include "cas.hpp"
#include "convert.hpp"
#include "async.hpp"

namespace cas {
namespace {

class PvProxy;
struct Pv {
    PyObject_HEAD
    char* name;
    bool held_by_server;
    char use_numpy;
    std::unique_ptr<PvProxy> proxy;
};
static_assert(std::is_standard_layout<Pv>::value, "Pv has to be standard layout to work with the Python API");


class PvProxy : public casPV {
public:
    PvProxy(PyObject* pv)
        : pv{pv}
    {
        // No GIL, don't use the python API
    }

    static PyObject* name(PyObject* self, PyObject*)
    {
        return Py_BuildValue("y", reinterpret_cast<Pv*>(self)->name);
    }

    char const* getName() const override
    {
        return reinterpret_cast<Pv*>(pv)->name;
    }

    virtual void destroy() override
    {
        Pv* pv_struct = reinterpret_cast<Pv*>(pv);

        PyGILState_STATE gstate = PyGILState_Ensure();
            PyObject* fn = PyObject_GetAttrString(pv, "destroy");
            if (fn) {
                PyObject* result = PyObject_CallFunction(fn, nullptr);
                if (PyErr_Occurred()) {
                    PyErr_WriteUnraisable(fn);
                    PyErr_Clear();
                }

                Py_DECREF(fn);
                Py_XDECREF(result);
            }

            if (PyErr_Occurred()) {
                PyErr_WriteUnraisable(pv);
                PyErr_Clear();
            }

            // the caServer released its ownership so we have to decrement the python reference count
            if (pv_struct->held_by_server) {
                pv_struct->held_by_server = false;
                Py_DECREF(pv);
            }
        PyGILState_Release(gstate);
    }

    static PyObject* destroy(PyObject* self, PyObject*)
    {
        Py_RETURN_NONE;
    }

    virtual aitEnum bestExternalType() const override
    {
        aitEnum ret = aitEnumString;
        PyGILState_STATE gstate = PyGILState_Ensure();
            PyObject* fn = PyObject_GetAttrString(pv, "type");
            if (fn) {
                PyObject* result = PyObject_CallFunction(fn, nullptr);
                if (PyErr_Occurred()) {
                    PyErr_WriteUnraisable(fn);
                    PyErr_Clear();
                }
                Py_DECREF(fn);

                if (result) {
                    to_ait_enum(result, ret);
                    Py_DECREF(result);
                }
            }

            if (PyErr_Occurred()) {
                PyErr_WriteUnraisable(pv);
                PyErr_Clear();
            }
        PyGILState_Release(gstate);
        return ret;
    }

    static PyObject* type(PyObject* self, PyObject*)
    {
        return PyObject_GetAttrString(cas::enum_type, "STRING");
    }

    virtual unsigned maxDimension() const override
    {
        unsigned ret = 0;
        PyGILState_STATE gstate = PyGILState_Ensure();
            PyObject* fn = PyObject_GetAttrString(pv, "count");
            if (fn) {
                PyObject* result = PyObject_CallFunction(fn, nullptr);
                if (PyErr_Occurred()) {
                    PyErr_WriteUnraisable(fn);
                    PyErr_Clear();
                }
                Py_DECREF(fn);

                if (PyLong_Check(result)) {
                    ret = 1;
                }
                Py_XDECREF(result);
            }

            if (PyErr_Occurred()) {
                PyErr_WriteUnraisable(pv);
                PyErr_Clear();
            }
        PyGILState_Release(gstate);
        return ret;
    }

    virtual aitIndex maxBound(unsigned dimension) const override
    {
        aitIndex ret = 0;
        PyGILState_STATE gstate = PyGILState_Ensure();
            PyObject* fn = PyObject_GetAttrString(pv, "count");
            if (fn) {
                PyObject* result = PyObject_CallFunction(fn, nullptr);
                if (PyErr_Occurred()) {
                    PyErr_WriteUnraisable(fn);
                    PyErr_Clear();
                }
                Py_DECREF(fn);

                if (result) {
                    aitIndex bound = PyLong_AsLong(result);
                    if (not PyErr_Occurred()) {
                        ret = bound;
                    }

                    Py_DECREF(result);
                }
            }

            if (PyErr_Occurred()) {
                PyErr_WriteUnraisable(pv);
                PyErr_Clear();
            }
        PyGILState_Release(gstate);
        return ret;
    }

    static PyObject* count(PyObject* self, PyObject*)
    {
        Py_RETURN_NONE;
    }

    virtual caStatus read(casCtx const& ctx, gdd& prototype) override
    {
        aitEnum type = aitEnumInvalid;
        caStatus ret = S_casApp_noSupport;
        PyGILState_STATE gstate = PyGILState_Ensure();
            {
                PyObject* fn = PyObject_GetAttrString(pv, "type");
                if (fn) {
                    PyObject* result = PyObject_CallFunction(fn, nullptr);
                    if (PyErr_Occurred()) {
                        PyErr_WriteUnraisable(fn);
                        PyErr_Clear();
                    }
                    Py_DECREF(fn);

                    if (result) {
                        to_ait_enum(result, type);
                        Py_DECREF(result);
                    }
                }
            }

            if (type != aitEnumInvalid) {
                PyObject* fn = PyObject_GetAttrString(pv, "read");
                if (fn) {
                    PyObject* result = PyObject_CallFunction(fn, "(N)",
                        create_async_context(ctx, &prototype, type));
                    if (PyErr_Occurred()) {
                        PyErr_WriteUnraisable(fn);
                        PyErr_Clear();
                    }
                    Py_DECREF(fn);

                    if (result and result != Py_None) {
                        if (give_async_read_to_server(result)) {
                            ret = S_casApp_asyncCompletion;
                        } else if (to_gdd(result, type, prototype)) {
                            ret = S_casApp_success;
                        }
                        Py_DECREF(result);
                    }
                }
            }

            if (PyErr_Occurred()) {
                PyErr_WriteUnraisable(pv);
                PyErr_Clear();
            }
        PyGILState_Release(gstate);
        return ret;
    }

    static PyObject* read(PyObject* self, PyObject*)
    {
        Py_RETURN_NONE;
    }

    virtual caStatus write(casCtx const& ctx, gdd const& value) override
    {
        Pv* pv_struct = reinterpret_cast<Pv*>(pv);

        caStatus ret = S_casApp_noSupport;
        PyGILState_STATE gstate = PyGILState_Ensure();
            PyObject* fn = PyObject_GetAttrString(pv, "write");
            if (fn) {
                PyObject* value_timestamp = from_gdd(value, pv_struct->use_numpy);
                if (value_timestamp) {
                    PyObject* result = PyObject_CallFunction(fn, "(OON)",
                        PyTuple_GET_ITEM(value_timestamp, 0),
                        PyTuple_GET_ITEM(value_timestamp, 1),
                        create_async_context(ctx, nullptr, aitEnumInvalid));
                    if (PyErr_Occurred()) {
                        PyErr_WriteUnraisable(fn);
                        PyErr_Clear();
                    }
                    Py_DECREF(value_timestamp);

                    if (result) {
                        if (give_async_write_to_server(result)) {
                            ret = S_casApp_asyncCompletion;
                        } else if (PyObject_IsTrue(result)) {
                            ret = S_casApp_success;
                        }
                        Py_DECREF(result);
                    }
                }
                Py_DECREF(fn);
            }

            if (PyErr_Occurred()) {
                PyErr_WriteUnraisable(pv);
                PyErr_Clear();
            }
        PyGILState_Release(gstate);
        return ret;
    }

    static PyObject* write(PyObject* self, PyObject* args)
    {
        Py_RETURN_FALSE;
    }

    static PyObject* postEvent(PyObject* self, PyObject* args)
    {
        PvProxy* proxy = reinterpret_cast<Pv*>(self)->proxy.get();
        PyObject* py_events = nullptr, *py_values = nullptr;

        if (not PyArg_ParseTuple(args, "OO", &py_events, &py_values)) return nullptr;


        PyObject* fn = PyObject_GetAttrString(proxy->pv, "type");
        if (not fn) return nullptr;

        PyObject* result = PyObject_CallFunction(fn, nullptr);
        Py_DECREF(fn);
        if (not result) return nullptr;

        aitEnum type = aitEnumInvalid;
        bool success = to_ait_enum(result, type);
        Py_DECREF(result);
        if (not success) return nullptr;

        if (type == aitEnumInvalid) {
            PyErr_SetString(PyExc_RuntimeError, "Invalid pv type");
            return nullptr;
        }


        caServer const* server;
        Py_BEGIN_ALLOW_THREADS
            server = static_cast<casPV*>(proxy)->getCAS();
        Py_END_ALLOW_THREADS
        if (not server) {
            // not installed into a server, do nothing
            Py_RETURN_NONE;
        }

        casEventMask mask;
        if (not to_event_mask(py_events, mask, *server)) return nullptr;

        auto* values = new gdd{gddAppType_value};
        if (not to_gdd(py_values, type, *values)) {
            values->unreference();
            return nullptr;
        }

        try {
            Py_BEGIN_ALLOW_THREADS
                static_cast<casPV*>(proxy)->postEvent(mask, *values);
            Py_END_ALLOW_THREADS
        } catch (...) {
            values->unreference();
            PyErr_SetString(PyExc_RuntimeError, "Could not post events");
            return nullptr;
        }
        values->unreference();

        Py_RETURN_NONE;
    }

    virtual caStatus interestRegister() override
    {
        caStatus ret = S_casApp_noSupport;
        PyGILState_STATE gstate = PyGILState_Ensure();
            PyObject* fn = PyObject_GetAttrString(pv, "interestRegister");
            if (fn) {
                PyObject* result = PyObject_CallFunction(fn, nullptr);
                if (PyErr_Occurred()) {
                    PyErr_WriteUnraisable(fn);
                    PyErr_Clear();
                }
                Py_DECREF(fn);

                if (result) {
                    if (PyObject_IsTrue(result)) {
                        ret = S_casApp_success;
                    }
                    Py_DECREF(result);
                }
            }

            if (PyErr_Occurred()) {
                PyErr_WriteUnraisable(pv);
                PyErr_Clear();
            }
        PyGILState_Release(gstate);
        return ret;
    }

    static PyObject* interestRegister(PyObject* self, PyObject*)
    {
        Py_RETURN_FALSE;
    }

    virtual void interestDelete() override
    {
        PyGILState_STATE gstate = PyGILState_Ensure();
            PyObject* fn = PyObject_GetAttrString(pv, "interestDelete");
            if (fn) {
                PyObject* result = PyObject_CallFunction(fn, nullptr);
                Py_XDECREF(result);

                if (PyErr_Occurred()) {
                    PyErr_WriteUnraisable(fn);
                    PyErr_Clear();
                }
                Py_DECREF(fn);
            }

            if (PyErr_Occurred()) {
                PyErr_WriteUnraisable(pv);
                PyErr_Clear();
            }
        PyGILState_Release(gstate);
    }

    static PyObject* interestDelete(PyObject* self, PyObject*)
    {
        Py_RETURN_NONE;
    }

private:
    PyObject* pv;
};


int pv_init(PyObject* self, PyObject* args, PyObject*)
{
    Pv* pv = reinterpret_cast<Pv*>(self);

    char const *c_name;
    int numpy = false;
    if (not PyArg_ParseTuple(args, "y|p", &c_name, &numpy)) return -1;

    pv->name = strdup(c_name);
    pv->held_by_server = false;
    pv->use_numpy = numpy;
    return 0;
}

void pv_dealloc(PyObject* self)
{
    Pv* pv = reinterpret_cast<Pv*>(self);

    free(pv->name);
    Py_BEGIN_ALLOW_THREADS
        pv->proxy.reset();
    Py_END_ALLOW_THREADS

    Py_TYPE(self)->tp_free(self);
}

PyObject* pv_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    PyObject* self = type->tp_alloc(type, 0);
    if (not self) return nullptr;

    Pv* pv = reinterpret_cast<Pv*>(self);
    Py_BEGIN_ALLOW_THREADS
        pv->proxy.reset(new PvProxy(self));
    Py_END_ALLOW_THREADS
    return self;
}

// we can't put these inside the PvProxy class
PyDoc_STRVAR(name__doc__, R"(name()

Return the name of the PV. This is the name used on-the-wire, possible
encoded with some text encoding.

This method is thread-safe.

Returns:
    bytes: The name of the PV given at initialization.
)");
PyDoc_STRVAR(destroy__doc__, R"(destroy()

Destroy the PV.

Request from the server when the PV handler object is no longer
needed.

This is called from an unspecified thread.
)");
PyDoc_STRVAR(type__doc__, R"(type()

Return the type of the PV.

This is called from the server when the PV type is needed.

This is called from an unspecified thread.

Returns:
    :class:`channel_access.common.Type`: Type of the PV.
)");
PyDoc_STRVAR(count__doc__, R"(count()

Return the number of elements.

This is called from the server when the number of elements is needed for
an array pv.
Return ``None`` for a scalar PV.

This is called from an unspecified thread.

Returns:
    int: Number of elements for an array or ``None`` for a scalar.
)");
PyDoc_STRVAR(read__doc__, R"(read(context)

Retreive the attributes of the PV.

This is called from the server when a get request is processed.

This is called from an unspecified thread.

Args:
    context: A context object needed to create an :class:`AsyncRead` object.

Returns:
    dict: An attributes dictionary with all PV attributes.
)");
PyDoc_STRVAR(write__doc__, R"(write(value, timestamp, context)

Set the value of the PV.

This is called from the server when a put request is processed.

This is called from an unspecified thread.

Args:
    value: The new value. The type depends on the PV type.
    timestamp: An epics timestamp tuple.
    context: A context object needed to create an :class:`AsyncWrite` object.

Returns:
    bool: ``True`` if the write was successful, ``False`` otherwise.
)");
PyDoc_STRVAR(postEvent__doc__, R"(postEvent(event_mask, attributes)

Post events to clients.

This should be called when any attributes change and events are requested
(:meth:`interestRegister()`). Depending on which attributes changed the
``event_mask`` should be set accordingly.

This method is thread-safe.

Args:
    event_mask (:class:`channel_access.common.Events`): This mask describes
        the events to post.
    attributes (dict): An attribute dictionary with the attribute values for the events.

)");
PyDoc_STRVAR(interestRegister__doc__, R"(interestRegister()

Request to inform the server about changes.

Request from the server that events should be posted
when attributes change, see :meth:`postEvents()`.

This is called from an unspecified thread.

Returns:
    bool: ``True`` if the request was successful, ``False`` otherwise.
)");
PyDoc_STRVAR(interestDelete__doc__, R"(interestDelete()

Don't inform server about changes any more.

Request from the server that events should not be posted any more
when attributes change.

This is called from an unspecified thread.
)");

PyMethodDef pv_methods[] = {
    {"name",             static_cast<PyCFunction>(PvProxy::name),             METH_NOARGS,  name__doc__},
    {"destroy",          static_cast<PyCFunction>(PvProxy::destroy),          METH_NOARGS,  destroy__doc__},
    {"type",             static_cast<PyCFunction>(PvProxy::type),             METH_NOARGS,  type__doc__},
    {"count",            static_cast<PyCFunction>(PvProxy::count),            METH_NOARGS,  count__doc__},
    {"read",             static_cast<PyCFunction>(PvProxy::read),             METH_NOARGS,  read__doc__},
    {"write",            static_cast<PyCFunction>(PvProxy::write),            METH_VARARGS, write__doc__},
    {"postEvent",        static_cast<PyCFunction>(PvProxy::postEvent),        METH_VARARGS, postEvent__doc__},
    {"interestRegister", static_cast<PyCFunction>(PvProxy::interestRegister), METH_NOARGS,  interestRegister__doc__},
    {"interestDelete",   static_cast<PyCFunction>(PvProxy::interestDelete),   METH_NOARGS,  interestDelete__doc__},
    {nullptr}
};

PyDoc_STRVAR(use_numpy__doc__, R"(use_numpy

bool: ``True`` if numpy arrays are used, ``False`` otherwise.

This can be changed any time. For any new request the new value is used
when processing the value attribute.
)");
PyMemberDef pv_members[] = {
    {"use_numpy",  T_BOOL,   offsetof(Pv, use_numpy), 0, use_numpy__doc__},
    {nullptr}
};

PyDoc_STRVAR(pv__doc__, R"(PV(name)
PV handler class.

A user defined class should derive from this class and override
the appropiate methods to inform the server about the properties
of the PV and handle requests for it. The default implementations
represent a scalar string PV which rejects all read/write access.

Care must be taken when implementing the methods because they are
called from unspecified threads and must be thread-safe.

The following keys can occur in an attributes dictionary:

    value
        Data value, type depends on the PV type. For integer types
        and enum types this is ``int``, for floating point types this
        is ``float``. For string types this is ``bytes``.
        For arrays this is a sequence of the corresponding values.

    status
        Value status, one of :class:`channel_access.common.Status`.

    severity
        Value severity, one of :class:`channel_access.common.Severity`.

    timestamp
        An epics timestamp tuple corresponding to the last time the
        value changed.

        See also: :meth:`channel_access.common.datetime_to_epics` and
        :meth:`channel_access.common.epics_to_datetime`.

    enum_strings
        Tuple with the strings corresponding to the enumeration values.
        The length of the tuple must be equal to :meth:``PV.count()``.
        The entries are ``bytes``.
        This is only used for enum PVs.

    unit
        String representing the physical unit of the value. The type is
        ``bytes``.
        This is only used for numerical PVs.

    precision
        Integer representing the number of relevant decimal places.
        This is only used for floating point PVs.

    display_limits
        A tuple ``(minimum, maximum)`` representing the range of values
        for a user interface.
        This is only used for numerical PVs.

    control_limits
        A tuple ``(minimum, maximum)`` representing the range of values
        accepted for a put request by the server.
        This is only used for numerical PVs.

    warning_limits
        A tuple ``(minimum, maximum)``. When any value lies outside of the
        range this is a warning condition.
        Typically the status becomes :class:`channel_access.common.Status.LOW` or :class:`channel_access.common.Status.HIGH`.
        This is only used for numerical PVs.

    alarm_limits
        A tuple ``(minimum, maximum)``. When any value lies outside of the
        range this is an alarm condition.
        Typically the status becomes :class:`channel_access.common.Status.LOLO` or :class:`channel_access.common.Status.HIHI`.
        This is only used for numerical PVs.

Args:
    name (bytes): The cannocial name of the PV. If a server serves the
        same PV under different names (aliases), this should be the
        main name.
)");
PyTypeObject pv_type = {
    PyVarObject_HEAD_INIT(nullptr, 0)
    "ca_server.cas.PV",                        /* tp_name */
    sizeof(Pv),                                /* tp_basicsize */
    0,                                         /* tp_itemsize */
    pv_dealloc,                                /* tp_dealloc */
    0,                                         /* tp_vectorcall_offset */
    nullptr,                                   /* tp_getattr */
    nullptr,                                   /* tp_setattr */
    nullptr,                                   /* tp_as_async */
    nullptr,                                   /* tp_repr */
    nullptr,                                   /* tp_as_number */
    nullptr,                                   /* tp_as_sequence */
    nullptr,                                   /* tp_as_mapping */
    nullptr,                                   /* tp_hash */
    nullptr,                                   /* tp_call */
    nullptr,                                   /* tp_str */
    nullptr,                                   /* tp_getattro */
    nullptr,                                   /* tp_setattro */
    nullptr,                                   /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,  /* tp_flags */
    pv__doc__,                                 /* tp_doc */
    nullptr,                                   /* tp_traverse */
    nullptr,                                   /* tp_clear */
    nullptr,                                   /* tp_richcompare */
    0,                                         /* tp_weaklistoffset */
    nullptr,                                   /* tp_iter */
    nullptr,                                   /* tp_iternext */
    pv_methods,                                /* tp_methods */
    pv_members,                                /* tp_members */
    nullptr,                                   /* tp_getset */
    nullptr,                                   /* tp_base */
    nullptr,                                   /* tp_dict */
    nullptr,                                   /* tp_descr_get */
    nullptr,                                   /* tp_descr_set */
    0,                                         /* tp_dictoffset */
    pv_init,                                   /* tp_init */
    nullptr,                                   /* tp_alloc */
    pv_new,                                    /* tp_new */
};

}

PyObject* create_pv_type()
{
    if (PyType_Ready(&pv_type) < 0) return nullptr;

    Py_INCREF(&pv_type);
    return reinterpret_cast<PyObject*>(&pv_type);
}

void destroy_pv_type()
{
    Py_DECREF(&pv_type);
}

casPV* give_to_server(PyObject* obj) {
    switch (PyObject_IsInstance(obj, reinterpret_cast<PyObject*>(&pv_type))) {
        case 1:
            break;
        case 0:
            PyErr_SetString(PyExc_TypeError, "Return value must be a PV instance");
        default:
            return nullptr;
    }

    Pv* pv = reinterpret_cast<Pv*>(obj);
    if (not pv->held_by_server) {
        Py_INCREF(obj);
        pv->held_by_server = true;
    }
    return pv->proxy.get();
}


}
