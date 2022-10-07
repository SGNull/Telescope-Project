# Telescope Project

This is a personal project of mine that is still being developed as of October of 2022, and probably will be for quite some time given how well it has turned out.

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

I came up with this idea for a few different reasons. First, I created a project a few years ago that was much more successful than I had planned, where I wrote a basic assembler on a CPU and created a basic computer network, all from scratch. I've done something similar a few times now over the past 7 years, but that project was the most successful by-far. Second, like I said previously, I've done this a few times now. I've become very familiar with designing small-scale CPUs and I want to do something bigger. Finally, I took an operating systems course back in 2021, and I found a few ways the OS we studied could be optimized to work on a small-scale CPU. It will support multiprogramming & semaphores, variable process memory usage, and it will simulate I/O interrupts at the software level, even though the CPU doesn't have (many) interrupts at the hardware level. After realizing that the OS could be simplified in such a way, it was hard to not work on this project.

This project went through a few big phases of redesign, including a major one towards the beginning of the project which involved effectively redoing the entire project up to the assembler. However, I'm very glad I went through with this, as it has taught me so much along the way that I never would have learned otherwise.

This project, like all of the projects that I've done up to this point, is about getting to the bottom of what makes computers work. It's also about doing things from scratch, but also not wasting too much time. This is why things like the self-assembler and bootloader exist, but also why the Python cross-assembler exists and why we are not doing this from the transistors up. As much as I (really really) love doing things from absolute scratch, it tends to waste a lot of time that is better spent developing and exploring new ideas.

## Project Overview

The Glass CPU is at the heart of the project. While originally created in Logisim, I moved the design over to Digital due to simulation performance concerns. I find it rather simple to work with, given the limited pins and the assembly language that I developed for it. Some of the features present in the Glass CPU are based off of [µMPS3](https://wiki.virtualsquare.org/#!education/umps.md).

On top of the CPU is the bootloader, which will automatically load a program in from ROM when it is powered on. After loading it in, the bootloader switches control over to the CPU to execute it.

Finally, on top of the bootloader is the TCS, or Telescope Computing System. It comes with a few different types of I/O, and a relatively easy-to-use pin layout. It also has a few features that the CPU is lacking, like a PC status code, random number generator, cycle counter, and kernel restrictions on I/O devices ending in 00. The one port of the TCS says it's for the OS, but it's really for any program you want the bootloader to run first.

The OS, called TBOS or Telescope Basic OS, is the shrunk down and simplified version of [PandOS](https://wiki.virtualsquare.org/#!education/pandos.md). TBOS will, as of October 7th 2022, load and run the program from drive 0 as a user process. It supports loading a program from the given IO port (SYS 0), loading a program from the file system at the given I/O (SYS 1 w/ RG1 = file number), ending the process's CPU burst early (SYS 2), and terminating the current process (HLT, user interrupts, and any exception not yet supported). If everything runs correctly, the PC will stop with the code 0x600D.

The assembly language at the heart of this project is called Telescope Assembly Light or TASL. It has gone through numerous iterations over the course of development, and will probably continue to do so (though hopefully not as frequently). The syntax highlighting is all done through [Notepad++](https://github.com/notepad-plus-plus/notepad-plus-plus) and it's User Defined Language feature. Additionally, TASL now works with the N++ Function List feature, which displays the list of all functions in the given document. All this, along with some easy to use buttons, is why I often refer to the them together as the N++ Mini-IDE.

It is important to note that the bootloader and OS can only load "loadable" machine code files into RAM. Loadable files begin with their file size, allowing loaders to pull them into memory correctly and efficiently.

## Documentation

All of the main documentation can be found on [Google Drive](https://drive.google.com/drive/folders/1KU3_15fWw5ZkAqqLl0eGuVECFLYhDBbg?usp=sharing). As of October 7, 2022, the documentation is scattered about various files like the Need-To-Know, the TBOS description, source-code comments, hardware comments, and some random text files. I think it goes without saying that this is not good. It necessarily cannot be kept up-to-date when I'm not even sure where all references to a given feature are. This, on top of the confusion it undoubtedly causes for people new to the project, is why I'm beginning to localize and organize all documentation in the Google Drive project folder. It's also why I'm including dates with certain things I say about critical features.

## Github Workflow

I tried to be somewhat organized about how I do things on Github for this project, so here's how my workflow goes:
- I make issues when I see a problem or come up with an idea that I am not actively working on.
  - I try to provide issue descriptions with enough detail to come back to later.
  - If an issue is surprisingly big or takes time to fix, I'll leave comments detailing my progress.

- I organize issues in 4 ways:
  - Issues are pined if they are currently being worked on.
  - Labels are used to provide a quick, easy-to-see category for the issue.
  - Milestones are used when there's a clear goal I have, and when a given issue is in service of that goal.
  - Projects are used to break issues down into the main project categories like OS, Assembler, CPU, etc.

- As I am working on a particular issue or set of issues, other things tend to change.
  - I keep track of all noteworthy changes to the project as they happen.
  - This changelog, along with some additional comments, are placed in the **commit descriptions**.
  - While many things might change, I try to minimize the scope of these changes.


