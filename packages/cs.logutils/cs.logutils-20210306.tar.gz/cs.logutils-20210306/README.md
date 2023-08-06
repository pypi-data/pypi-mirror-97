Logging convenience routines.

*Latest release 20210306*:
* Default logging level for ttys is now INFO, not STATUS.
* New VERBOSE level below INFO but above DEBUG.
* infer_logging_level: if verbose unspecified, logging=WARNING on a tty and TRACK otherwise, else if verbose, level=VERBOSE, otherwise WARNING.
* Include .verbose in the loginfo.
* New verbose() and ifverbose().

The logging package is very useful, but a little painful to use.
This package provides low impact logging setup and some extremely
useful if unconventional context hooks for logging.

The default logging verbosity output format has different defaults
based on whether an output log file is a tty
and whether the environment variable `$DEBUG` is set, and to what.

On terminals warnings and errors get ANSI colouring.

A mode is available that uses `cs.upd` for certain log levels.

Log messages dispatched via `warning` and friends from this module
are automatically prefixed with the current `cs.pfx` prefix string,
providing automatic message context.

Some examples:
--------------

Program initialisation:

    from cs.logutils import setup_logging

    def main(argv):
        cmd = os.path.basename(argv.pop(0))
        setup_logging(cmd)

Basic logging from anywhere:

    from cs.logutils import info, warning, error
    [...]
    def some_function(...):
        [...]
        error("nastiness found! bad value=%r", bad_value)

## Function `add_logfile(filename, logger=None, mode='a', encoding=None, delay=False, format=None, no_prefix=False)`

Add a `FileHandler` logging to the specified `filename`;
return the chosen logger and the new handler.

Parameters:
* `logger`: if supplied and not `None`, add the `FileHandler` to that
  `Logger`, otherwise to the root Logger. If `logger` is a string, call
  `logging.getLogger(logger)` to obtain the logger.
* `mode`, `encoding` and `delay`: passed to the `FileHandler`
  initialiser.
* `format`: used to override the handler's default format.
* `no_prefix`: if true, do not put the `Pfx` context onto the front of the message.

## Function `critical(*a, **kw)`

Emit a log at `logging.CRITICAL` level with the current `Pfx` prefix.

## Function `D(msg, *args)`

Print formatted debug string straight to `sys.stderr` if
`D_mode` is true, bypassing the logging modules entirely.
A quick'n'dirty debug tool.

## Function `debug(*a, **kw)`

Emit a log at `logging.DEBUG` level with the current `Pfx` prefix.

## Function `error(*a, **kw)`

Emit a log at `logging.ERROR` level with the current `Pfx` prefix.

## Function `exception(msg, *args, **kwargs)`

Emit an exception log with the current `Pfx` prefix.

## Function `ftrace(func)`

Decorator to trace a function if `__module__.DEBUG` is true.

## Function `ifdebug()`

Test the `loginfo.level` against `logging.DEBUG`.

## Function `ifverbose(*a, **kw)`

Conditionally log a message.

If `is_verbose` is `None`, log at `VERBOSE` level and rely on the logging setup.
Otherwise, if `is_verbose` is true, log at `INFO` level.

## Function `infer_logging_level(env_debug=None, environ=None, verbose=None)`

Infer a logging level from the `env_debug`, which by default
comes from the environment variable `$DEBUG`.

Usually default to `logging.WARNING`, but if `sys.stderr` is a terminal,
default to `logging.INFO`.

Parse the environment variable `$DEBUG` as a comma separated
list of flags.

Examine the in sequence flags to affect the logging level:
* numeric < 1: `logging.WARNING`
* numeric >= 1 and < 2: `logging.INFO`
* numeric >= 2: `logging.DEBUG`
* `"DEBUG"`: `logging.DEBUG`
* `"STATUS"`: `STATUS`
* `"INFO"`: `logging.INFO`
* `"TRACK"`: `TRACK`
* `"WARNING"`: `logging.WARNING`
* `"ERROR"`: `logging.ERROR`

Return an object with the following attributes:
* `.level`: A logging level.
* `.flags`: All the words from `$DEBUG` as separated by commas and uppercased.
* `.module_names`: Module names to be debugged.
* `.function_names`: Functions to be traced in the form *module_name*`.`*func_name*.

## Function `info(*a, **kw)`

Emit a log at `logging.INFO` level with the current `Pfx` prefix.

## Function `log(*a, **kw)`

Emit a log at the specified level with the current `Pfx` prefix.

## Function `logException(exc_type, exc_value, exc_tb)`

Replacement for `sys.excepthook` that reports via the `cs.logutils`
logging wrappers.

## Class `LogTime`

LogTime is a content manager that logs the elapsed time of the enclosed
code. After the run, the field .elapsed contains the elapsed time in
seconds.

### Method `LogTime.__init__(self, tag, *args, **kwargs)`

