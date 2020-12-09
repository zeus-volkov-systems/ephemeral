# Ephemeral

## A lightweight task-focused WMS

### Status

Version 1.0.0

### Introduction

Ephemeral is a pure python, asyncio driven, functional workflow management system. It is designed with a clear separation in mind of engine logic, task logic, and library logic - in fact, these packages remain completely separate and their format specified by structural requirement. This allows ephemeral to serve as a very stable platform for developing python libraries that are designed in a clear and stereotyped manner. The structural rules enforce good design.

We built ephemeral because we wanted to create a tool that does this good design up front. Many workflow management systems already exist, but most focus on something else - distributed performance, error recovery, etc. Ephemeral focuses on enforcement of good software engineering practices.

The ephemeral job builder takes json maps which specify jobs to run, turns these maps into executable code, and runs the code as a series of asynchronous tasks. The job map contains an input datasource, a set of tasks, and a workflow that specifies how tasks flow from one to the next.

Ephemeral can be used to drive or glue together other workflow systems. In fact, that is a good use case. Tests are included in the package that demonstrate a multipath job that runs dask distributed to read, parse, calculate statistics, and create a report from a NetCDF file. Tests are the best way to learn about using ephemeral - start with the ephemeral/engine/resources/test/job directory to see how different jobs process data.

A simple example looks like this:

```json
{
    "name": "Example Job",
    "datasource" : {
                    "source": "direct",
                    "content": {"input": "this is our test string input"}
                    },
    "tasks": [
                {
                    "name":"in",
                    "type":"input"
                },
                {
                    "name": "example",
                    "type": "function",
                    "method": "example",
                    "namespace": "main",
                    "consumes": "string",
                    "produces": "string",
                    "init_args": {"example_property": "This is a test!"}
                },
                {
                    "name": "out",
                    "type": "output"
                }
           ],
    "workflow": [["in", "example"],
                ["example", "out"]]
}

```

From this map, it is obvious that there is one direct-input data source, on input task, one processing task named 'example', and one output task, and they are connected as specified in the 'workflow' key. As all ephemeral projects rely on a strict project structure for tasks, the namespace for this function indicates it can be found in ephemeral/tasks/src/main. Listing this directory namespace shows two python files - task_factory.py and tasks.py. These files are both stereotyped, and both always need to reside in the namespace being used. Copy/paste allows them to quickly form other namespaces. Opening up task_factory.py, it can be seen that other task_factories are loaded in dictionary entries, and the 'tasks.py' file is loaded as a tasks var. This is generally all that ever needs to be updated in the task_factory module for a given namespace. The methods in task_factory (other than adding entries to the dict in make_task_dict) don't need to edited at all.

In the 'main' namespace's 'tasks.py' file, there are two methods that always exist (another make_task_dict and a get_task). Like in the task_factory.py file, the make_task_dict method here only has to be provided with new dictionary entries for methods. This 'tasks.py' file is also where user business logic functions are wrapped in closures. User business functions would be imported in the tasks.py file and then each wrapped in a function that returns an 'async def' for the user business logic. The pattern is always the same, and examples in the package can be followed to get a hang of what's expected. You will see that for the tests, all the user library code resides in the ephemeral/library subnamespaces, but this isn't a hard requirement.

To see how this job runs, you can open the runner at ephemeral/engine/src/test/jobs/example_test.py - submitting a job in ephemeral involves only loading the fully qualified json path, building a job from either a file containing JSON or directly from a JSON map, and then submitting a job to grab output.

### Description

An ephemeral job must have a single input method and a single input data source. A job can contain an arbitrary number of function tasks, and an arbitrary number of output tasks. Any function task can flow to an arbitrary number of other function tasks in the job map. So task 1 may flow to both task 2 and task 3. The acyclic digraph
is produced and validated by the system when parsed.

Each task must accept a python dictionary and produce either a python dictionary or
a list of dictionaries. If a task produces a single dictionary, that dictionary is
passed to any child tasks as their input data. If the task produces a list of dictionaries,
each dictionary is passed individually to child tasks and these are run asynchronously.

Only when the entire task chain finishes every output will the job be complete.

The job builder relies on a task factory, which contains functions that correspond to
the tasks specified in task maps. Each task also has a formal definition as a json string
stored on file, so that task definitions can be retrieved by the system and served to an end user,
for the end user to compose into a job map.

Any business logic may take place within a given task. To illustrate this, examine the dask distributed
test job, which demonstrates a working example of submitting a job to a distributed cluster and working with
dask futures in the course of this job.

The benefit of having an additional layer of abstraction for jobs, on top of using a specific workflow engine,
is that the job builder asyncio engine uses a single thread to manage blocking. So tasks which may be better suited
for using something other than a distributed engine, or another engine, can still use whatever they need (i.e., simple calculation,
  multithreading, multiprocessing, or another distributed engine) and seamlessly work with those distributed calculations.

