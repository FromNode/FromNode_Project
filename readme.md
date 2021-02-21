[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![](https://img.shields.io/badge/Django-3.1.1-blue) ![](https://img.shields.io/github/issues/FromNode/FromNode_Project) ![](https://img.shields.io/github/issues-closed/FromNode/FromNode_Project) ![](https://img.shields.io/github/languages/count/FromNode/FromNode_Project) ![](https://img.shields.io/github/contributors/FromNode/FromNode_Project)
![noname](https://user-images.githubusercontent.com/43606451/108619937-adbb7b80-746b-11eb-9508-012266a5b8c1.png)
# FromNode with Assistant Kim

## __Are you a univ student? Then you are our user!__
This is __Fromnode__, and __assistant kim__. It is __super simple__ to use.   
Drag the document to the screen on our web page and write a explanation like github commit.   
This gives you a __quick__, __at-a-glance view of flow__ around the evolution of the file.
# Background
지난 몇 년간 대학내 PBL(Problem-Based Learning 또는 Project-Based Learning) 수업이 크게 증가하고 있습니다. 모 대학의 경우, 2017년부터 2020년까지 4년간 약 1.7배 가량의 PBL 수업 증가 추이를 보였으며, 이는 학기 중 팀 프로젝트를 수행하는 학생들이 증가하고 있음을 의미합니다. (한양대학교 ERICA캠퍼스, 2020.12 기준)
또한, COVID-19 바이러스 사태는 많은 수업을 비대면 형태로 진행되도록 만들었습니다. 지금 이 순간에도, 2021년 1학기의 많은 수업은 비대면 또는 비대면/대면 병행 형태로 진행될 예정에 있습니다. 비대면 수업은 학생들로 하여금 팀프로젝트 수행에 있어서 많은 어려움을 만들어내었습니다. 대부분의 학생들은 온라인 화상회의 플랫폼, 채팅 기반의 SNS, 파일 공유 Cloud 서비스 등을 통해 비대면으로 프로젝트를 진행하였고, 이 과정에서 커뮤니케이션의 어려움, 소통의 부재로 인한 갈등, 일정 관리 및 프리라이더 배제의 어려움 등, 많은 문제에 노출되기도 하였습니다. 이러한 경험은 학생들로 하여금 효율적으로 팀프로젝트를 진행할 해법을 찾아낼 필요성을 느끼게 하였습니다.

PBL을 비롯한 여러 팀프로젝트 기반의 수업은 평가방식 자체가 팀프로젝트 평가 위주로 돌아가는 경우가 많습니다. 특히, COVID-19 사태는 기존의 대면 평가방식(중간고사, 기말고사, 퀴즈 등)을 축소시켰으며, 이에 따라 자연스럽게 팀프로젝트의 평가 비중은 늘어나게 되었습니다. 즉, 기존 평가방식에 비해 훨씬, 팀프로젝트의 중요성이 늘어났으며, 팀프로젝트를 공정하게 평가할 수 있는 정량적/절대적인 기준이 필요해졌습니다.

이하 중략

# Requirements
#### put some stuff about development environment.
```terminal
 pip install django
 pip install docx
 pip install pororo
 ...
 
 or
 pip install -r requirements.txt
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
 
 # License
FromNode with Assistant Kim Project is licensed under the terms of the Apache License 2.0.
