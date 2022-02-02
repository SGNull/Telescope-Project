# Telescope Project

This is a personal project of mine that is still being developed, and probably will be for ~~a few months~~ quite some time.

I had a lot of different, rather big goals for this project. Here are just a few of them:
1. Design a CPU with a simple yet robust ISA capable of running a simple OS.
2. Write a fully-functional assembler that can run ON the CPU.
3. Write a lightweight and small-scale operating system.
4. Integrate the assembler into a file system on top of the OS.
5. Design a simple networking architecture, and write software for a router.
6. Hack a machine over the network (as a final and interesting test of everything).

I came up with this idea as a result of a few different factors. First, I created a project a few years ago that was much more successful than I had planned, where I wrote a basic assembler on a CPU and created a basic computer network, all from scratch. I've done something similar a few times now, but that project was the most successful by-far. Second, well, I've done this a few times now. I've become very familiar with designing small-scale CPUs and I want to do something bigger. Finally, I took an operating systems course last semester, and I already have a high-level description of a basic OS that should be able to run on this CPU. It will support multiprogramming & semaphores, variable process memory usage, and it simulates I/O interrupts at the software level, even though the CPU doesn't have (many) interrupts at the hardware level. 

This project went through a few big phases of redesign, including a major one towards the beginning of the project which involved effectively redoing the entire project up to the assembler. However, I'm very glad I went through with this, as it has taught me so much along the way that I never would have learned otherwise.

A complete description of the project is currently in the works over on [Overleaf](https://www.overleaf.com/read/gyrcwfqhfsrf), though I'm not sure when exactly it will be complete. There's a lot to talk about, and I want to make sure that as much of it is in the writeup as necessary.
