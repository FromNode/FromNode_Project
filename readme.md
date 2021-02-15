# FromNode with Assistant Kim
# Requirements
#### put some stuff about development environment.
```terminal
 pip install django
 ...
```
--------------
# Major Changes 
### Add summarization, textualization Module (21.02.15) from @jaehoonkimm
- We can use new two modules, convert and summary. This modules are into NodeApp directory as folder type. 
- They are super simple module. If you want to import this module in your code on the NodeApp, put the code like following that,
```terminal
    pip install pororo
    pip install docx
```
```python
    # summary module
    from summary import summary
    
    # convert module
    from convert import convert
    from convert import show_paragraph
```
 #### Usage 
   - **Summary Function** from summary module
       - It has two parameter, target_text and language(default for korean).
       - You must put str type argument to target_text parameter. 
       - You can get a summarized text.

   - **Convert Function** from convert module
       - Now this module has two function, convert and show_paragraph. 
       - Put the document to convert function. 
       - If the document has docx extension name, the file will converted 
         to "docx.document.Document" object automatically.

   - **Show_paragraph Function** from convert module
       - You must put two arguments to two parameter, converted_document, index.
       - Put the object converted through convert function to first argument field. 
       - Put the index number you want to get paragraph to second argument field. 
       - If you want to get the all of the paragraphs, use "all".
 --------------
