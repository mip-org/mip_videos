# mip: basic usage (revised outline)

Revised from `basic_usage.md` after the practice recording on 2026-11-10. The order follows what flowed well in that take. Each step gives Jeremy's line, then what Dan types and the points to make, so Dan does not have to work it out on camera. Times in brackets are where that step happened in the practice take (`tutorial.mp4`), for reference.

## Before recording

- [ ] Start from a clean MATLAB: run `mip uninstall mip` (and remove any old mip from the path). Check that nothing like a manually installed chebfun is on the path (`which chebfun` should find nothing). In the practice take a leftover chebfun caused a detour at [6:15]. Use the same MATLAB version you cleaned up; mip saved in one version's path can show up in another.
- [ ] Dan shares the MATLAB window only (not the desktop), maximized, with a larger code font (Preferences → Fonts → Desktop code font).
- [ ] Have the install one-liner in the clipboard, so the website does not need to be on screen: `eval(webread('https://mip.sh/install.txt'))`
- [ ] Dan has this outline on a second screen or printed. Jeremy has it beside the call.
- [ ] Check the demo packages beforehand: an example repo for "own repository" and a File Exchange entry not already in core (see the TODOs below).

## 1. Introduction

**Jeremy:** I'm Jeremy Magland and I'm here with Dan Fortunato. We are the developers of the mip package manager for MATLAB. In this video, we'll walk you through how to get started with mip to install and manage mip packages. In a follow-up video we will get more in depth on how you can create and share your own packages.

## 2. Why mip? [0:33]

**Jeremy:** First, Dan, could you give a quick overview of why we created mip?

> Dan, no typing. Points (this went well in the take, keep it about this length):
> - Precompiled MEX files: mip installs a build for your machine's architecture, so no compiler is needed.
> - Path management: packages often need many folders, and their dependencies' folders, on the path. `mip load` does it, instead of ad hoc startup scripts.
> - Dependencies are resolved and installed automatically.
> - Decentralized: anyone can host packages (more in section 9).

## 3. Installing mip [2:23]

**Jeremy:** Let's begin with installation. Dan, can you show us how to install mip from a fresh installation of MATLAB?

