# User Services
Here are a collection of user services I include in my environment, assuming the runit init system is being used (like in void linux)

In particular, I have the emacs service which I put in the .local folder.

I ensure that my wm init file runs the following command as a part of autostarting programs:
`runsvdir -P "${HOME}/.local/service/"`

That service directory needs to be created and is the runsvdir. I symlink the included emacs directory to that services dir. This allows the run script in the emacs directory to be executed, and has emacs run in daemon mode, as a service!


