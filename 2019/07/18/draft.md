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
We can breakup "tokenizing" into these 6 rules :

* A word is starting with a letter and can contains letters, numbers and underscores, like built-in commands `WHILE`, `IF` or variable names `myAwesomeVar_12`.
* A list of symbols are acting as separators like `(` or `+`.
* Some symbols must be merged together like `&&` or `>=`.
* Numbers are digits and can have a floating point like `2.03`.
* Numbers and variables can have a leading leading sign like `-2` or `-varA`.
* Spaces are meaningful expect between 2 words: we can shrink `A +` but not `IF A`.

Following these information, we can start writing our `tokenize` function that will split an instruction line into meaningful tokens.

## Divide and conquer

```javascript
/**
* split a string expression into tokens
* @param {string} exp
* @return {string[]} tokens
*/
function tokenize(exp){
```

So as we said before, there are 2 types of spaces: between words and others.
We need to differentiate both by changing the first temporarily.
We can also declare an output list and a variable keeping the first index of a word.

```javascript
//save the space between 2 a-z words by replacing it with ¤ and ditch other blank spaces
const exp2 = exp.replace(/([a-zA-Z0-9_]*)[\\s]([a-zA-Z0-9_]*)/g, '$1¤$2')
                .replace(/[\\s]/g,'') // remove blank chars
                .replace(/¤/g,' '); // recover saved space
const output = []; // saved tokens
let i0 = 0; // start of a word
```

We will now iterate over each characters the following way :

<small>

```
    VAR var2=169
        ^             start of word at i0=4
    VAR var2=169
        |^            letter of a word
    VAR var2=169
        | ^           letter of a word
    VAR var2=169
        |  ^          letter of a word
    VAR var2=169
        |   ^         new word 'var2' starting at i0=4
```

</small>

So a `for` loop is perfect for this task

```javascript
for (let i = 0; i < exp2.length; i++) {
```

# TODO

<details><summary>Full `tokenize` function (click)</summary><p>

```javascript

/**
* split a string expression into tokens
* @param {string} exp
* @return {string[]} tokens
*/
function tokenize(exp){
  //save the space between 2 a-z words by replacing it with ¤ and ditch other blank spaces
  const exp2 = exp.replace(/([a-zA-Z0-9_]*)[\s]([a-zA-Z0-9_]*)/g, '$1¤$2')
                  .replace(/[\\s]/g,'')
                  .replace(/¤/g,' ');
  const output = []; // saved tokens
  let i0 = 0; // start of a word
  for (let i = 0; i < exp2.length; i++) {
    if ('+-*/%^()=&| ><!'.includes(exp2[i])) { // if current char is separator
      if (i > i0) // save token before
        output.push(exp2.substr(i0, i - i0).trim());
      if (exp2[i] !== ' ') // save separator as token if not word separator
        output.push(exp2[i]);
      i0 = i + 1;
    }
  }
  if (i > i0) // save last token
    output.push(exp2.substr(i0, i - i0).trim());
  
  const testMerge = function(a,b){
    return ('&|='.includes(a) && a.length === 1 && a === b) || // double separator
      (b === '=' && '!<>'.includes(a) && a.length === 1);// >= or <= or !=
  };

  // join two separators of same char in output
  for (let i = output.length - 1; i > 0; i--) {
    if (testMerge(output[i - 1], output[i])) {
      output[i - 1] += output[i];
      output.splice(i, 1);
    } else if ('+-*/%^=&|><(!'.includes(output[i - 1]) && output[i] === '-') {
      output[i] = '.-';
    }
  }
  return output;
}

```

</p></details>

Testing:
```javascript
console.log(tokenize('VAR A = 169').join('  /  '));
console.log(tokenize('WHILE var != var2 + 1 && var < (5.2 - var3) ^ -2').join('  /  '));
```

Console output from your browser:  
> <span id="output"></span>

<script>
function log(...args){
  console.log(...args);
  document.getElementById('output').innerHTML += args.map(x => x.toString()).join(' ')+'<br>';
}
function tokenize(exp){
  //save the space between 2 a-z words by replacing it with ¤ and ditch other blank spaces
  const exp2 = exp.replace(/([a-zA-Z0-9_]*)[\s]([a-zA-Z0-9_]*)/g, '$1¤$2')
                  .replace(/[\\s]/g,'')
                  .replace(/¤/g,' ');
  const output = []; // saved tokens
  let i0 = 0; // start of a word
  let i;
  for (i = 0; i < exp2.length; i++) {
    if ('+-*/%^()=&| ><!'.includes(exp2[i])) { // if current char is separator
      if (i > i0) // save token before
        output.push(exp2.substr(i0, i - i0).trim());
      if (exp2[i] !== ' ') // save separator as token if not word separator
        output.push(exp2[i]);
      i0 = i + 1;
    }
  }
  if (i > i0) // save last token
    output.push(exp2.substr(i0, i - i0).trim());
  
  const testMerge = function(a,b){
    return ('&|='.includes(a) && a.length === 1 && a === b) || // double separator
      (b === '=' && '!<>'.includes(a) && a.length === 1);// >= or <= or !=
  };

  // join two separators of same char in output
  for (let i = output.length - 1; i > 0; i--) {
    if (testMerge(output[i - 1], output[i])) {
      output[i - 1] += output[i];
      output.splice(i, 1);
    } else if ('+-*/%^=&|><(!'.includes(output[i - 1]) && output[i] === '-') {
      output[i] = '.-';
    }
  }
  return output;
}

log(tokenize('VAR A = 169').join('&nbsp;&nbsp;/&nbsp;&nbsp;'));
log(tokenize('WHILE var != var2 + 1 && var < (5.2 - var3) ^ -2').join('&nbsp;&nbsp;/&nbsp;&nbsp;'));

</script>