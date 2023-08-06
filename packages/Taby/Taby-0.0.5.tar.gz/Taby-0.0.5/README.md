# Taby

A pip package that highlights tabs

### Features
- Easy to use
- Fast
- Efficient

### Author
This pip package was created and maintained by Landon Hutchins and Travis Mackey

### Installation
The following are the steps on how to use the Taby package.

```sh
pip install taby
```

```
#Create a highlighter object by specifying the color of the highlight and thennthe 'TAB' keyword to replace all tab instances in the file.

ho = highlighter('color', 'TAB')

#Specify a file to be read from, a file to output, and the highlighter object

reader(infile, outfile, ho)

#Once the output file has been written to, specify the same outfile and pass in the highlighter object so that the changes can be printed to the console. 

console(outfile, ho)

```
### Contributions
This project is currently closed to contributions

### License
MIT


