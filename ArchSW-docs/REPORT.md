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
_**The Fuck**_ is a handy tool that allows its users to easily understand what went wrong with their console command. Keeping it short and simple, what it does is show them some alternatives to our last terminal input, (tries to match a rule for the previous command, creates a new command using the matched rule and runs it), and allowing them to make their own rules also.

This project was created on GitHub in April 2015 and in total there are over 70 contributors, although only three have been active during this year (2016). Its creator is Vladimir Yakovlev ("nvbn") along side two others, Martin Carton ("mcarton") and Pablo Aguiar ("scorphus") constitute the principal nucleus of the app development. According to its creator, this app was inspired by a [@liamosaur](https://twitter.com/liamosaur/) [tweet](https://twitter.com/liamosaur/status/506975850596536320).


Let's take a look:

<figure>
    <img src='https://raw.githubusercontent.com/nvbn/thefuck/master/example.gif' alt='Example' /><br>
  <sup>Image from https://github.com/nvbn/thefuck<sup>
</figure>
<br>

### Some use cases:
```bash
user$ aptget install java
aptget: command not found
user$ fuck
apt-get install java
```

### Prerequisites
This program requires Python with [pip](https://pypi.python.org/pypi/pip) installed. On UNIX, it's necessary to have `python-dev`. On Windows you may need a shell with alias support such as the `bash` shell from the [mingw](www.mingw.org).
We recommend the [cmder](www.cmder.net) console emulator on Windows.


### Contributions
To improve the app, the creator makes it possible for other people to make contributions such as new rules, new features or bug fixes. These contributions are performed via pull requests, which are later analyzed and approved by the project owner.


## Software Architecture
_**4+1 architectural view model**_ describes the architecture of software-intensive systems, based on the use of multiple views. The views are used to describe the perspective of different stakeholders, such as end-users, programmers, software managers, integrators and system engineers.
There are 5 views, each of them describing the expected behaviour of the system from the point of view of the different stakeholders: **Scenarios**, **Logical View**, **Development View**, **Process View** and **Physical View**.


### Logical View

This view is designed to address the end user's concerns regarding the system's insurance of their functional requirements. As such, it provides a basis for understanding the structure and organization of the overall system. The end result should be a mapping of the functionality in components that provide that functionality. 

![LogicalDiagram](/ArchSW-docs/Diagrams/logical.png)

When the user calls the program, after entering a _broken command_ (i.e. mistyped command), _**The Fuck**_ initializes its settings and converts that shell specific (broken) command to its shell agnostic version (the reverse process is made with _fixed command_).
Afterwards, the _corrector_ matches all enabled rules against the shell agnostic command, generates a list of correct commands sorted by priority (similarity) and displays them with _UI_. The user can, at this point, choose one of the available corrected commands with arrow keys and approve selection with `enter`, or dismiss it with `Ctrl+C`.

### Process View

This view derives from the Logical view the concurrency and synchronization mechanisms underlying the software product, having the objective to provide a basis for understanding the process organization of the system.

The process view works with the dynamic aspects of the system, explains the system processes and how they communicate, and focuses on system runtime behavior. For this system, we'll use the [activity diagram](http://www.agilemodeling.com/artifacts/activityDiagram.htm) to show the data flow and control, from one activity to another, according to the user's view.

![ProcessDiagram](/ArchSW-docs/Diagrams/process.png)

The behavior of _**The Fuck**_ is intuitive, and is described as follows. It detects a broken command, regardless of the shell in which it's being executed, and matches it with a set of rules. Then, several corrected commands are displayed to the user, allowing for the user to pick the one that translates his immediate request.

In more detail, after the alias of _the fuck_ is loaded, if there is an invalid command, the user can call `fuck` (by default). This will provide the available suggestions, corresponding to possible corrections for the (broken) input command. Then, the user can either pick one of them, or cancel. If the user selects one of the provided options, it will be executed according to the underlying Shell running in the user's environment. If he doesn't accept any of the options displayed, nothing will happen, and he will be redirected to the original shell prompt.

Furthermore, _**The Fuck**_ allows for user-specific configurations. This is made available using **settings.py**, which defines the list of enabled rules and other slight tweaks on the application functionality (such as disabling of colored output, or confirmation requirement for command executions).

### Development View

This view, also known as **Implementation View**, illustrates the system from a programmer's perspective and focuses on configuration management and internal organization of the software components in the development environment. For this system, we'll use the [package diagram](http://www.agilemodeling.com/artifacts/packageDiagram.htm) below to describe the dependencies between the main components of the code.

![DevelopmentDiagram](/ArchSW-docs/Diagrams/PackageDiagram.png)

So, we organize _**The Fuck**_ in the following packages and single modules:
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

The relation between the packages is depicted by the diagram, as well as the direction of the relationship established.

### Physical View

This view, also known as **Deployment View**, is concerned with the topology of software components on the physical layer, as well as the physical connections between them. For this system, we'll use the [deployment diagram](http://www.agilemodeling.com/artifacts/deploymentDiagram.htm) to show what hardware components ("nodes") exist, what software components ("artifacts") run on each node, and how the different pieces are connected.

To start  _**The Fuck**_, the client requires only a computer running an operative system following the specifications defined on the prerequisites section. As such, running  _**The Fuck**_ gives rise to two main "artifacts": the user interface (`UI`), interacting with the `rule corrector`.


### Scenarios

The use cases or scenarios, as it is also known, connects all the views described above.

In this view we can analyze the sequences of interactions between objects (in this case the user), and between the different processes. It helps to identify architectural elements and illustrate and validate the architecture design. It also helps the architect during the architecture design.

For this system, we'll use the [use case diagrams](http://www.agilemodeling.com/artifacts/useCaseDiagram.htm) to represent a user's interaction with the system, showing the relationship between the user and the different use cases.


![UseCaseDiagram](/ArchSW-docs/Diagrams/usecase.png)

In this case, the use cases, or scenarios, are really simple. You have the user, who has acess to the shell, and from there, he can type `fuck`, execute a command or exit. He can also configure the rules through the configure files. When the user types `fuck`, the program prompt will appear and the user will choose if he wants to accept the suggested command, ask for more commands, or reject the commands suggested by the program. If the user chooses to accept the suggested command, the command will be executed.
