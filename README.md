# log2mq

EOS.IO logfile to Message Queue([NSQ](https://github.com/nsqio/nsq)).

Just a simple script, no authorization, etc. Please use it carefully.

## Installation

`pip install git+https://github.com/eostea/log2mq.git`

## Usage: 

### Listen to a log file:

`log2mq /tmp/test.log http://127.0.0.1:4151/pub?topic=test`

### Listen to a log directory:

`log2mq /tmp/ http://127.0.0.1:4151/pub?topic=test`
