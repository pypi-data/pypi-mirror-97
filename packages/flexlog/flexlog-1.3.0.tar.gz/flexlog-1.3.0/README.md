# README

This package shall make logging easier. These are the goals:

* Make setup of a logger with time-stamped log messages a no-brainer
* Make adding/removing additional log files a one-liner

Use it like this:

```python
from flexlog import cleanlogger

log = cleanlogger.CleanLogger("My Cool Module Name, Version 42")

# Log to console
log.info("Hello World!")

# Add a file
log.add_filelogger("mylogging.log")
log.debug("Log level of files is debug by default, but you can give it as parameter, too.")

import logging
log.add_filelogger("problemsonly.log", loglevel = logging.WARNING)

# Remove a file
log.remove_filelogger("mylogging.log")
```