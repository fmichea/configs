README for kushou's configuration files
=======================================

First of all, thank you for reading this README file. I am writting this
because I would like to thank some people, and help you configure your own
system using these files.

Introduction
------------

* Project by: [Franck Michea][1]
* Developpement repository on [bitbucket][2]

Introduction - Global Structure
-------------------------------

This repository is mostly composed of dot-files. They are intended to configure
softwares like *zsh*, *awesome wm* or *vim*. A lot of this files include stuff
missing of this repository. These are either softwares or specific system
configuration file (names *stuff_opt*).

Specific configuration files are included only if present, and permits you to
add configuration on several computers without pushing it to your repository.

The following list is a list of programs used by the configuration and
configured at the time I am writing this README. I'll try to keep it updated.

### Configured

* [rxvt-unicode][3] - Terminal emulator
* [zsh][4] - Powerful shell
* git, mercurial - DCVS
* i3, i3status - i3 WM suite (tiling window manager).
* vim - Text editor

### Used programs (dependencies)

* synclient - Synaptics driver options
* feh - Sets wallpaper

Obviously, any of the programs used are not mandatory. They are only used by
the configuration and you can replace them whenever you want.

Special Thanks
--------------

If I wanted to thank every author of every article I read to help me write this
configuration, I would be really embarrassed. But I can especially thank these
people (in no particular order):

* anrxc and tdy for there awesome configuration, found on awesome's wiki. They
  really helped me build mine.
* delroth, for his vim configuration. I saved a lot of time "forking" his own
  configuration to build mine.
* Ph1l!'s for his ZSH prompt that greatly inspired mine.
* ctaf (ctafconf) for some ideas of keybindings in zsh, directly inpired from
  his.
* jcorbin and all the contributors of zsh-git.

[1]: mailto:franck.michea@gmail.com
[2]: https://bitbucket.org/kushou/configs
[3]: http://software.schmorp.de/pkg/rxvt-unicode.html
[4]: http://www.zsh.org/
[5]: http://awesome.naquadah.org/
[6]: http://www.gnu.org/software/emacs/
[7]: http://mercurial.selenic.com/
