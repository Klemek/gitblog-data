# How to create an interpreter : introduction

Have you ever considered creating your own language ? With it's own features and syntax ? If the answer is yes, maybe you should read another article where you can learn an efficient way of doing so. If you're here by curiosity, tighten your seatbelt and find a drink, we're going on a ride.

## How I got here

Several month ago, I was in this project with friends where we had to make a choice between these 3 options :
* make a full scratch-like interface to allow programming with building blocks
* allow user to use a known language with its own potential backdoors that could threaten our server.
* create our own limited but complete language

As you can guess, the third option was the one we did choose after all as we had the motivation and the energy to do it in 4 to 5 months. The goal was to generate math problems from templates written by teachers in a not so complicated language.

Back then, we didn't know there are tools to do that task from your own design and choices, but we were young and ignorant (we still are by the way) and nothing is more formative than doing it from scratch (keep repeating that to reassure your manager, 100% success rate).

I took this task myself to let others handle front-end and back-end development of our service and because I was also eager to create something of my own. After the some months, here is what this language was doing :
* Variable attributions
* Conditions, loops
* Formal expression computing and common math functions
* LaTeX expression output with variables injection
* Custom ternary inside output
* Matrix creation and handling (indices, vectors, other stuff)
* Seeded random functions

You can see the working interpreter [here](https://github.com/Klemek/Red-Juice).

I discovered a lot of things during this project and I wanted to took this opportunity to discuss it with anyone interrested.

We will be creating during this blog post a small but efficient language interpreter for a language with a minimal syntax.
It will be close to the one mentionned before but with far less features for the post simplicity.

## First step, syntax

Ok first thing first, we will be working on an interpreted language, not a compiled one. The difference is simple : we don't need to create a bytecode to be read by the computer. In fact, it will be as simple as reading it from a human prespective : a cursor will jump along the lines and decide where to go next while a memory will retain variables known during the execution. There will be 2 major steps :

* Code error detection
* Code execution (if the last step was successful)

By doing so, we don't need to do the horrible task of throwing exceptions.

Looks like it's time to make some choices :
* Each line is a single statement : no semi-colon for delimitting (like python)
* Variable assignement and modification : `VAR` keyword
* Conditions : `IF`, `ELSEIF`, `ELSE` and `ENDIF` keywords
* Loops : `WHILE` and `ENDWHILE` keywords
* Output : `PRINT` keyword with brackets for formatting

To summarize, the following code :
```
VAR A = 169
VAR B = 585
PRINT GCD({A}, {B})
VAR D = 0
WHILE A != B
    IF A > B
        VAR A = A - B
    ELSE
        VAR B = B - A
    ENDIF
    PRINT = GCD({A}, {B})
ENDWHILE
PRINT = {A}
```
Will output :
```
GCD(169, 585)
= GCD(169, 416)
= GCD(169, 247)
...
= GCD(13, 26)
= GCD(13, 13)
= 13
```

I think we're good to go.

See you next time for the part 1 : Tokens.
