#**_The Fuck_ - Report**


**Contents**
- [Description](#description)
- [Prerequisites](#prerequisites)
- [Contributions](#contributions)
- [Software Architecture](#software-architecture)
	- [Logical View](#logical-view)


##Description
_**The Fuck**_ is a handy tool that allow it's users to easily understand what went wrong with their console command. Keeping it short and simple, what it does is show us some alternatives to our last terminal input, (tries to match a rule for the previous command, creates a new command using the matched rule and runs it), and allowing us to make our own rules also.
This project was created on GitHub in April 2015 and in total there are over 70 contributors, although only three have been active during this year (2016). Its creator is Vladimir Yakovlev, whose nickname is "nvbn" which, along with two others, Martin Carton ("mcarton") and Pablo Aguiar ("scorphus") constitute the principal nucleus of the app development. According Vladimir Iakovlev, was inspired by a [@liamosaur](https://twitter.com/liamosaur/) [tweet](https://twitter.com/liamosaur/status/506975850596536320).


Let's take a look:

<figure>
    <img src='https://raw.githubusercontent.com/nvbn/thefuck/master/example.gif' alt='Example' /><br>
  <sup>Image from https://github.com/nvbn/thefuck<sup>
</figure>
<br>

#### Some use cases:
```bash
user$ aptget install java
aptget: command not found
user$ fuck
apt-get install java
```

## Prerequisites
This program requires Python with [pip](https://pypi.python.org/pypi/pip) installed. On UNIX, it's necessary to have `python-dev`. On Windows you may need a shell with alias support such as the `bash` shell from the [mingw](www.mingw.org).
We recommend the [cmder](www.cmder.net) console emulator on Windows.


## Contributions
The creator of the app gives the possibility of other people being able to contribute with new rules, new features, bug fixes, etc., to improve the same. These contributions are made from a pull request, which will then be analyzed and accepted or not by the project owner.


## Software Architecture
_**4+1 architectural view model**_ describes the architecture of software-intensive systems, based on the use of multiple views. The views are used to describe the viewpoint of different stakeholders, such as end-users, programmers, software managers, integrator and system engineer.
There are 5 views, each is a set of specific objectives of the project, according to the different stakeholders, **Logical View**, **Development View**, **Process View**, **Physical View** and **Scenarios**.


### Logical View

This view is designed to address the end user's concerns regarding the system's insurance of their functional requirements. As such, it provides a basis for understanding the structure and organization of the design of the system. The end result should be a mapping of the functionality in components that provide that functionality. For this system, we'll use the [package diagram](http://www.agilemodeling.com/artifacts/packageDiagram.htm) below to describe the dependencies between the main components of the code.

![LogicalDiagram](/ArchSW-docs/Diagrams/LogicalView.png)

So, we organize *The Fuck* in the following packages and single modules:
  - **_rules_** - contains rules enabled by default. Each rule is a special module with two functions:
    * `match(command)` - True when rule matched;
    * `get_new_command(command)` - return a list of fixed commands.
  - **_shells_** - converts shell specific command to sh compatible version, expands aliases and environment variable.
  - **_ui.py_** - allows to chose from a list of corrected commands with arrow keys, approve selection with `Enter` or dismiss it with `Ctrl+C` 
  - **_corrector.py_** - matches all enabled rules from rules package against current command and return all available corrected commands.
