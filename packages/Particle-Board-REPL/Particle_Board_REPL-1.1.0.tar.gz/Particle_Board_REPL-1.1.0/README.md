# particle board REPL (PBR)  program.


    pip install Particle_Board_REPL
    
To run interactively in with the REPL.

    PBR -r

This Module adds Particle board cli functionality to
the [Simple_Process_REPL](https://github.com/Ericgebhart/Simple_Process_REPL.git) 
along with
various other higher level functions for interacting with Particle.io boards.
The idea is to make it possible to create a repeatable process which can interact
test, and program a particle.io board.

This uses the particle.io cli, **particle-cli** in the Arch-linux AUR,
to interface with a board, verify it's life, update it, claim/register
it, flash it, test it, etc.

The [_Simple_Process_REPL_](https://github.com/Ericgebhart/Simple_Process_REPL.git) 
provides the basic application functionality here. Everything
is configurable in a yaml file, Both Simple_process_repl and the particle board
interface provide defaults which are merged into _config_ in the Application
State dict. Additional config files can be merged on top of these to give complete
control over every possible setting.

All of the commands here could be almost doable in a chain of _'do this', 'do that'_. But
the boards take time in between events. The USB device comes up and down constantly,
it's not reliable just because you know that's where the board was. I have read about
other gnu/linuxs which change the device on occasion or always. Arch does not. Once
I have it, I have it. However, it comes and goes... 

If a command fails at any point in a process, the entire process stops and the
board is considered a failure.

So we have to wait, watch and listen.

But, as a whole, it's just a module of things we'd like to do.  So we 
wrap those up to make life easier. and life is easier. At some point, 
making life is easier is just listing all the previous things that made life easier. 
And so it goes.

# Simple_Process_REPL runs 4 ways, and so does PBR.

Once you have some processes defined you can then run what you like in
4 different ways,w

 * run the autoexec setting once: `python -m Particle_Board_Interface`
 * Start a REPL   `-r`
 * Run the autoexec setting in a loop with a continue dialog `-i` 
 * To run commands instead of the autoexec, Just add them to the command.

 `PBR -r get list
  PBR -i get list
  PBR get list`

## Dependencies
 * [_Simple_Process_REPL_](https://github.com/Ericgebhart/Simple_Process_REPL.git) 
 * It's all in pypi, so just `pip install Particle_Board_Interface`


### Getting Help

Help with the command line can be obtained with `-h`,
Additionally, Help with the symbols which are available for programming in the yaml files or 
in the REPL are obtained with the `help` command, so `help` runs help.
 * `PBR -h` for cli help.
 * `PBR help` for internal help.
 * `PBR particle-help` for internal particle specific help.

The easiest way to understand this system by using the REPL. 
It will show you how it works. `PBR -r` 
 
Once in the REPL at the prompt; __PBR:>__,  There are two help 
commands.  __help__ and __particle-help__.  _Help_ shows all
the commands known with their documentation. _particle-help_,
__show-all__ will show you everything there is to know about the state
of things in yaml format. __showin__ lets you drill in if you like.


### Get

It's the first command you'll want to do when you plug in.

This is the command we use to populate our _usb device_, _board type_ and _device-id_.
Various particle commands need the id, and we need the usb device so we know
who to wait for. It uses `particle serial list` for it's data.

The first thing to do is a __list__ and a __get__ or just a __get__. From there
the device id board type and usb device should be known. They will be used
for other commands in the process.

If you know particle commands then those should make sense, this is a small subset of the
possibilities. 

The REPL will do whatever you ask, so _help_, _show_, _list_, _identify_, 
_update_, _set-setup-done_, etc. Some which require a bit more, such as entering _dfu_ 
or _listen_ mode, are wrapped up together for convenience, but also available as
commands themselves.


## Particle.io Lights.
Something very important for knowing the state of your Particle.io boron.

[The meaning of the lights on a Particle.io Boron.](https://docs.particle.io/tutorials/device-os/led/boron/)


## The modules, core.py, particle.py, and Config.

The more complex functions are in core.py, These are functions which 
interact with the Application state as well as the device. 
This is also where the symbol tables are defined.

There is very little in the particle.py module. These are all of
the basic particle-cli commands I've used so far. All of these functions are
here to be as close to bare particle-cli commands as can be. I combined some 
things, like flash always does dfu first, identify always does a listen. 
Get is perhaps the most complex as it does wait and poll to give a chance 
for a reset or a plug.

The rest of the functions can actually live in the configuration file. 
It is only necessary to modify python code if there is a desire for more 
base functionality.

# Current state

__flash-test__, __flash-image__, __flash-tinker__, are working, but through 
os.popen().read() instead of subprocess like everything else.  I don't have an
explanation, subrocess needs more configuration for these commands. I've 
tried _shell=True_ with no change. So it's going be down in the details somewhere.

I had thought that perhaps using the particle.get_w_wait function to wait for the device could
work nicely, but it does not. So what we have are the best of what I've thought of, it
works, so there is not a lot of motivation yet.