### Installation

To install this package, there are a few options.

1. Use pip! Change into the directory you cloned, and run:

    ```Shell
    pip install . --upgrade
    ```

    This should run through and install the package along with dependencies. Eventually you should see the following if successful:

    ```Shell
    ...3.6/site-packages (from pandas>=0.18.0->xarray->ephemeral==0.0.1)
    Requirement already up-to-date: six>=1.5 in /Users/rab25/anaconda3/lib/python3.6/site-packages (from python-dateutil>=2->pandas>=0.18.0->xarray->ephemeral==0.0.1)
    Installing collected packages: ephemeral
      Found existing installation: ephemeral 0.0.1
        Uninstalling ephemeral-0.0.1:
          Successfully uninstalled ephemeral-0.0.1
      Running setup.py install for ephemeral ... done
    Successfully installed ephemeral-0.0.1
    ```

2. Use the excellent pipenv! <https://github.com/pypa/pipenv>
pipenv combines pip and virtual environments.
Assuming you've installed it, CD into your cloned directory, and do

    ```Shell
    pipenv install
    
    pipenv shell
    
    nosetests
    ```

3. Run in a docker container:  
    First build the image: `docker build -t ephemeral .`  
    Run the tests: `docker run -it ephemeral nosetests`

4. Use some other environment of your choice! If you find something that works well, please let me know or create a PR on this README.

### Package Validation

To validate your installation, run the tests. From the project root, run

```Shell
nosetests
```

This should run a few tests on jobs (4 so far) which are set up in {root}/ephemeral/engine/src/test/jobs. It takes a few seconds, because one of the tests is actually spinning up a dask cluster to do some NetCDF processing.
Each test exhibits some unique engine behavior. They are:

* example_test.py
* branching_test.py
* multi_layer_vector_return_test.py
* dask_xarray_test.py

You can run these tests individually too, to get better descriptive output. Just CD into the {root}/ephemeral/engine/src/test/jobs directory,

and then you can run individual files like

``` python branching_test.py ```

For the branching test, if successful, it will provide an output like:

```Shell
Ryans-MacBook-Pro:jobs rab25$ python3 multi_layer_vector_return_test.py
{'autumntmin', 'springtmin', 'summertmax', 'winterprecip', 'summertmin', 'springprecip', 'wintertmax', 'summerprecip', 'springtmax', 'autumnprecip', 'autumntmax', 'wintertmin'}
Parsing a job map from a file.
Submitting a job for execution.
{'id': 'GCYJCBUBPVV9B6L', 'type': 'output', 'name': 'combined-output', 'data': [{'combined': 'springtmax'}, {'combined': 'springtmin'}, {'combined': 'springprecip'}, {'combined': 'summertmax'}, {'combined': 'summertmin'}, {'combined': 'summerprecip'}, {'combined': 'wintertmax'}, {'combined': 'wintertmin'}, {'combined': 'winterprecip'}, {'combined': 'autumntmax'}, {'combined': 'autumntmin'}, {'combined': 'autumnprecip'}], 'method': <function get_output_function.<locals>.output_function at 0x309fefb70>, 'parent': 'TS4LK37UTFSWPM8'}
{'autumntmin', 'springtmin', 'summertmax', 'winterprecip', 'summertmin', 'springprecip', 'wintertmax', 'summerprecip', 'springtmax', 'autumnprecip', 'autumntmax', 'wintertmin'}
.
----------------------------------------------------------------------
Ran 1 test in 0.004s

OK
```

### Project Structure

So once you've run the tests, you have done full job processing in the system. Opening a test job is a good way to trace how the system works.

First, we pass a job map json file (or we can pass a json map directly) to a manual_controller.

The manual controller then passes the job map to a validator. the job map itself parses tasks, validates tasks individually, and also validates tasks against inputs and outputs as specified in the workflow. The specified input datasource is also validated up front - if anything fails, we haven't wasted time processing.

After validation, the tasks are split and prepared according to their specification - each task lives in a separate library, and is loaded through a wrapper that lives in the ephemeral tasks subpackage. This wrapper is a python closure that uses any specified constructor parameters to prepare the library function and hold it as a reference.

After preparation, the job begins to run using the asyncio 'futures' based operation. Data is passed through the tasks as specified by the workflow. Ephemeral allows two top level data types - lists and dicts. Every task wrapper must accept a dict, which can contain any other data. Tasks can do anything with their data inside the dict, and can then return a dict or list of dicts. If a list of dicts is passed out of a task, those dicts are then parallelized (branched) by the ephemeral processor.

Post processing, final results are returned inside list of dicts, which can be pulled out and used as needed.

### Open Issues

* Creating a CLI tool for creating new ephemeral namespaces
* Aggregation and windowing over branched results
* Logging library
* Error handling in case of async thread failure

Copyright Zeus Volkov Systems, 2020-*