Set up a LogTime.

Parameters:
* `tag`: label included at the start of the log entry
* `args`: optional array; if not empty `args` is applied to
  `tag` with `%`
* `level`: keyword argument specifying a log level for a
  default log entry, default `logging.INFO`
* `threshold`: keyword argument specifying minimum time to
  cause a log, default None (no minimum)
* `warning_level`: keyword argument specifying the log level
  for a warning log entry, default `logging.WARNING`
* `warning_threshold`: keyword argument specifying a time
  which raises the log level to `warning_level`

## Function `logTo(filename, logger=None, mode='a', encoding=None, delay=False, format=None, no_prefix=False)`

Add a `FileHandler` logging to the specified `filename`;
return the chosen logger and the new handler.

Parameters:
* `logger`: if supplied and not `None`, add the `FileHandler` to that
  `Logger`, otherwise to the root Logger. If `logger` is a string, call
  `logging.getLogger(logger)` to obtain the logger.
* `mode`, `encoding` and `delay`: passed to the `FileHandler`
  initialiser.
* `format`: used to override the handler's default format.
* `no_prefix`: if true, do not put the `Pfx` context onto the front of the message.

## Class `NullHandler(logging.Handler,logging.Filterer)`

A `Handler` which discards its requests.

### Method `NullHandler.emit(self, record)`

Discard the log record.

## Class `PfxFormatter(logging.Formatter)`

A Formatter subclass that has access to the program's `cmd` and `Pfx` state.

### Method `PfxFormatter.__init__(self, fmt=None, datefmt=None, cmd=None)`

Initialise the `PfxFormatter`.

Parameters:
* `fmt`: format template,
  default from `DEFAULT_PFX_FORMAT` `'%(asctime)s %(levelname)s %(pfx)s: %(message)s'`.
  Passed through to `Formatter.__init__`.
* `datefmt`:
  Passed through to `Formatter.__init__`.
* `cmd`: the "command prefix" made available to format strings.
  If not set, `cs.pfx.cmd` is presented.

### Method `PfxFormatter.format(self, record)`

Set `record.cmd` and `record.pfx`
to the global `cmd` and `Pfx` context prefix respectively,
then call `Formatter.format`.

## Function `setup_logging(cmd_name=None, main_log=None, format=None, level=None, flags=None, upd_mode=None, ansi_mode=None, trace_mode=None, module_names=None, function_names=None, verbose=None)`

Arrange basic logging setup for conventional UNIX command
line error messaging; return an object with informative attributes.
That object is also available as the global `cs.logutils.loginfo`.

Parameters:
* `cmd_name`: program name, default from `basename(sys.argv[0])`.
  Side-effect: sets `cs.pfx.cmd` to this value.
* `main_log`: default logging system.
  If `None`, the main log will go to `sys.stderr`;
  if `main_log` is a string, is it used as a filename to
  open in append mode;
  otherwise main_log should be a stream suitable
  for use with `logging.StreamHandler()`.
  The resulting log handler is added to the `logging` root logger.
* `format`: the message format for `main_log`.
  If `None`, use `DEFAULT_PFX_FORMAT_TTY`
  when `main_log` is a tty or FIFO,
  otherwise `DEFAULT_PFX_FORMAT`.
* `level`: `main_log` logging level.
  If `None`, infer a level from the environment
  using `infer_logging_level()`.
* `flags`: a string containing debugging flags separated by commas.
  If `None`, infer the flags from the environment using
  `infer_logging_level()`.
  The following flags have meaning:
  `D`: set cs.logutils.D_mode to True;
  `TDUMP`: attach a signal handler to SIGHUP to do a thread stack dump;
  `TRACE`: enable various noisy tracing facilities;
  `UPD`, `NOUPD`: set the default for `upd_mode` to True or False respectively.
* `upd_mode`: a Boolean to activate cs.upd as the `main_log` method;
  if `None`, set it to `True` if `flags` contains 'UPD',
  otherwise to `False` if `flags` contains 'NOUPD',
  otherwise set it from `main_log.isatty()`.
  A true value causes the root logger to use `cs.upd` for logging.
