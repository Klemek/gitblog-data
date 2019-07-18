# How to create a (slow) interpreter - Part 1: Tokens

![thumbnail](thumbnail.jpg)
*Vue.js minified code highlight on Webstorm*

Before reading this article, I strongly recommend you to read __[How to create a (slow) interpreter - Introduction](/2019/07/09/how_to_create_a__slow__interpreter___introduction/)__.

Last time, we had a simple syntax to our language, it's now time to get our hands dirty and start writing some code.  

## Now you're thinking with tokens

First we need to think about what our interpreter needs to compute.
As an input, we will feed it a text containing the code and as an output it will either return a list of errors or a text output.
We must ask ourselves how it will read this initial text and understand commands.

It's already pretty obvious regarding how we defined the syntax that we can safely split along the line breaks to get the instructions lines.
So let's take that for granted.

When you read a text like `The cat is blue`, you can easily count words as we are familiar with this type of sentences.
Now imagine we happen to read the line `VAR A = 169`, how many words do you see ?
That's a tricky question, answers may vary considering how you are reading this.
Some may argue that only `VAR` is a valid word, others would say that there are 2 or 3.

Since we cannot define instructions from words, we will use another object that hold information: **tokens**. In the last example we can see 4 tokens:

* `VAR`: a word of 3 letters
* `A`: a word of 1 letter
* `=`: a symbol
* `169` a number

Let's try that on harder example: `WHILE var != var2 + 1 && var < (5.2 - var3) ^ -2`. How many tokens do you think there are ?

<details><summary>And the anwser is... (click)</summary><p>

If you guessed 16, you were right, the full decomposition is :

`WHILE`, `var`, `!=`, `var2`, `+`, `1`, `&&`, `var`, `<`, `(`, `5.2`, `-`, `var3`, `)`, `^`, `2`

</p></details>

Working on this case, the first rule we realize is that splitting along spaces will not work (and should not work) as, for example, `VAR A=169` has a valid syntax.
We can breakup "tokenizing" into these 5 rules :

* A word is starting with a letter and can contains letters, numbers and underscores, like built-in commands `WHILE`, `IF` or variable names `myAwesomeVar_12`.
* A list of symbols are acting as separators like `(` or `+`.
* Some symbols must be merged together like `&&` or `>=`.
* Numbers are digits and can have a floating point or a leading sign like `-2.03`.
* Spaces are meaningful expect between 2 words: we can shrink `A +` but not `IF A`.

Following these information, we can start writing our `tokenize` function that will split an instruction line into meaningful tokens.