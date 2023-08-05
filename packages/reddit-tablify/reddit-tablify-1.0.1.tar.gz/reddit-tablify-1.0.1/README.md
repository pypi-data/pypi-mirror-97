Usage 

createRedditTable(obj, headers=[], justifyString='c', outputfile='', index='index', includeIndex=False)


Basic Usage just pass in a dictionary and you get a table output to console with no ordering of headers,
all columns center justified and no index included
```
import rtablify as rtablify

dictionary = {"apple": {'a': 1, 'b' : 2}, "banana" : {'a': 4, 'b' : 6}}
rtablify.createRedditTable(dictionary)

Output:
a|b
:-:|:-:
1|2
4|6
```
Include a list of headers to enforce a header order
```
rtablify.createRedditTable(dictionary, headers = ['b', 'a']])

Output:
b|a
:-:|:-:
2|1
6|4
```

Include a justify string of either 'r' for right 'c' for center and 'l' to justify columns, 
if you don't provide enough characters it will fill with the last in the string. 

So if you had 7 columns and wanted the first left justified and all the rest centered you could pass in a string of
'lc' or 'lcccccc' both would have the same results.

Bug to fix in future relases is handle if justifyString is too long for now don't do that.

```
rtablify.createRedditTable(dictionary, justifyString = 'll')

Output:
a|b
--:|--:
1|2
4|6
```

If you include an outputfile name it will be created in the directory with a name provided and will not print to the console.


If leave on includeIndex = True (default false) The index will added into the table. If you do not specify an index name it will be called index.
If you want an index it is best to include a header list to let the function know where you want the index to be.

```
rtablify.createRedditTable(dictionary, headers= ['index','a','b'], includeIndex = True)

Output:
index|a|b
:-:|:-:|:-:
apple|1|2
banana|4|6
```