# adh-apis

Contains all the code common to both ADH internally, Cherenkov Camera servers and analysis reader. This project only builds relevant libraries to be used in your own
project. To build unit tests for this code the project ACADA/Array-data-handler should be used instead. 

## Cloning

This module relies on third party code included via git submodules.
When cloning for the first time, make sure to add `--recursive`, i.e.

```bash
$ git clone --recursive git@gitlab.cta-observatory.org:cta-computing/common/acada-array-elements/adh-apis
```

To update the submodules, or if you forgot to add the `--recursive` when cloning, do
```bash
$ git submodule update --init --recursive
```

## Build

To build the apis to directory BUILD cmake3 should be invoked from the cloned root. e.g.
```bash
   cmake3 -B BUILD -S .
   cmake3 --build BUILD 
```
In case you do not have a working python3 enabled, you can disable the python bindings by adding the option -DPYTHON=OFF to the first cmake3 command.

In the above example the compiled libraries would be placed under ./BUILD/lib, executables in ./BUILD/bin while the generated protocol buffer code is under ./BUILD. 

## Example programs

There are 4 example programs which demonstrate the usage of the ADH APIs for 
dealing with Events and Trigger data. Currently only the R1 data format is used, DL0 will be added once its data model will be agreed.

Command lines given as examples below assume that the code was built according to the directions given above. Calling the programs without
any argument prints the help.

### Sending Cherenkov events from camera servers
Two executables are provided: `events_server` and `events_consumer` along with their source code `ExecExampleEventsServer.cpp` and `ExecExampleEventsConsumer.cpp` respectively.

The server creates dummy R1 events and sends them in a loop to the consumer, which then discards them. Obviously server and consumer should use the same port number. The following command lines would generate 100 events at ~10Hz on port 1234 before exiting:

```
BUILD/bin/events_server --port 1234 --sleep 100000 --total 100
```

If running the consumer on the same host its command line should be:
```
BUILD/bin/events_consumer --input tcp://localhost:1234
```

Otherwise `localhost` should be replaced by the hostname (or IP) running the server.

The total number of consumed messages should be 102: 100 events + 2 header messages. 


### Sending software triggers and listening for events requests
An executable is provided: ```swat_client``` along with its source code ```ExecExampleSWATClient.cpp```.

The software exhibits the basic usage of the C++-based SWAT API in order to send triggers and receive requests. It configures the SWAT_API_CLIENT structure using a .ini file or programmed defaults, starts the underlying processing thread and creates two threads: first is responsible for event generation and submission and second reads and prints event information to stdout (for performance reasons it's recommended to redirect to a file). To test, start a SWAT server, configure LD_LIBRARY_PATH to link BUILD/lib/libswat.so and BUILD/lib/libsADHCore.so and run using:
````
BUILD/bin/swat-client --file <ini configuration file path; example at swat/SWAT_config.ini> --IP <SWAT IP> --channel <telescope channel; use 0 for 1st instance 1 for 2nd and so on> >./events.log
````
The client generates events indefinitely until the process is stopped (during preliminary testing at a rate of ~30k events per second).
