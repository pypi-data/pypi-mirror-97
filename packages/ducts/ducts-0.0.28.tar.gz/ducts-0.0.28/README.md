# DUCTS: DUplex Communication and Transactional Streaming Web Framework

## SAMPLE

## Install

You can install this package by pip

        pip3 install ducts

## start and stop server and other backend processes

You can start ducts server as well as other backends with following commands.

        python -m ducts server start [-c configfile]
        python -m ducts asr start [-c configfile]

You can also stop them.

        python -m ducts server stop [-c configfile]
        python -m ducts asr stop [-c configfile] 

In configfile, you can define followings:

        [ducts.common_config]

        # root directory of all local path (<class 'pathlib.Path'>)
        # ducts_home = .
        
        # filepath to store PID (<class 'str'>)
        # pidpath = {ducts_home}/.pid/{module}_{service}.pid
	
----

This is the README file for the project.

The file should use UTF-8 encoding and can be written using
[reStructuredText][rst] or [markdown][md use] with the appropriate [key set][md
use]. It will be used to generate the project webpage on PyPI and will be
displayed as the project homepage on common code-hosting services, and should be
written for that purpose.

Typical contents for this file would include an overview of the project, basic
usage examples, etc. Generally, including the project changelog in here is not a
good idea, although a simple “What's New” section for the most recent version
may be appropriate.

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/pypa/sampleproject
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
