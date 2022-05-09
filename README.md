# Telescope Project

This is a personal project of mine that is still being developed, and probably will be for quite some time, given how well it has turned out.

I had a lot of different, rather big goals for this project. Here are just a few of them:
1. Design a CPU with a simple yet robust ISA capable of running a simple OS ~~in [Logisim](https://www.cburch.com/logisim/)~~ in [Digital](https://github.com/hneemann/Digital).
2. Come up with an assembly language for the CPU, that can enable large programs like operating systems.
3. Write a fully-functional assembler that can run ON the CPU.
4. Write a lightweight and small-scale operating system.
5. Integrate the assembler into a file system on top of the OS.
6. Design a simple networking architecture, and write software for a router.
7. Hack a machine over the network (as a final and interesting demonstration of everything).

However, there were a lot of things that I did not anticipate, like
- Poor assembler performance and optimizations
- Switching logic simulators mid-project
- Writing test programs
- Extra hardware needed for an OS
- Documentation
- Other class work
- Small tweaks, bugs, and errors that come with projects at this scale.

Though I am still working towards that final goal, a lot more stuff is necessary to get there.

## Why

I came up with this idea as a result of a few different factors. First, I created a project a few years ago that was much more successful than I had planned, where I wrote a basic assembler on a CPU and created a basic computer network, all from scratch. I've done something similar a few times now, but that project was the most successful by-far. Second, well, like I said, I've done this a few times now. I've become very familiar with designing small-scale CPUs and I want to do something bigger. Finally, I took an operating systems course last semester, and I already have a high-level description of a basic OS that should be able to run on this CPU. It will support multiprogramming & semaphores, variable process memory usage, and it simulates I/O interrupts at the software level, even though the CPU doesn't have (many) interrupts at the hardware level. 

This project went through a few big phases of redesign, including a major one towards the beginning of the project which involved effectively redoing the entire project up to the assembler. However, I'm very glad I went through with this, as it has taught me so much along the way that I never would have learned otherwise.

This project, like all of the projects that I've done up to this point, is about getting to the bottom of what makes computers work. It's also about doing things from scratch, but also not wasting too much time. This is why things like the self-assembler and bootloader exist, but also why the Python cross-assembler exists and why we are not doing this from the transistors up. As much as I love doing things from absolute scratch, it tends to waste a lot of time that would be better spent developing and exploring new ideas.

## Quick Guide

The Glass CPU is at the heart of the project. While originally being made in Logisim, I moved the design over to Digital due to speed concerns. I find it rather simple to work with, given the limited pins and the assembly language that I developed for it.

The assembly language, called Telescope Assembly Light or TASL, has gone through numerous iterations. The syntax highlighting is all done through [Notepad++](https://github.com/notepad-plus-plus/notepad-plus-plus) and it's User Defined Language feature. Here's a quick (non-functional) example of how the language works:
```
JMP >Init
/ The language supports comments
/ You should always start your .tasl file with a jump to init or some equivalent
/ This is because any variables or data you create is placed directly where you define it in memory.

#MyLabel
MOV RG0, RG1

JMP >MyLabel

% 
  The language differentiates between "important" and "unimportant" characters.
  Lexemes, important strings, are comprised of important characters, and are seperated by unimportant characters.
  This allows for flexibility in how users write code, but places further emphasis on the user to make their code readable.
  The hope is that this flexibility will allow users to write much tidier code than normal assembly langauges support.
% 

#MyVariable = 2
#MyHex = 0x234F

@MY_CONSTANT = 5
@MY_OTHER_CONST = 'H'
#MyEmptyArray = (~MY_CONSTANT)  / An empty array of size MY_CONSTANT
#MyArray = (24, 'a', 'b', 15, 0x1, 0b010110)
#MyString = "Hello World!"

(#MyFoldableFunction
    LDI RG1 >MY_CONSTANT
    LOD RG0 RG1 >SomeArray
    JIF NEZ >NextLoop
    MOV IO RG2
    HLT
)

%
  Looking under the hood, you might be surprised at how simple the assembler sees the above code.
  Due to this, a "lexical compressor" was added to the Python assembler which reduces files into just their lexemes.
  This is useful for "importing", which can be done by copying the contents of multiple files together into a temporary file.
  By generating compressed versions of the files beforehand, the temporary file's size can be reduced and speed up assembling.
%
```

After writing your .tasl file, you can run it through the Python assembler for convenience, or through the self-assembler if you want to see it work. The Python assembler will take your file as an argument, and return a .tlo.hex file. Originally they were just .tlo files, but Digital only accepts .hex files (or else it really messes with the memory contents). After the file, you can specify -d, -c, or -l. 

-d will run the assembler in "debug mode," something which is not available in the self-assembler due to the lack of a file system to work with. Debug mode not only assembles your file, but produces a symbol .table file, and a reduced .rtl version of your code for following along line by line. 

-c instead of assembling, will run the "lexical compressor" and return a .tl "compressed" file.

-l is actually available in the self-assembler via the @GENLOADABLE constant. This will create a .tload file, which can be ran by the bootloader (but NOT directly on the CPU. It will probably halt, but it might also really mess up your program).

The bootloader idea came about back when I was working in Logisim, because the contents of RAM have to be re-loaded every time. While Digital does support automatically loading the RAM, _*I*_ don't. This is a realistic challenge, so I developed a bootloader machine which can be used in any computer system. It's identical to the CPU, except it supports ROM chips and not RAM chips. These ROM chips must be in the .tload format in order to be ran.

## Documentation

Most of the documentation can be found on [Overleaf](https://www.overleaf.com/read/gyrcwfqhfsrf), and that is where all of the major documents will be. There's also some miscellaneous documents scattered around the directories which are more technical. What I consider to be the most important document, the Need-To-Know, is in this directory along with the readme.

Getting back to the major documents, a complete CPU description is available on the Overleaf project: CPU Principles of Operation. There's also a "main" file which was the initial project-proposal document, and I've edited it a bit since then. I also started working on a complete description for TASL, but that's still in the works.

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


