# FromNode with Assistant Kim
![](https://img.shields.io/badge/Django-3.1.1-blue) ![](https://img.shields.io/github/issues/FromNode/FromNode_Project) ![](https://img.shields.io/github/issues-closed/FromNode/FromNode_Project) ![](https://img.shields.io/github/languages/count/FromNode/FromNode_Project) ![](https://img.shields.io/github/contributors/FromNode/FromNode_Project)

# Requirements
#### put some stuff about development environment.
```terminal
 pip install django
 ...
```
--------------
# Major Changes 
### Add similarity Module (21.02.16) from @jaehoonkimm
- This module is basically similar to the two modules updated yesterday.
- To use, do the following.
```python
    # similarity module
    from NodeApp.similarity.similarity import similarity_compare
```
 #### Usage 
   - **Similarity_compare** from similarity module
       - It has four parameter, before_doc, after_doc, user_name, save_list.
       - Put the document object converted through convert function(in the convert module) 
         to each before_doc and after_doc parameter.
       - Put the user name you want to user_name parameter. It'll be appended in a result list.
       - Put the empty python-list to save_list parameter. If this list are not empty, It'll be cleared automatically.
       - Finally you can get a list with the following three lists added and two values: 
         - same_paragraph_index_list,  
         - moved_paragraph_index_list,  
         - new_paragraph_index_list,  
         - user_name,  
         - new_paragraph_ratio(new paragraphs ratio per all paragraphs about before and after document). 
 --------------
### Add summarization, textualization Module (21.02.15) from @jaehoonkimm
- We can use new two modules, convert and summary. This modules are into NodeApp directory as folder type. 
- They are super simple module. If you want to import this module in your code on the NodeApp, put the code like following that,
```terminal
    pip install pororo
    pip install docx
```
```python
    # summary module
    from NodeApp.summarization.summary import summary
    
    # convert module
    from NodeApp.textualization.convert import convert
    from NodeApp.textualization.convert import show_paragraph
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