> Dan pastes `eval(webread('https://mip.sh/install.txt'))` and presses Enter.
> - Read out what the wizard says it will do.
> - At "Enter install location", point out the default, `Documents/MATLAB/mip` (MATLAB's `userpath` plus `mip`), and press Enter.
> - Then run `mip help` and point out that this is where to start.
>
> This also answers "where is mip installed" from the old outline; no separate question needed.

## 4. Uninstalling mip [3:36]

**Jeremy:** And how would we uninstall mip?

> `mip uninstall mip`
> - mip manages itself as a package, so uninstalling it is just `mip uninstall` with its own name.
> - Read the warning: it unloads and deletes every installed package, removes mip from the saved path, and deletes the mip root folder. Confirm.
>
> Then reinstall it with the same one-liner: "If we want it back, we just run this again."

## 5. Installing and loading a package [4:30]

**Jeremy:** Now show us how you would install and load a package.

> ```matlab
> mip install chebfun
> chebfun          % error: unrecognized function or variable
> mip load chebfun
> chebfun          % now works
> path             % chebfun's folder was added for us
> mip list
> mip unload chebfun
> mip list
> ```
> - When installing: mip looks in its core channel, detects the architecture (Apple Silicon here), finds no dependencies, and installs. Chebfun is pure MATLAB, so the architecture does not matter for it.
> - After install, it is on disk under the mip root, but not on the path yet. That's what `mip load` is for.
> - `mip list` shows what is loaded and what is installed. The `*` marks packages you loaded directly.
> - After `mip unload` it is still installed, just not on the path.

## 6. Why install and load are separate [8:36]

**Jeremy:** Typically in MATLAB there's no distinction between installing something and loading it. Why does mip have two separate operations?

> Dan, no typing. Points (from the take; it was a good answer):
> - MATLAB has one global namespace: anything on the path is visible, and the first match wins.
> - With many packages on the path, names collide and one package can shadow another.
> - So you can have many packages installed, but only put on the path the ones you are using.
> - Scripts can start with `mip load ...` (and end with `mip unload ...`) to be self-contained, without downloading anything or changing the environment for good.

## 7. A package with MEX files [11:22]

**Jeremy:** Chebfun doesn't come with any MEX files. Could you show an example of a package that does, where the binaries for your operating system are downloaded automatically?

> ```matlab
> mip install finufft
> mip load finufft
> mip test finufft
> which finufft    % the MEX file, e.g. finufft.mexmaca64, inside the mip root
> ```
> - When installing: point out the architecture it detected and that it downloaded the Apple Silicon build.
> - `mip test` runs the test script each package comes with. Here it calls the MEX files.
> - Use `which finufft` (the MEX file is named `finufft`, like the package). Skip `which finufft_plan`, which is a `.m` file and was a detour in the take [13:42].
> - Don't use `mip info finufft` to show the installed build: it does not show it yet (to be fixed in mip).

## 8. Dependencies [17:52]

**Jeremy:** Package managers for other languages handle dependencies as a core part of how they work. How does mip handle dependencies?

> Start with nothing extra installed (`mip uninstall chebfun` if it is still there).
> ```matlab
> mip info surfacefun      % not installed; depends on chebfun
> mip install surfacefun   % plan: chebfun, then surfacefun
> mip list
> mip load surfacefun      % loads chebfun as well
> path                     % chebfun ahead of surfacefun, plus surfacefun's 2 folders
> mip list                 % * next to surfacefun only
> mip unload surfacefun    % "Unloading transitive dependencies: chebfun"
> mip uninstall surfacefun % removes chebfun too, since nothing needs it
> ```
> - Point out that we never asked for chebfun: mip worked out it was needed.
> - In `mip info`, "Dependencies (latest)" means the dependencies of the newest available version.
> - **Don't `mip load chebfun` directly in the middle of this.** Loading a package directly also marks it as directly installed, so uninstalling surfacefun would then keep chebfun. That was the long detour in the take [21:53–26:21]. To show that a package you want yourself is kept, use `mip install chebfun` instead, and expect it to say only "already installed".
>
> Then the bigger example, which went well:
> ```matlab
> mip install chunky       % installs fmm2d (MEX) and flam (pure MATLAB) first
> mip unload --all
> path                     % just mip and MATLAB's own
> mip load chunky
> path                     % all of the dependencies' folders, added for us
> mip test chunky          % solves a PDE
> mip uninstall chunky     % cleans up fmm2d and flam
> ```
> - "This is where automatic path management pays off": no remembering which startup scripts to run, or in what order.

## 9. Where packages come from [15:40]

**Jeremy:** How would I know which packages are available to install? Are these the only ones?

> There are four ways a package can be hosted. Show each one:
>
> 1. **The core channel**, which we curate. `mip avail` lists it, and https://mip.sh lists the same packages. Explain: a channel is a GitHub repository of packages (core is `mip-org/core`), like Homebrew taps or conda channels.
> 2. **Other channels**: anyone can host one. Show the labs channel:
>    ```matlab
>    mip avail --channel mip-org/labs
>    mip install --channel mip-org/labs matnwb
>    ```
>    Mention `mip channel add mip-org/labs` to subscribe, so plain names are found there too.
> 3. **A package in its own repository**, with no channel:
>    ```matlab
>    mip install <owner>/<repo>
>    ```
>    TODO: we need a real example repo. mip-org/hello_mip is not published that way yet. It needs `mip init -g` and a `v0.1.0` tag first.
> 4. **File Exchange**, directly:
>    ```matlab
>    mip install https://www.mathworks.com/matlabcentral/fileexchange/<id>-<name> --name <name>
>    ```
>    TODO: pick an entry that is a zip and not already in core (`export_fig` is in core, so it would be a confusing example).

## 10. Compared with File Exchange [28:45]

**Jeremy:** Before mip, I would download packages from File Exchange. What's the advantage of using mip?

> Dan, no typing (this was a good answer). Points:
> - File Exchange: open the browser, download a zip, extract it somewhere, add folders to the path (maybe recursively), maybe run a startup script. mip does all of that in one command, and can even install straight from a File Exchange URL (just shown).
> - MATLAB's toolbox and add-on framework is heavy, and it is hard to see what is installed. mip is a small command line, like a terminal.
> - mip can update packages and use specific versions (next section).

## 11. Other features [31:20]

**Jeremy:** In our next video, we'll get into more detail about preparing and hosting mip packages. But for now, are there other features about managing packages you'd like to show?

> The take ran out of steam here. Script it:
> ```matlab
> % Sticky: stays loaded through "mip unload --all"
> mip load chebfun --sticky
> mip unload --all
> mip list                 % chebfun still loaded, marked [sticky]
>
> % Optional groups of folders, such as examples
> mip info surfacefun      % "Extra paths" lists its groups
> mip load surfacefun --with examples
>
> % Versions and updates (treeweave in the labs channel has several versions)
> mip info --channel mip-org/labs treeweave
> mip install --channel mip-org/labs treeweave@0.0.3
> mip update treeweave     % moves to the newest version
> mip pin treeweave        % pinned packages are skipped by mip update
> mip help                 % everything else
> ```
> - Don't use `mip load chebfun --with examples`: chebfun's groups are `demos` and `tests`.
> - Check the treeweave versions in the live index before recording.

## 12. Closing

**Jeremy:** So as you can see, mip helps you avoid a lot of the headaches of installing and using MATLAB tools. In our next video, we'll show how you can create, manage, and host your own MATLAB packages using mip. Thanks for watching.

(In the take the last line came out as "using MATLAB"; it should be "using mip".)
