# mip: basic usage

Introduction: I'm Jeremy Magland and I'm here with Dan Fortunato. We are the developers of the mip package manager for MATLAB. In this video, we'll walk you through how to get started with mip to install and manage mip packages. In a follow-up video we will get more in depth on how you can create and share your own packages.

First, Dan, could you give a quick overview about why we created mip?

> Dan responds with the mip philosophy (precompiled MEX files, path management, etc)

Let's begin with installation. Dan, can you show us how to install mip from a fresh installation of MATLAB?

> Dan copies install command from website and installs mip.

Where is mip installed now?

> Dan answers

How would we uninstall mip?

> Dan shows uninstallation, then reinstalls.

How can I install a package, and what's the difference between installing and loading?

> Dan responds - includes install (chebfun?), load, unload

How does mip handle dependencies?

> Dan uninstalls chebfun, installs surfacefun -> shows that chebfun gets installed as a dependency, and that it gets loaded as a dependency as well.

So how would I know which packages are available to install?

> Dan explains that there four ways a channel can be hosted. In core channel, in a user channel, as its own repository, or on file exchange. For the core channel, you can see the available packages either by using "mip avail" command or by browsing the website. People can host their own channels as well. Show the labs channel on mip-org. Or you can host a mip package in its own repository without a channel. Show an example of that. It is also possible to install packages directly from file exchange.

So what's the advantage of a mip package compared to one that is on file exchange?

> Dan responds

Great. In our next video, we'll get into more detail about preparing and hosting mip packages. But for now, let's see some other features about managing packages in mip.

> Dan explains sticky, --with examples, versions, etc.

Could you show me an example where precompiled MEX binaries are automatically downloaded specific to your operating system?

> Dan shows this.

So as you can see, mip helps you avoid a lot of the headaches of installing and using matlab tools. In our next video, we'll show how you can create, manage, and host your own MATLAB packages using mip.