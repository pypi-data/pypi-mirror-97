Thread related convenience classes and functions.

*Latest release 20210306*:
bg: include the current Pfx prefix in the thread name and thread body Pfx, obsoletes cs.pfx.PfxThread.

## Class `AdjustableSemaphore`

A semaphore whose value may be tuned after instantiation.

### Method `AdjustableSemaphore.acquire(self, blocking=True)`

The acquire() method calls the base acquire() method if not blocking.
If blocking is true, the base acquire() is called inside a lock to
avoid competing with a reducing adjust().

### Method `AdjustableSemaphore.adjust(self, newvalue)`

Set capacity to `newvalue`
by calling release() or acquire() an appropriate number of times.

If `newvalue` lowers the semaphore capacity then adjust()
may block until the overcapacity is released.

### Method `AdjustableSemaphore.adjust_delta(self, delta)`

Adjust capacity by `delta` by calling release() or acquire()
an appropriate number of times.

If `delta` lowers the semaphore capacity then adjust() may block
until the overcapacity is released.

### Method `AdjustableSemaphore.release(self)`

Release the semaphore.

## Function `bg(func, daemon=None, name=None, no_start=False, no_logexc=False, args=None, kwargs=None)`

Dispatch the callable `func` in its own `Thread`;
return the `Thread`.

Parameters:
* `func`: a callable for the `Thread` target.
* `daemon`: optional argument specifying the `.daemon` attribute.
* `name`: optional argument specifying the `Thread` name,
  default: the name of `func`.
* `no_logexc`: if false (default `False`), wrap `func` in `@logexc`.
* `no_start`: optional argument, default `False`.
  If true, do not start the `Thread`.
* `args`, `kwargs`: passed to the `Thread` constructor

## Class `LockableMixin`

Trite mixin to control access to an object via its `._lock` attribute.
Exposes the `._lock` as the property `.lock`.
Presents a context manager interface for obtaining an object's lock.

### Property `LockableMixin.lock`

Return the lock.

## Function `locked(*da, **dkw)`

A decorator for instance methods that must run within a lock.

Decorator keyword arguments:
* `initial_timeout`:
  the initial lock attempt timeout;
  if this is `>0` and exceeded a warning is issued
  and then an indefinite attempt is made.
  Default: `2.0`s
* `lockattr`:
  the name of the attribute of `self`
  which references the lock object.
  Default `'_lock'`

## Function `locked_property(*da, **dkw)`

A thread safe property whose value is cached.
The lock is taken if the value needs to computed.

The default lock attribute is `._lock`.
The default attribute for the cached value is `._`*funcname*
where *funcname* is `func.__name__`.
The default "unset" value for the cache is `None`.

## Function `monitor(*da, **dkw)`

Turn a class into a monitor, all of whose public methods are `@locked`.

This is a simple approach requires class instances to have a `._lock`
which is an `RLock` or compatible
because methods may naively call each other.

Parameters:
* `attrs`: optional iterable of attribute names to wrap in `@locked`.
  If omitted, all names commencing with a letter are chosen.
* `initial_timeout`: optional initial lock timeout, default `10.0`s.
* `lockattr`: optional lock attribute name, default `'_lock'`.

Only attributes satifying `inspect.ismethod` are wrapped
because `@locked` requires access to the instance `._lock` attribute.

## Class `PriorityLock`

A priority based mutex which is acquired by and released to waiters
in priority order.

The initialiser sets a default priority, itself defaulting to `0`.

The `acquire()` method accepts an optional `priority` value
which specifies the priority of the acquire request;
lower values have higher priorities.
`acquire` returns a new `PriorityLockSubLock`.

Note that internally this allocates a `threading.Lock` per acquirer.

When `acquire` is called, if the `PriorityLock` is taken
then the acquirer blocks on their personal `Lock`.

When `release()` is called the highest priority `Lock` is released.

Within a priority level `acquire`s are served in FIFO order.

Used as a context manager, the mutex is obtained at the default priority.
The `priority()` method offers a context manager
with a specified priority.
Both context managers return the `PriorityLockSubLock`
allocated by the `acquire`.

### Method `PriorityLock.__init__(self, default_priority=0, name=None)`

Initialise the `PriorityLock`.

Parameters:
* `default_priority`: the default `acquire` priority,
  default `0`.
