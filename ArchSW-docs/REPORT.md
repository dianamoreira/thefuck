#**_The Fuck_ - Report**


**Contents**
- [Description](#description)
	- [Some use cases](#some-use-cases)
- [Prerequisites](#prerequisites)
- [Contributions](#contributions)
- [Software Architecture](#software-architecture)
	- [Logical View](#logical-view)
	- [Process View](#process-view)
	- [Development View](#development-view)
	- [Physical View](#physical-view)
	- [Scenarios](#scenarios)



##Description
_**The Fuck**_ is a handy tool that allow its users to easily understand what went wrong with their console command. Keeping it short and simple, what it does is show us some alternatives to our last terminal input, (tries to match a rule for the previous command, creates a new command using the matched rule and runs it), and allowing us to make our own rules also.

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
The creator of the app makes it possible for other people to contribute with new rules, new features, bug fixes, etc., to improve the app. These contributions result in a pull request, which is later analyzed and accepted or not by the project owner.


## Software Architecture
_**4+1 architectural view model**_ describes the architecture of software-intensive systems, based on the use of multiple views. The views are used to describe the viewpoint of different stakeholders, such as end-users, programmers, software managers, integrator and system engineer.
There are 5 views, each is a set of specific objective  s of the project, according to the different stakeholders, **Logical View**, **Development View**, **Process View**, **Physical View** and **Scenarios**.


### Logical View

This view is designed to address the end user's concerns regarding the system's insurance of their functional requirements. As such, it provides a basis for understanding the structure and organization of the design of the system. The end result should be a mapping of the functionality in components that provide that functionality. 

![LogicalDiagram](/ArchSW-docs/Diagrams/logical.png)

When the user calls the program, after entering a broken command, `thefuck` initializes its settings and converts shell specific (broken) command (i.e. mistyped command) to shell agnostic version. The opposite process is made with _fixed command_.
Then, corrector matches all enabled rules against shell agnostic command, generates a list of correct commands sorted by priority (similarity) and displays them with UI. The user can, at this point, choose one of the available corrected commands with arrow keys and approve selection with `enter`, or dismiss it with `Ctrl+C`.

### Process View

This view derives from the Logical view the concurrency and synchronization mechanisms underlying the software product. Has the objective to provide a basis for understanding the process organization of the system.

The process view works with the dynamic aspects of the system, explains the system processes and how they communicate, and focuses on system runtime behavior. For this system, we'll use the [activity diagram](http://www.agilemodeling.com/artifacts/activityDiagram.htm) to show the data flow and control, from one activity to another, when executed from the client side (since this is the most relevant aspect of the system).

![ProcessDiagram](/ArchSW-docs/Diagrams/process.png)

The behavior of "the fuck" is intuitive, and is described as follows. What it does is it basically detects a broken command and in whatever shell you are in (as long as it supports alias), a rule is matched, and then some command options are displayed to the user. The user only has to pick whichever it fits what he wants and there it is, the command is fixed.

In more detail, the alias is loaded (it can be _fuck_ or it can be whatever the user wants), and then, whenever there is a broken command (invalid command), the user has the option of not doing anything about it, and try again, or it can type _fuck_  (or, as mentioned before, any other alias picked by the user), and the available options will be displayed to the user. The user can either pick one, or discard them. If he chooses to accept any of the commands, the command will be executed and he will be back in the shell prompt. If he doesn't accept any of the options displayed, nothing will happen and he will be back in the shell prompt.

Also, since _the fuck_ is a very configurable app, it allows the user to easily change a few settings parameters. And that's where **settings.py** comes in. For example, the user can change the list of enabled rules, disable the colored output, require confirmation before running new command (`True` by default), among others. 


### Development View

This view, also known as **Implementation View**, illustrates a system from a programmer's perspective and focuses on configuration management and internal organization of the software components in the development environment. For this system, we'll use the [package diagram](http://www.agilemodeling.com/artifacts/packageDiagram.htm) below to describe the dependencies between the main components of the code.

![DevelopmentDiagram](/ArchSW-docs/Diagrams/PackageDiagram.png)

So, we organize *The Fuck* in the following packages and single modules:
  - **_rules_** - contains rules enabled by default. Each rule is a special module with two functions:
    * `match(command)` - True when rule matched;
    * `get_new_command(command)` - return a list of fixed commands.
  - **_specific_** - utility functions to help matching specific rules. Provides information about existence of `apt-get ` or ArchLinux `pacman`, for instance, and predicts a fix for the command.
  - **_shells_** - converts shell specific command to `sh` compatible version, expands aliases and environment variable.
  - **_system_** - decides which terminal encoding to use and how to recognize key up/down movements in `unix` and `Windows`.
  - **_Aux_** - auxiliary modules that deal with the program settings, errors, global variables, etc. We grouped these modules in a virtual package in order to make the diagram easier to understand.
  - **_corrector.py_** - matches all enabled rules from rules package against current command and return all available corrected commands. 
  - **_ui.py_** - allows to choose from a list of corrected commands with arrow keys, approve selection with `Enter` or dismiss it with `Ctrl+C`. 
  - **_types.py_** - it's distributed in three classes:
    * `Command(object)` - parser of commands;
    * `Rule(object)` - inicializes rule with given fields;
    * `CorrectedCommand(object)` - run command from chosen rule by user.

The **Aux** package contains the following modules:
  - **_conf.py_** - configure the settings.
  - **_utils.py_** - define the necessary auxiliary functions for developing the program.
  - **_logs.py_** - deals with internal errors.
  - **_const.py_** - initializes through global variables the default options.
  - **_exceptions.py_** - displays an error message when the user enters a command that is not found.


### Physical View

This view, also known as **Deployment View**, is concerned with the topology of software components on the physical layer, as well as the physical connections between them. Makes the mapping the software to the hardware.

For this system, we'll use the [deployment diagram](http://www.agilemodeling.com/artifacts/deploymentDiagram.htm) to show what hardware components ("nodes") exist, what software components ("artifacts") run on each node, and how the different pieces are connected.


### Scenarios

The use cases or scenarios, as it is also known, connects all the views described above.

In this view we can analyze the sequences of interactions between objects (in this case the user), and between the different processes. It helps to identify architectural elements and illustrate and validate the architecture design. It also helps the architect during the architecture design.

For this system, we'll use the [use case diagrams](http://www.agilemodeling.com/artifacts/useCaseDiagram.htm) to represent a user's interaction with the system, showing the relationship between the user and the different use cases.
