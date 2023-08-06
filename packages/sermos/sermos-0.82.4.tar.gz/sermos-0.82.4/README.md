# Sermos

__Note:__ This represents Sermos' _developer_ README.
Public documentation generated using Sphinx and
located at [Sermos](https://docs.sermos.ai/).

## Quickstart

1. Add `sermos` as a dependency to your Python application
1. Install extras depending on what you are building:

  1. `flask` - Convenient interface for Flask applications
  1. `flask_auth` - Utilize Sermos' authentication system ([Sermos Cloud](https://sermos.ai) only)
  1. `web` - Some standard web server dependencies we like
  1. `workers` - Installs [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) and [networkx](https://networkx.org/documentation/stable/index.html), which are required if using [Sermos Cloud](https://sermos.ai) for your deployed pipelines and scheduled tasks
  1. `deploy` - Only required for deploying to [Sermos Cloud](https://sermos.ai)

## Overview

Sermos provides a set of tools and design roadmap for developers to _quickly_
and _effectively_ integrate Data Science into real-world applications. The core
design decisions and recommended technologies are based on nearly a decade
of putting data science to work in demanding applications such as real-time motorsports
strategy at [Pit Rho](https://pitrho.com), custom implementations across industries
as diverse as energy, finance, and healthcare at [Rho AI](https://rho.ai), and climate
impact assesment tools at [CRANE](https://cranetool.org). With that
said, this is built by _developers and data scientists_ and strives to strike an
appropriate balance between opinionated decisions and personal choice.

This is open source software and we look forward to seeing what you can build
on top of Sermos. For those looking for quick, scalable, enterprise-grade
deployments, make sure to check out [Sermos Cloud](https://sermos.ai),
which is purpose-built for running complex, scalable, highly available Machine Learning (ML)
workloads, including Natural Language Processing (NLP), Computer Vision (CV), Decision
Modeling, Internet of Things (IoT), and more.

A standard Sermos application comprises two key libraries:

1. [Sermos](https://gitlab.com/sermos/sermos)
  * This is the base package with optional scaffolding, architecture components
  (e.g. [DAG implementation](https://en.wikipedia.org/wiki/Directed_acyclic_graph)
  on top of
  [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)),
  and some useful utilities.
1. [Sermos Tools](https://gitlab.com/sermos/sermos-tools)
  * Tool catalog for use in Sermos (or other!) Machine Learning applications.


### Sermos

* Celery Configuration
* Pipelines
* APIs
* Utilities

### Sermos Tools

* NLP Tools
  * Document Classification
  * Document Similarity Searching
  * Date Finding
  * etc.
* IoT Tols
* General Tools
  * Slack Notifications

### Your Application

_aka "Sermos Client" or "Client Codebase"_

This is where all of your code lives and only has a few _requirements_:

1. It is a base application written in Python (additional language support
slated for the future).
1. Scheduled tasks and Pipeline nodes must be Python Methods that accept
at least one positional argument: `event`
1. [Optional] A `sermos.yaml` file, which is a configuration file if you
choose to deploy using [Sermos Cloud](https://sermos.ai)

## Celery [optional]

Sermos provides sensical default configurations for the use of
[Celery](http://www.celeryproject.org/). The default deployment uses RabbitMQ,
and is recommended. This library can be implemented in any other workflow
(e.g. Kafka) as desired.

There are two core aspects of Celery that Sermos handles and differ from a
standard Celery deployment.

### ChainedTask

In `celery.py` when imported it will configure Celery and also run
`GenerateCeleryTasks().generate()`, which will use the `sermos.yaml` config
to turn customer methods into decorated Celery tasks.

Part of this process includes adding `ChainedTask` as the _base_ for all of
these dynamically generated tasks.

`ChainedTask` is a Celery `Task` that injects `tools` and `event` into the
signature of all dynamically generated tasks.

### SermosScheduler

We allow users to set new scheduled / recurring tasks on-the-fly. Celery's
default `beat_scheduler` does not support this behavior and would require the
Beat process be killed/restarted upon every change. Instead, we set our
custom `sermos.celery_beat:SermosScheduler` as the `beat_scheduler`,
which takes care of watching the database for new/modified entries and reloads
dynamically.

## Workers / Tasks / Pipeline Nodes

If running in [Sermos Cloud](https://sermos.ai), Sermos runs all work
(whether scheduled tasks or pipeline nodes) as Celery
workers. Sermos handles decorating the tasks, generating the correct Celery
chains, etc.

Customer code has one requirement: write a python method that accepts one 
positional argument: `event`

e.g.

	def demo_pipeline_node_a(event):
	    logger.info(f"RUNNING demo_pipeline_node_a: {event}")
	    return

## Sermos Tools [optional]

Sermos provides much of the scaffolding and design guidance for running
machine learning workloads and has a companion project
[Sermos Tools](https://gitlab.com/sermos/sermos-tools), which provides
a set of useful (and growing) tools intended to streamline
development of machine learning workflows and tasks.

### Generators
_TODO_: This needs to be updated both in code and documentation. Leaving here
because it's valuable to update in the future.

A common task associated with processing batches of documents is generating
the list of files to process.  `sermos.generators` contains two helpful
classes to generate lists of files from S3 and from a local file system.

`S3KeyGenerator` will produce a list of object keys in S3. Example:

    gen = S3KeyGenerator('access-key', 'secret-key')
    files = gen.list_files(
        'bucket-name',
        'folder/path/',
        offset=0,
        limit=4,
        return_full_path=False
    )

`LocalKeyGenerator` will produce a list of file names on a local file system.
Example:

    gen = LocalKeyGenerator()
    files = gen.list_files('/path/to/list/')

## Testing

If you are developing Sermos core and want to test this package,
install the test dependencies:

    $ pip install -e .[test]

Now, run the tests:

    $ tox

## Contributors

Thank you to everyone who has helped in our quest to put machine learning
to work in the real-world!

* Kevin Lyons
* Alejandro Mesa
* Cassie Borish
* Vickram Premakumar
* Aral Tasher
* Akshay Pakhle
* Gilman Callsen
* _Your Name Here!_