* `ansi_mode`: if `None`,
  set it from `main_log.isatty() and not cs.colourise.env_no_color()`,
  which thus honours the `$NO_COLOR` environment variable
  (see https://no-color.org/ for the convention).
  A true value causes the root logger to colour certain logging levels
  using ANSI terminal sequences (currently only if `cs.upd` is used).
* `trace_mode`: if `None`, set it according to the presence of
  'TRACE' in flags. Otherwise if `trace_mode` is true, set the
  global `loginfo.trace_level` to `loginfo.level`; otherwise it defaults
  to `logging.DEBUG`.
* `verbose`: if `None`, then if stderr is a tty then the log
  level is `INFO` otherwise `WARNING`. Otherwise, if `verbose` is
  true then the log level is `INFO` otherwise `WARNING`.

## Function `status(*a, **kw)`

Emit a log at `STATUS` level with the current `Pfx` prefix.

## Function `trace(*a, **kw)`

Emit a log message at `loginfo.trace_level` with the current `Pfx` prefix.

## Function `track(*a, **kw)`

Emit a log at `TRACK` level with the current `Pfx` prefix.

## Function `upd(*a, **kw)`

If we're using an `UpdHandler`,
update the status line otherwise write an info message.

Note that this calls `Upd.out` directly with `msg%args`
and thus does not include the current `Pfx` prefix.
You may well want to use the `status()` function instead.

## Class `UpdHandler(logging.StreamHandler,logging.Handler,logging.Filterer)`

A `StreamHandler` subclass whose `.emit` method
uses a `cs.upd.Upd` for transcription.

### Method `UpdHandler.__init__(self, strm=None, upd_level=None, ansi_mode=None)`

Initialise the `UpdHandler`.

Parameters:
* `strm`: the output stream, default `sys.stderr`.
* `upd_level`: the magic logging level which updates the status line
  via `Upd`. Default: `STATUS`.
* `ansi_mode`: if `None`, set from `strm.isatty()`.
  A true value causes the handler to colour certain logging levels
  using ANSI terminal sequences.

### Method `UpdHandler.emit(self, logrec)`

Emit a `LogRecord` `logrec`.

For the log level `self.upd_level` update the status line.
For other levels write a distinct line
to the output stream, possibly colourised.

### Method `UpdHandler.flush(self)`

Flush the update status.

## Function `verbose(*a, **kw)`

Emit a log at `VERBOSE` level with the current `Pfx` prefix.

## Function `warning(*a, **kw)`

Emit a log at `logging.WARNING` level with the current `Pfx` prefix.

## Function `with_log(filename, **kw)`

Context manager to add a `Logger` to the output logs temporarily.

# Release Log



*Release 20210306*:
* Default logging level for ttys is now INFO, not STATUS.
* New VERBOSE level below INFO but above DEBUG.
* infer_logging_level: if verbose unspecified, logging=WARNING on a tty and TRACK otherwise, else if verbose, level=VERBOSE, otherwise WARNING.
* Include .verbose in the loginfo.
* New verbose() and ifverbose().

*Release 20201021*:
* setup_logging: always provide loginfo.upd, being either main_handler.upd if upd_mode otherwise Upd().
* exception(): plumb keyword arguments.

*Release 20200729*:
setup_logging: honour $NO_COLOR if ansi_mode not specified, per https://no-color.org/

*Release 20200613*:
* LogTime: set .end on exit.
* UpdHandle.emit: fix message colouring logic.

*Release 20200521*:
setup_logging: include the logger in loginfo (presently always the root logger).

*Release 20200519*:
bugfix setup_logging: apparently a LoggingProxy does not have an encoding

*Release 20200518*:
* Sweeping removal of cs.obj.O, universally supplanted by types.SimpleNamespace.
* Default to logging level TRACK if stderr is a tty instead of logging.INFO.
* New ifverbose function with leading `verbose` parameter: if None, log at INFO otherwise if true, log at TRACK, otherwise do not log.
* BREAKING: remove global logging_level and trace_level variables, put it all in the global loginfo.
* Make STATUS just below TRACK so that it is above INFO instead of below.
* New status() function for cs.upd messages.
* UpdHandler: treat status_level as special, going directly to Upd.out.
* Improved source line recitation on modern Python.
* Default level if sys.stderr.isatty() now STATUS, not TRACK.
* Some fixes for loginfo initialisation and setting cs.pfx.cmd.

*Release 20200229*:
* Update for new Upd.without context manager.
* setup_logging: default `upd_mode` to `main_log.isatty()`, was previously False.
* Drop UpdHandler.upd method, shadowed by instance attribute, never used.

*Release 20190923*:
* New `TRACK` constant equal to `logging.INFO+5` to provide a level higher than `INFO`
* (which seems unreasonably noisy) and lower than `WARNING`
* warning for tracking salient events.
* New `track()` function to match.

*Release 20190220*:
Improvements to upd_mode.

*Release 20190103*:
Documentation updates.

*Release 20190101*:
Bugfix for @contextmanager usage.

*Release 20171030*:
Assorted fixes from recent module reshuffle. Other small features and cleanups. Drop a couple of unused functions.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
* Pfx: import __exit__ handler
* Preliminary per-module and per-function syntax accepted in $DEBUG envvar.
* Improvements to X(), add DP() and XP() prefixed flavours.
* status() function to update terminal status line.
* New X_via_tty global flag: directs X() to tty instead of sys.stderr.
* Assorted other minor improvements.

*Release 20150118*:
metadata updates

*Release 20150110*:
Initial PyPI release.
