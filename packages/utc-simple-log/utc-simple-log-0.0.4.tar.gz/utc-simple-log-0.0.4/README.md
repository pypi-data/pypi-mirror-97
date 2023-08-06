# UTC Simple Log

Simple log with UTC timer     

* No option
* Both console and File
* Singleton logger

## Quick start
```python
# -*- coding: utf-8 -*-
from sslog.logger import SimpleLogger

# Default parameter
# File: ./logs/log.txt
# File size: 2Mb 
# Rolling count: 5
logger = SimpleLogger()

logger.setLevel(logging.DEBUG)

logger.debug('hello world!')
logger.info('This is a simple log.')
logger.warning('Quick start')
logger.error('It print to console and')
logger.critical('files("./logs/log.txt")')
logger.fatal('fatal and critical')
```

### Console and File
```bash
2021-03-03T05:54:51, [   DEBUG] [logger.py:_tests,L:147]: Debugging message  
2021-03-03T05:54:51, [    INFO] [logger.py:_tests,L:148]: Info message  
2021-03-03T05:54:51, [ WARNING] [logger.py:_tests,L:149]: Warning message  
2021-03-03T05:54:51, [   ERROR] [logger.py:_tests,L:150]: Error message  
2021-03-03T05:54:51, [CRITICAL] [logger.py:_tests,L:151]: Critical message  
2021-03-03T05:54:51, [CRITICAL] [logger.py:_tests,L:151]: FATAL message
```
