#Telescope Project

This is a personal project of mine that is still being developed, and probably will be for a few months.

I had a lot of different, rather big goals for this project. Here are just a few of them:
1. Design a CPU with a robust ISA capable of running a simple OS.
2. Write a fully-functional assembler that can run ON the CPU.
3. Write a lightweight and small-scale operating system.
4. Integrate the assembler into a file system on top of the OS.
5. Design a simple networking architecture, and write software for a router.
6. Hack a machine over the network (as a final and interesting test of everything).

I came up with this idea as a result of a few different factors. First, I created a project a few years ago that was much more successful than I had planned, where I wrote a basic assembler on a CPU and created a basic computer network, all from scratch. I've done something similar a few times now, but that project was the most successful by-far. Second, well, I've done this a few times now. I've become very familiar with designing small-scale CPU's and I want to do something bigger. Finally, I just came out of an operating systems course, and I already have a high-level description of a basic OS that should be able to run on this CPU. It will support multiprogramming & semaphores, variable process memory usage, and it simulates interrupts at the software level, even though the CPU doesn't have interrupts at the hardware level. 

This project went through a big re-design, which simplified the architecture greatly and resulted in me being behind schedule. Also, I vastly underestimated the difficulty of writing an assembler which supported constants, arrays, and labels, in addition to normal instructions, in addition to writing it in the assembly language it was assembling. This put me way, way behind schedule from where I wanted to be. To solve this problem, I ended up writing a python script in a style very close to the assembly language. This way I can use the python assembler as a test, then write the actual assembler based on that and use the python one to generate the machine code.