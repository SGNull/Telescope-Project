# Telescope Project

This is a personal project of mine that is still being developed, and probably will be for quite some time given how well it has turned out.

I had a lot of different, rather big goals for this project. Here are just a few of them:
1. Design a CPU with a simple yet robust ISA capable of running a simple OS in ~~[Logisim](https://www.cburch.com/logisim/)~~ [Digital](https://github.com/hneemann/Digital).
2. Come up with an assembly language for the CPU, that can enable large programs like operating systems.
3. Write a fully-functional assembler that can run ON the CPU.
4. Write a lightweight and small-scale operating system.
5. Integrate the assembler into a file system on top of the OS.
6. Design a simple networking architecture, and write software for a router.
7. Hack a machine over the network (as a final and interesting demonstration of everything).

However, there were a lot of things that I did not anticipate or did not anticipate being so difficult, like:
- Senior year college assignments and projects
- Poor assembler performance and optimizations
- Switching logic simulators mid-project
- Writing test programs
- Extra hardware needed for an OS
- Writing documentation
- Keeping documentation up to date (surprisingly difficult)
- Small tweaks, bugs, and errors that come with projects at this scale.

Though I am still working towards that final goal, a lot more work is necessary to get there.

## Why

I came up with this idea for a few different reasons. First, I created a project a few years ago that was much more successful than I had planned, where I wrote a basic assembler on a CPU and created a basic computer network, all from absolute scratch (yes, even the assembler!). I've done something similar a few times now (minus [boostrapping](https://en.wikipedia.org/wiki/Bootstrapping_(compilers)) an assembler from machine code) since 2015, but that project was the most successful by far. The second reason for this project is exactly that; I've done this a few times now. I've become very familiar with designing small-scale CPUs and building small projects on top of them, and I wanted to do something bigger. Finally, I took an operating systems course back in 2021, and I found a few ways the OS we studied could be optimized to work on a small-scale CPU with much less memory. It would support multiprogramming & semaphores, variable process memory usage, and it could simulate I/O interrupts at the software level, even though the CPU doesn't have those interrupts at the hardware level. After realizing that the OS could be simplified in such a way, it was hard to _not_ work on this project.

The project went through a few large redesigns/recreations, including a major one towards the beginning of the project which involved effectively redoing everything up to the assembler. However, I'm very glad I went through with this, as it has taught me so much about good coding practices and the importance of them.

This project, like all of the projects that I've done up to this point, is about getting to the bottom of what makes computers work. It's also about doing things from scratch, but not wasting too much time. This is why things like the self-assembler and bootloader exist, but also why the Python cross-assembler exists and why we are not doing this from the transistors up. As much as I (really really) love doing things from absolute scratch, it tends to waste a lot of time that is better spent developing and exploring new ideas.

## Project Overview

The Glass CPU is at the heart of the project. While originally created in Logisim, I moved the design over to Digital due to simulation performance concerns. I find the CPU rather simple to work with, given the limited pins and the assembly language that I developed for it. Some of the features present in the Glass CPU are based off of [µMPS3](https://wiki.virtualsquare.org/#!education/umps.md).

On top of the CPU is the bootloader, which will automatically load a program in from ROM when it is powered on. After loading it in, the bootloader switches control over to the CPU to execute it. This all happens very quickly now that the bootloader is pure hardware (it used to rely on firmware, which greatly reduced its speed).

Finally, on top of the bootloader is the TCS, or Telescope Computing System. It comes with a few different types of I/O, and a relatively easy-to-use pin layout. It also has a few features that the CPU is lacking, like a computer status code, random number generator, cycle counter, and kernel restrictions on I/O devices ending in 00. One port of the TCS says it's for the operating system, but it's really for any program you want the bootloader to run first to control the computer.

The OS, called TBOS or Telescope Basic OS, is an attempt to shrink down and simplify [PandOS](https://wiki.virtualsquare.org/#!education/pandos.md). Though as time has gone on, it has become clear that TBOS is more "inspired by" than a "recreation of" PandOS. For a full list of features and syscalls, see the documentation for it [here](https://docs.google.com/document/d/1w4tGKG7OOmJUgn_xcEoIwMuiV4fEk35birdfAZGWwIo/edit?usp=sharing).

The assembly language at the heart of this project is called Telescope Assembly Light or TASL. It has gone through numerous iterations, tweaks, and modifications over the course of development, but change in it has significantly slowed down over time. The syntax highlighting is all done through [Notepad++](https://github.com/notepad-plus-plus/notepad-plus-plus) and its User Defined Language feature. Additionally, TASL now works with the N++ Function List feature, which displays the list of all functions in the given document. All this, along with the other features of N++ and some easy to use scripts, I often refer to as an IDE.

It is important to note that the bootloader and OS can only load "Loadable" machine code files into RAM. Loadable files begin with their file size, allowing loaders to pull them into memory correctly and efficiently.

## Documentation

All of the main documentation can be found on [Google Drive](https://drive.google.com/drive/folders/1KU3_15fWw5ZkAqqLl0eGuVECFLYhDBbg?usp=sharing). Originally, documentation was located within the project files themself, split across multiple directories. However, this became not just confusing, but unsustainable. This is why all documentation can be found on the Google Drive public directory (or within code comments).

A good next step after the documentation is the "START HERE - Project Examples.txt" file. This contains some simple walkthroughs on how to make certain types of projects. It does not have nearly as much detail as the documentation, but it contains great supplimentary information.

## Github Workflow

I tried to be somewhat organized about how I do things on Github for this project, so here's how my workflow goes:
- I make issues when I see a problem or come up with an idea that I am not actively working on.
  - I try to provide issue descriptions with enough detail to come back to later.
  - If an issue is surprisingly big or takes time to fix, I'll leave comments detailing my progress.

- I organize issues in 4 ways:
  - Issues are pinned if they are currently being worked on.
  - Labels are used to provide a quick, easy-to-see category for the issue.
  - Milestones are used when there's a clear goal I have, and when a given issue is in service of that goal.
  - Projects are used to break issues down into the main project categories like OS, Assembler, CPU, etc.

- As I am working on a particular issue or set of issues, other things tend to change.
  - I keep track of all noteworthy changes to the project as they happen.
  - This changelog, along with some additional comments, are placed in the **commit descriptions**.
  - While many things might change, I try to minimize the scope of these changes.

- I am attempting to use branches to differentiate between in-progress "development" versions, and the working "main" versions.

- Related to the above point, I'm also using this project as a way to better understand Git and optimal workflows, so the way this project interfaces with Git is likely to change in the future.
