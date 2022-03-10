# ABOP
Python implementation of algorithms reproducting the pictures from the Algorithmic Beauty of Plants
The original book can be found freely here : [http://algorithmicbotany.org/papers/#abop](http://algorithmicbotany.org/papers/#abop)

The general idea of the book is to generate trees using L-Systems (Lindenmayer-Systems).
L-Systems are formal grammars allowing the parallel and recursive rewriting of collections of symbols.

Very roughly, we call an Alphabet a set of symbols we will use in an expression. The L-System is composed of an Alphabet, and of Rules.
A rule takes an element from an alphabet and returns a successor : the value by which you will replace the original alphabet element by.

For instance, the rule A -> AB will replace all occurence of "A" in a string by "AB".
Hence, if I take the original string "A", successively applying this rule on the string will yield :

```
A
AB
ABB
ABBB
ABBBB
ABBBBB
etc.
```

Each new evolution of the string is called a generation.

L-Systems are associated with tracing systems allowing you to visualize them, by giving certain meaning to certain symbols in the alphabet. For instance `F` will represent a "move forward", `+` and `-` will represent rotations.
This allows you to use L-Systems to plot in a plane or in space structures.

This repository stores plotting routines used to reproduce the figures of the book.
The simplest way to see the images is to call the bash-script at the root of the project `./plot_everything.sh`.

The images generated are the following :

## Chapter 1
### Section 1.3
![Section 1.3](/figs/mosaic_1.3.png)

### Section 1.4
![Section 1.4](/figs/mosaic_1.4.png)

### Section 1.5
![Section 1.5](/figs/img_1.5.png)

### Section 1.6
![Section 1.6](/figs/mosaic_1.6.png)

### Section 1.7
![Section 1.7](/figs/mosaic_1.7.png)

### Section 1.8
![Section 1.8](/figs/mosaic_1.8.png)

### Section 1.10
![Section 1.10](/figs/mosaic_1.10.png)