* `name`: optional identifying name

### Method `PriorityLock.__enter__(self)`

Enter the mutex as a context manager at the default priority.
Returns the new `Lock`.

### Method `PriorityLock.__exit__(self, *_)`

Exit the context manager.

### Method `PriorityLock.acquire(self, priority=None)`

Acquire the mutex with `priority` (default from `default_priority`).
Return the new `PriorityLockSubLock`.

This blocks behind any higher priority `acquire`s
or any earlier `acquire`s of the same priority.

### Method `PriorityLock.priority(self, this_priority)`

A context manager with the specified `this_priority`.
Returns the new `Lock`.

### Method `PriorityLock.release(self)`

Release the mutex.

Internally, this releases the highest priority `Lock`,
allowing that `acquire`r to go forward.

## Class `PriorityLockSubLock(PriorityLockSubLock,builtins.tuple)`

The record for the per-`acquire`r `Lock` held by `PriorityLock.acquire`.

## Class `State(_thread._local)`

A `Thread` local object with attributes
which can be used as a context manager to stack attribute values.

Example:

    from cs.threads import State

    S = State(verbose=False)

    with S(verbose=True) as prev_attrs:
        if S.verbose:
            print("verbose! (formerly verbose=%s)" % prev_attrs['verbose'])

### Method `State.__init__(self, **kw)`

Initiale the `State`, providing the per-Thread initial values.

### Method `State.__call__(self, **kw)`

Calling a `State` returns a context manager which stacks some state.
The context manager yields the previous values
for the attributes which were stacked.

## Function `via(cmanager, func, *a, **kw)`

Return a callable that calls the supplied `func` inside a
with statement using the context manager `cmanager`.
This intended use case is aimed at deferred function calls.

## Class `WorkerThreadPool(cs.resources.MultiOpenMixin)`

A pool of worker threads to run functions.

### Method `WorkerThreadPool.__init__(self, name=None, max_spare=4)`

Initialise the WorkerThreadPool.

Parameters:
* `name`: optional name for the pool
* `max_spare`: maximum size of each idle pool (daemon and non-daemon)

### Method `WorkerThreadPool.dispatch(self, *a, **kw)`

Wrapper function to check that this instance is not closed.

### Method `WorkerThreadPool.join(self)`

Wait for all outstanding Threads to complete.

### Method `WorkerThreadPool.shutdown(self)`

Shut down the pool.

Close all the request queues.

Note: does not wait for all Threads to complete; call .join after close.

### Method `WorkerThreadPool.startup(self)`

Start the pool.

## Class `WTPoolEntry(builtins.tuple)`

WTPoolEntry(thread, queue)

### Property `WTPoolEntry.queue`

Alias for field number 1

### Property `WTPoolEntry.thread`

Alias for field number 0

# Release Log



*Release 20210306*:
bg: include the current Pfx prefix in the thread name and thread body Pfx, obsoletes cs.pfx.PfxThread.

*Release 20210123*:
New @monitor class decorator for simple RLock based reentrance protection.

*Release 20201025*:
* @locked: bump the default warning timeout to 10s, was firing too often.
* New State class for thread local state objects with default attribute values and a stacking __call__ context manager.

*Release 20200718*:
@locked: apply the interior __doc__ to the wrapper.

*Release 20200521*:
@locked_property: decorate with @cs.deco.decorator to support keyword arguments.

*Release 20191102*:
@locked: report slow-to-acquire locks, add initial_timeout and lockattr decorator keyword parameters.

*Release 20190923.2*:
Fix annoying docstring typo.

*Release 20190923.1*:
Docstring updates.

*Release 20190923*:
Remove dependence on cs.obj.

*Release 20190921*:
New PriorityLock class for a mutex which releases in (priority,fifo) order.

*Release 20190812*:
bg: compute default name before wrapping `func` in @logexc.

*Release 20190729*:
bg: provide default `name`, run callable inside Pfx, add optional no_logexc=False param preventing @logec wrapper if true.

*Release 20190422*:
bg(): new optional `no_start=False` keyword argument, preventing Thread.start if true

*Release 20190102*:
* Drop some unused classes.
* New LockableMixin, presenting a context manager and a .lock property.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
* Replace bare "excepts" with "except BaseException".
* Doc updates. Other minor improvements.

*Release 20150115*:
First PyPI release.
