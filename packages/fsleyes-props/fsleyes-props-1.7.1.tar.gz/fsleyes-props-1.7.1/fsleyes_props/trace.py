#!/usr/bin/env python
#
# trace.py - debugging functions
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides some useful logging/debugging functions.

.. warning:: This module is not intended for general use - it is solely for
             development/debugging purposes. Do not use it unless you know
             know what you are doing.


.. warning:: When this module is imported, it monkey patches the
             :class:`.CallQueue` class in a devious and dangerous manner to
             allow for more informative debug statements.  Therefore it's a
             bad idea to even import this module, unless you really know what
             you are doing.


.. warning:: Just don't import this module, ok?


The functions provided by this module are as follows:

.. autosummary::
   trace
   setcause
   propchange
"""

import            logging
import            inspect
import os.path as op


log = logging.getLogger(__name__)


# If trace debugging is enabled, we're going to
# do some funky stuff to the props callqueue
# object, so we can get some extra information
# in the propchange function.
if log.getEffectiveLevel() == logging.DEBUG:

    log.debug('Monkey-patching fsleyes_props.properties_value.queue instance')

    import fsleyes_props as props

    import queue

    # The problem that I am addressing here is the
    # fact that, when a property value listener is
    # called, the cause of the call (i.e. the point
    # at which the property value was changed) does
    # not necessarily exist in the stack. This is
    # because when a PV instance passes all of its
    # listeners to the CallQueue (CQ) to call, the
    # CQ will queue them immediately, but will not
    # necessarily call them - they are only called
    # if the CQ is not already processing the
    # listeners from another PV change.

    # A single CallQueue instance is shared
    # by all PropertyValue instances to queue/
    # call property value listeners.
    theQ = props.properties_value.PropertyValue.queue


    def tracePop(*args, **kwargs):

        # When the CallQueue calls its _pop
        # method, it will call the returned
        # function. For debugging purposes,
        # we'll pop the associated cause
        # (enqueued in the tracePush function
        # below), so the propchange function
        # can print it out.
        #
        # This will throw Queue.EmptyError if
        # the _causes queue is empty, but
        # that is what the real _pop method
        # does anyway.
        try:    theQ._currentCause = theQ._causes.get_nowait()
        except: theQ._currentCause = None

        return theQ._realPop(*args, **kwargs)


    def tracePush(*args, **kwargs):

        pushed = theQ._realPush(*args, **kwargs)

        # If the real _push method returns False,
        # it means that the function was not enqueued
        if not pushed:
            return False

        frames = inspect.stack()[1:]

        # We search for the first frame in the stack
        # which is not in the props package  - this
        # will be the point of the PV change which
        # caused this listener to be enqueued
        triggerFrame = None
        for frame in frames:
            if 'fsleyes_props' not in frame[1]:
                triggerFrame = frame
                break

        # This should never happen,
        # but in case it does, we
        # put a dummy value into
        # the causes queue, so it
        # is the same length as the
        # reall call queue
        if triggerFrame is None:
            theQ._causes.put_nowait(None)

        # Store the cause of the listener
        # push on the causes queue
        else:

            cause = [triggerFrame[1],
                     triggerFrame[2],
                     triggerFrame[3]]
            if triggerFrame[4] is not None:
                cause.append(triggerFrame[4][triggerFrame[5]])
            else:
                cause.append('<input>')
            theQ._causes.put_nowait(cause)

        return True

    # Patch the CallQueue instance with
    # our push/pop implementations
    theQ._causes          = queue.Queue()
    theQ._realPush        = theQ._CallQueue__push
    theQ._realPop         = theQ._CallQueue__pop
    theQ._CallQueue__push = tracePush
    theQ._CallQueue__pop  = tracePop


def trace(desc):
    """Outputs a log message containing the given description and the current
    stack trace.
    """

    if log.getEffectiveLevel() != logging.DEBUG:
        return

    stack = inspect.stack()[1:]
    lines = '{}\n'.format(desc)

    for i, frame in enumerate(stack):

        srcMod    = frame[1]
        srcLineNo = frame[2]

        if frame[4] is not None: srcLine = frame[4][frame[5]]
        else:                    srcLine = '<native>'

        lines = lines + '{}{}:{}: {}\n'.format(
            ' ' * (i + 1),
            srcMod, srcLineNo,
            srcLine.strip())

    log.debug(lines)

    return lines


def propchange(*args):
    """Intended to be called from a :class:`.PropertyValue` listener
    function.

    If this function is called due to a change, attempts to determine the line
    of code which triggered the change. Prints some informative log messages.

    :arg args: The arguments that were passed to the listener function.
    """


    if log.getEffectiveLevel() != logging.DEBUG:
        return

    import fsleyes_props as props

    theQ  = props.properties_value.PropertyValue.queue
    stack = inspect.stack()

    listenerFile = stack[1][1]
    listenerLine = stack[1][2]
    listenerFunc = stack[1][3]

    triggerFile = None

    if len(args) != 4:
        triggerFile = stack[2][1]
        triggerLine = stack[2][2]
        triggerFunc = stack[2][3]
        triggerSrc  = stack[2][4][stack[2][5]]
    else:
        triggerFile = theQ._currentCause[0]
        triggerLine = theQ._currentCause[1]
        triggerFunc = theQ._currentCause[2]
        triggerSrc  = theQ._currentCause[3]

    if triggerFile is None:
        log.debug('Listener {} ({}:{}) was called '
                  'due to an unknown process'.format(
                      listenerFunc,
                      op.basename(listenerFile),
                      listenerLine))

    else:

        if len(args) != 4:
            reason = 'manually called from'
        else:
            value, valid, ctx, name = args
            reason = 'called due to a value change of {}.{} ({}) at'.format(
                type(ctx).__name__,
                name,
                value)

        log.debug('Listener {} ({}:{}) was {} '
                  '{} ({}:{}:{})'.format(
                      listenerFunc,
                      op.basename(listenerFile),
                      listenerLine,
                      reason,
                      triggerFunc,
                      op.basename(triggerFile),
                      triggerLine,
                      triggerSrc.strip()))


def setcause(desc):
    """I can't quite remember the difference betwen this function and the
    :func:`propchange` function.
    """

    if log.getEffectiveLevel() != logging.DEBUG:
        return

    stack      = inspect.stack()[1:]
    causeFrame = None
    ultCauseFrame = None

    for i, frame in enumerate(stack):

        if 'fsleyes_props' not in frame[1]:
            causeFrame = frame
            break

    if causeFrame is not None:
        for i, frame in reversed(list(enumerate(stack))):
            if 'fsleyes_props' in frame[1]:
                ultCauseFrame = stack[i + 1]
                break

    if causeFrame is None:
        log.debug('{}: Unknown cause'.format(desc))
    else:
        causeFile = causeFrame[1]
        causeLine = causeFrame[2]
        causeFunc = causeFrame[3]
        causeSrc  = causeFrame[4][causeFrame[5]]

        line = '{}: Caused by {} ({}:{}:{})'.format(
            desc,
            causeFunc,
            op.basename(causeFile),
            causeLine,
            causeSrc.strip())

        if ultCauseFrame is not None:

            causeFile = ultCauseFrame[1]
            causeLine = ultCauseFrame[2]
            causeFunc = ultCauseFrame[3]
            causeSrc  = ultCauseFrame[4][ultCauseFrame[5]]
            line = '{} (ultimately caused by {} ({}:{}:{})'.format(
                line,
                causeFunc,
                op.basename(causeFile),
                causeLine,
                causeSrc.strip())

        log.debug(line)
