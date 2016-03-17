#**_The Fuck_ - Report**
##Description
_**The Fuck**_ is a handy tool that allow it's users to easily understand what went wrong with their command.
Keeping it short and simple, what it does is show us some alternatives to our last terminal input, (tries to match a rule for the previous command, creates a new command using the matched rule and runs it), and allowing us to make our own rules also.

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
