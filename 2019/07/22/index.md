# How to create a (slow) interpreter - Part 1: Tokens

![thumbnail](thumbnail.jpg)
*Photo by [Andreas Brücker](https://unsplash.com/@andreasbruecker) on Unsplash*

[![Hacker News](https://img.shields.io/badge/dynamic/json.svg?color=green&style=flat-square&label=Hacker%20News&query=score&suffix=%20points&url=https%3A%2F%2Fhacker-news.firebaseio.com%2Fv0%2Fitem%2F20515595.json)](https://news.ycombinator.com/item?id=20515595) 
![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fblog.klemek.fr%2F2019%2F07%2F22%2F)

***

Before reading this article, I strongly recommend you to read __[How to create a (slow) interpreter - Introduction](/2019/07/09/how_to_create_a__slow__interpreter___introduction/)__.

Last time, we had a simple syntax to our language, it's now time to get our hands dirty and start writing some code.  

## Divide and conquer

First, we need to think about what our interpreter needs to compute.
As an input, we will feed it a text containing the code and as an output it will either return a list of errors or a text output.
We must ask ourselves how it will read this initial text and understand commands.

It's already pretty obvious regarding how we defined the syntax that we can safely split along the line breaks to get the instruction lines.
So let's take that for granted.

When you read a text like `The cat is blue`, we can easily count words as we are familiar with this type of sentences.
Now imagine we happen to read the line `VAR A = 169`, how many words do you see?
That's a tricky question, answers may vary considering how you are reading this.
Some may argue that only `VAR` is a valid word, others would say that there are 2 or 3 in total.

Since we cannot define instructions from words, we will use another object that holds information: **tokens**. In the last example we can see 4 tokens:

* `VAR`: a word of 3 letters
* `A`: a word of 1 letter
* `=`: a symbol
* `169` a number

Let's try that on harder example: `WHILE var != var2 + 1 && var < (5.2 - var3) ^ -2`. How many tokens do you think there are?

<details><summary>And the anwser is... (click)</summary><p>

If you guessed 17, you were right, the full decomposition is:

`WHILE`, `var`, `!=`, `var2`, `+`, `1`, `&&`, `var`, `<`, `(`, `5.2`, `-`, `var3`, `)`, `^`, `-`, `2`

</p></details>

Working on this case, the first rule we realize is that splitting along spaces will not work (and should not work) as, for example, `VAR A=169` has a valid syntax.
We can break up "tokenizing" into these 6 rules:

1. A word is starting with a letter and can contain letters, numbers and underscores, like built-in commands `WHILE`, `IF` or variable names `myAwesomeVar_12`.
1. Spaces are meaningless excepted between 2 words: we can shrink `A +` but not `IF A`.
1. Some symbols are acting as separators like `(` or `+`.
1. Numbers are digits and can include a floating point like `2.03`.
1. Some symbols must be merged together like `&&` or `>=`.
1. Numbers and variables can possess a leading leading sign like `-2` or `-varA`.*

> \* The last one is special as we will handle this task here and it will only be used later in another function.

Following these indications, we can start writing our `tokenize` function that will split an instruction line into meaningful tokens.

## Now you're thinking with tokens

```javascript
/**
* split a string expression into tokens
* @param {string} exp
* @return {string[]} tokens
*/
function tokenize(exp){
```

So as we said before, there are 2 types of spaces: between words and others.
We must differentiate both by changing the first temporarily.
We can also declare an output list and a variable keeping the first index of a word.

```javascript
// save the space between 2 a-z words by replacing it with ¤ and ditch other spaces
const exp2 = exp.replace(/([a-zA-Z0-9_]*)[\\s]([a-zA-Z0-9_]*)/g, '$1¤$2')
                .replace(/[\\s]/g,'') // remove blank chars
                .replace(/¤/g,' '); // recover saved space
const output = []; // saved tokens
let i0 = 0; // starting index of a word
```

We will now iterate over each character the following way:

<small>

```
    VAR var2=169
    ^                 i0=0
    VAR var2=169
    |^
    VAR var2=169
    | ^
    VAR var2=169
    |  ^              separator, new token: VAR
    VAR var2=169
        ^             i0=4
    VAR var2=169
        |^
    VAR var2=169
        | ^
    VAR var2=169
        |  ^
    VAR var2=169
        |   ^         separator, new tokens: var2, =  
    VAR var2=169
             ^        i0=9
    VAR var2=169
             |^
    VAR var2=169
             | ^
    VAR var2=169
             |  ^     end of string, new token: 169
```

</small>

So we will loop until we encounter a separator:

```javascript
let i;
for (i = 0; i < exp2.length; i++) {
  if ('+-*/%^()=&| ><!'.includes(exp2[i])) { // if current char is a separator
```

Whenever it happens, we first have to save the previous token if it exists.  
Next we save the separator as a token when it's not a space between words.  
Then we update the starting point of the following token.

```javascript
if (i > i0) // save token before
  output.push(exp2.substr(i0, i - i0));
if (exp2[i] !== ' ') // save separator as token if not a word separator
  output.push(exp2[i]);
i0 = i + 1;
}
```

At the end of the loop, let's not forget to save the remaining token:
```javascript
}
if (i > i0) // save last token
  output.push(exp2.substr(i0, i - i0));
```

Pretty easy, right? So where are we now?

1. <i class="fas fa-check green"></i> words aren't containing symbols*.  
1. <i class="fas fa-check green"></i> spaces are removed except between words.  
1. <i class="fas fa-check green"></i> symbols act as separators.  
1. <i class="fas fa-check green"></i> numbers can contains points. (as `.` is not in the symbol list)  
1. <i class="fas fa-times red"></i> symbols aren't merged. (`A!=B` became `A`, `!`, `=`, `B`)  
1. <i class="fas fa-times red"></i> inverse operation is not separated from subtraction.

> \* words might actually contain symbols if there aren't in the separators list (like `@`) but we will check their validity another time.

We now want to merge symbols when it's required. To do so, we will create a testing function that takes two neighbor tokens and checks their merge ability:

```javascript
const canMerge = function(a,b){
  return ('&|='.includes(a) && a.length === 1 && a === b) || // double separator
    (b === '=' && '!<>'.includes(a) && a.length === 1); // >= or <= or !=
};
```

We only need to iterate over our `output` list (in reverse to avoid index jumps) and merge whenever it's possible:

```javascript
for (let i = output.length - 1; i > 0; i--) {
  if (canMerge(output[i - 1], output[i]))
    output.splice(i - 1, 2, output[i - 1] + output[i]); // remove 2 elements and add merged
```

We will take this opportunity to iterate over the output to identify the inverse operation:

> Inverse operation is identified by a minus sign after a symbol except for closing parenthesis.
For example, in `(A-B)-C*-D`, only the final one is different.

```javascript
else if ('+-*/%^(=&| ><!'.includes(output[i - 1]) && output[i] === '-') 
  output[i] = '.-'; // differentiate this operation from subtraction
```

Now that all the rules are fulfilled, we can simply return our output:

```javascript
}
return output;
}
```

## 

We can now enjoy our fully working function:

<details><summary>Full `tokenize` function (click)</summary><p>

```javascript

/**
* split a string expression into tokens
* @param {string} exp
* @return {string[]} tokens
*/
function tokenize(exp){
  // save the space between 2 a-z words by replacing it with ¤ and ditch other spaces
  const exp2 = exp.replace(/([a-zA-Z0-9_]*)[\\s]([a-zA-Z0-9_]*)/g, '$1¤$2')
                  .replace(/[\\s]/g,'') // remove blank chars
                  .replace(/¤/g,' '); // recover saved space
  const output = []; // saved tokens
  let i;
  let i0 = 0; // starting index of a word
  for (i = 0; i < exp2.length; i++) {
    if ('+-*/%^()=&| ><!'.includes(exp2[i])) { // if current char is a separator
      if (i > i0) // save token before
        output.push(exp2.substr(i0, i - i0));
      if (exp2[i] !== ' ') // save separator as token if not a word separator
        output.push(exp2[i]);
      i0 = i + 1;
    }
  }
  if (i > i0) // save last token
    output.push(exp2.substr(i0, i - i0));
  
  const canMerge = function(a,b){
    return ('&|='.includes(a) && a.length === 1 && a === b) || // double separator
      (b === '=' && '!<>'.includes(a) && a.length === 1); // >= or <= or !=
  };
  
  for (let i = output.length - 1; i > 0; i--) {
    if (canMerge(output[i - 1], output[i]))
      output.splice(i - 1, 2, output[i - 1] + output[i]); // remove 2 elements and add merged
    else if ('+-*/%^(=&| ><!'.includes(output[i - 1]) && output[i] === '-')
      output[i] = '.-'; // differentiate this operation from subtraction
  }
  return output;
}

```

</p></details>

Let's test this out with the examples described above:
```javascript
console.log(tokenize('VAR A = 169').join('  /  '));
console.log(tokenize('WHILE var != var2 + 1 && var < (5.2 - var3) ^ -2').join('  /  '));
```

Here's the console output from the tests that just ran into your browser:
> <span id="output"></span>

<script>
function log(...args){
  console.log(...args);
  document.getElementById('output').innerHTML += args.map(x => x.toString()).join(' ').replace(/ /gm,'&nbsp;')+'<br>';
}

function tokenize(exp){
  // save the space between 2 a-z words by replacing it with ¤ and ditch other spaces
  const exp2 = exp.replace(/([a-zA-Z0-9_]*)[\\s]([a-zA-Z0-9_]*)/g, '$1¤$2')
                  .replace(/[\\s]/g,'') // remove blank chars
                  .replace(/¤/g,' '); // recover saved space
  const output = []; // saved tokens
  let i0 = 0; // starting index of a word
  let i;
  for (i = 0; i < exp2.length; i++) {
    if ('+-*/%^()=&| ><!'.includes(exp2[i])) { // if current char is a separator
      if (i > i0) // save token before
        output.push(exp2.substr(i0, i - i0));
      if (exp2[i] !== ' ') // save separator as token if not a word separator
        output.push(exp2[i]);
      i0 = i + 1;
    }
  }
  if (i > i0) // save last token
    output.push(exp2.substr(i0, i - i0));
  
  const canMerge = function(a,b){
    return ('&|='.includes(a) && a.length === 1 && a === b) || // double separator
      (b === '=' && '!<>'.includes(a) && a.length === 1); // >= or <= or !=
  };

  for (let i = output.length - 1; i > 0; i--) {
    if (canMerge(output[i - 1], output[i]))
      output.splice(i - 1, 2, output[i - 1] + output[i]); // remove 2 elements and add merged
    else if ('+-*/%^=&|><(!'.includes(output[i - 1]) && output[i] === '-')
      output[i] = '.-'; // differentiate this operation from subtraction
  }
  return output;
}

log('Time:',new Date());
log(tokenize('VAR A = 169').join('  /  '));
log(tokenize('WHILE var != var2 + 1 && var < (5.2 - var3) ^ -2').join('  /  '));

</script>

That's it, we can now move on to our next task in this adventure which is __How to create a (slow) interpreter - Part 2: Shunting Yard__ (soon) 

See you next time!

[![Comments](https://img.shields.io/badge/dynamic/json.svg?color=orange&style=for-the-badge&label=Comments&query=descendants&url=https%3A%2F%2Fhacker-news.firebaseio.com%2Fv0%2Fitem%2F20498444.json)](https://news.ycombinator.com/item?id=20515595)
