# Telescope Project

This is a passion project of mine that is still being developed, and probably will be for quite some time given how well it has turned out.

I had a lot of different, rather big goals initially. So far most of them have been accomplished, but here are some of my current big goals:
- Networking
- Hacking over the network
- Workstation setup inside the simulation
- Streamlined user experience
- Possible LLM integration?

Right now, the GitHub repo and the entire underlying philosophy of this project are going through some big changes. I got extremely burnt out from how rigid and time-consuming everything became, and I'm trying to address those issues through large-scale reworks and a re-thinking of the entire project's purpose.

## Why

I created a project a few years ago that was much more successful than I had planned, where I wrote a basic assembler on a CPU I made and created a basic computer network, all from absolute scratch! I've done something similar a few times now (except for [boostrapping](https://en.wikipedia.org/wiki/Bootstrapping_(compilers)) an assembler from machine code and making a computer network) since 2015, which is the second reason for this project. I've become very familiar with designing small-scale CPUs and building small projects on top of them, and I wanted to do something bigger. Finally, I took an operating systems course back in 2021, and I found a few ways the OS we studied could be optimized to work with much less memory and processing power. After realizing that, it was hard to _not_ work on this project.

The project went through a few large redesigns/recreations, including a major one towards the beginning of the project which involved effectively redoing everything up to the assembler. However, I'm very glad I went through with this, as it has taught me so much about good coding practices and the importance of them.

This project, like all of the projects that I've done up to this point, is first and foremost a passion project. It is subject to change as my interests change. The point, as of right now, is to create, build on, and work within a simulated low-level software/hardware ecosystem, and to make it slightly less low-level over time.

## Project Overview

My unique Glass CPU powers this project. While originally created in [Logisim](http://www.cburch.com/logisim/), I moved the design over to [Digital](https://github.com/hneemann/Digital) due to simulation performance concerns. I find the CPU rather simple to work with, given the limited pins and the assembly language I developed for it. Some of its features are based off of [µMPS3](https://wiki.virtualsquare.org/#!education/umps.md).

On top of the CPU is the bootloader, which will automatically load a program from ROM when it is powered on. After loading it in, the bootloader switches control over to the CPU to execute it. This all happens very quickly now that the bootloader is pure hardware.

On top of the bootloader is the TCS, or Telescope Computing System. It comes with a few different types of I/O, and a relatively easy-to-use pin layout. It also has a few features that the CPU is lacking, like a computer status code, random number generator, cycle counter, and some I/O restrictions. The "OS" port of the TCS is for any program that you want to run when booting (usually TBOS).

The OS, called TBOS or Telescope Basic OS, is my attempt to shrink down and simplify [PandOS](https://wiki.virtualsquare.org/#!education/pandos.md) for the Glass CPU. Though as time has gone on, it has become clear that TBOS is more "inspired by" than a "recreation of" PandOS.

The assembly language this project uses is Telescope Assembly Light or TASL. It has gone through numerous iterations, tweaks, and modifications over the course of development, but change in it has slowed down over time. The syntax highlighting is all done through [Notepad++](https://github.com/notepad-plus-plus/notepad-plus-plus) and its User Defined Language feature. There are many more N++ features this project has, which create something like a mini IDE.

## Documentation

All of the main documentation can be found on [Google Drive](https://drive.google.com/drive/folders/1KU3_15fWw5ZkAqqLl0eGuVECFLYhDBbg?usp=sharing).

A good next step after the documentation is the "START HERE - Project Examples.txt" file. This contains some simple walkthroughs on how to make certain types of projects. It does not have nearly as much detail as the documentation, but it contains great supplimentary information.

## Github Workflow

Currently this part of the project is being completely revisited, so expect lots of changes.

I tried to be somewhat organized about how I do things on Github for this project, so here's how my workflow goes:
- Issues are for ideas or problems I am not actively working on, and for discussing their progress if necessary. I organize them in three ways:
  - Issues are pinned if they are currently being worked on.
  - Labels are used to provide a quick, easy-to-see category for the issue.
  - Milestones are used when there's a clear goal I have, and when a given issue is in service of that goal.

- As I am working on a particular issue or set of issues, other things tend to change.
  - I **try** to keep track of all noteworthy changes to the project as they happen.
  - This changelog, along with some additional comments, are placed in the **commit descriptions**.
  - While many things might change, I try to minimize the scope of these changes.

- I am attempting to use branches to differentiate between in-progress "development" versions, and the working "main" versions.
