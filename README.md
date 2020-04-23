
#Alpha-Build-v0.1

Invoice generation software made for Alpha Tutorials

#How to use

First make a TEXT file in this format

{name},{address},{city},{pin},{state},{reg. no}  
{description of item 1},{hsn},{quantity},{rate}  
{description of item 2},{hsn},{quantity},{rate}  
{description of item 3},{hsn},{quantity},{rate}  
{description of item 4},{hsn},{quantity},{rate}  
{description of item 5},{hsn},{quantity},{rate}  
{description of item 6},{hsn},{quantity},{rate}  

The template contains only 6 rows for now
If there are less than 6 items, enter only the items and leave others empty
Save the text file and copy the path

Then on your terminal, enter the command:

```bash
create-invoice '{path to text file}'
```
