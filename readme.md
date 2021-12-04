[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![](https://img.shields.io/badge/Django-3.1.1-blue) ![](https://img.shields.io/github/issues/FromNode/FromNode_Project) ![](https://img.shields.io/github/issues-closed/FromNode/FromNode_Project) ![](https://img.shields.io/github/languages/count/FromNode/FromNode_Project) ![](https://img.shields.io/github/contributors/FromNode/FromNode_Project)
![noname](https://user-images.githubusercontent.com/43606451/108619937-adbb7b80-746b-11eb-9508-012266a5b8c1.png)
# FromNode with Assistant Kim

## __Are you a univ student? Then you are our user!__
This is __Fromnode__, and __assistant kim__. It is __super simple__ to use.   
Drag the document to the screen on our web page and write a explanation like github commit.   
This gives you a __quick__, __at-a-glance view of flow__ around the evolution of the file.
# Background
지난 몇 년간 대학내 **PBL(Problem-Based Learning 또는 Project-Based Learning)** 수업이 크게 증가하고 있습니다. 
모 대학의 경우, 2017년부터 2020년까지 4년간 약 **1.7배** 가량의 PBL 수업 증가 추이를 보였으며, 이는 학기 중 팀 프로젝트를 수행하는 학생들이 증가하고 있음을 의미합니다. (한양대학교 ERICA캠퍼스, 2020.12 기준)

또한, COVID-19 바이러스 사태는 많은 수업을 비대면 형태로 진행되도록 만들었습니다. 지금 이 순간에도, 2021년 1학기의 많은 수업은 비대면 또는 비대면/대면 병행 형태로 진행될 예정에 있습니다. 비대면 수업은 학생들로 하여금 팀프로젝트 수행에 있어서 많은 어려움을 만들어내었습니다. 대부분의 학생들은 온라인 화상회의 플랫폼, 채팅 기반의 SNS, 파일 공유 Cloud 서비스 등을 통해 비대면으로 프로젝트를 진행하였고, 이 과정에서 커뮤니케이션의 어려움, 소통의 부재로 인한 갈등, 일정 관리 및 프리라이더 배제의 어려움 등, 많은 **문제에 노출**되기도 하였습니다. 
이러한 경험은 학생들로 하여금 **효율적으로 팀프로젝트를 진행할 해법을 찾아낼 필요성**을 느끼게 하였습니다.

--------------
### 협업에 대한 Issue
일반적으로 팀프로젝트는 크게 \[조편성 -> 역할분담 -> 주제선정 -> 자료조사 -> PPT/보고서 등 제작 -> 발표 또는 제출]과 같은 순서로 진행됩니다. 팀원들은 이 과정에서 최소 수십, 수백 번에 달하는 상호작용과 파일 공유를 반복합니다. 

전통적인 작업물 공유 방식인 'XXX톡 채팅방에서 파일 공유, 클라우드 기반 플랫폼에서 파일 공유, 메일로 파일 공유' 등은 많은 **제약 사항**을 가지고 있습니다. 채팅과 파일이 혼재하여 원하는 파일을 쉽게 찾을 수 없거나, 구체적으로 어떠한 파일(언제, 어떤 사항이, 어떻게 추가되었는지...)인지에 대한 파악, 업로드 된 시점과 업로드한 팀원 간의 선후 관계 등, 여러 부분에서 불편이 야기되며, 이는 **비효율적인 시간 소모**를 낳게 됩니다.

FromNode는 이를 해결하기 위하여, **Project -> File -> Node**의 삼단 구조를 통해 오로지 프로젝트만을 위한 **공유/협업의 공간**을 제공하며, 업로드하는 File에 대한 코멘트, 시점, 선후관계, 지난 파일과의 유사도, 파일의 요약본 등을 제공하여 **불필요한 시간 소모**를 극단적으로 줄여줍니다.

--------------
### 평가에 대한 Issue
COVID-19 사태는 기존의 대면 평가방식(중간고사, 기말고사, 퀴즈 등)을 축소시켰으며, 이에 따라 자연스럽게 팀프로젝트의 평가 비중은 늘어나게 되었습니다. 즉, 기존 평가방식에 비해 훨씬, 팀프로젝트의 중요성이 늘어났으며, 팀프로젝트를 공정하게 평가할 수 있는 **정량적/절대적인 기준**이 **필요**해졌습니다.

PBL 수업의 팀프로젝트 평가 방식은 '팀간 상호평가', '팀원간 상호평가', '교수자 평가' 등이 있습니다. 이러한 평가 방식은, __공정성이 침해받을 위험성__을 잠재적으로 내포하고 있습니다. 

팀원별 평가에서는 단순히 프로젝트 결과물에 대한 기여도가 높은 팀원이 높은 점수를 받는 것이 아닌, 사전에 합의한 이들의 상호 점수 교환이 이루어질 가능성이 있습니다. 일반적으로 팀원간 평가는 익명성을 보장하므로, 이러한 가능성은 분명히 존재합니다.

교수자 평가의 경우는, 교수자가 볼 수 있는 평가물은 오로지 팀프로젝트의 과정과 결과물이므로, 이에 대한 각 학생들의 기여 정도에 대한 정보는 일체 제공받지 못 합니다. 결국, 공정성 침해의 위험이 큰 팀원간 평가, 정량적인 기여 정도가 배제된 채로 진행되는 교수자의 평가, 이것으로 팀프로젝트의 평가, 최종적으로는 성적에 대한 평가가 내려지게 되는 것입니다.

--------------
### FromNode with Assistant Kim은 다음과 같은 해법을 제시합니다.
본 서비스는 서비스 내 진행된 **팀프로젝트 협업 과정**(파일 공유 및 업로드, 커뮤니케이션 등)을 추적합니다. 이 과정에서 각 팀원이 파일을 업로드하는 시점에서 얼마나 기여를 했는지 측정할 수 있으며, 최종 결과물을 제출하게 되면 다시 한번 전체 팀원의 기여 정도를 평가합니다. 또한, 해당 프로젝트에 대한 대시보드를 통해 교수자가 평가할 수 있는 여러가지 지표를 제시합니다. 

교수자는 이를 통하여, 단순히 결과물에 의존한 평가가 아닌, **객관적이고 정량적인 지표**를 통하여 팀별, 학생별 평가를 진행할 수 있습니다. 궁극적으로, 김조교 AI는 팀프로젝트 협업 활동 데이터를 수집/모니터링하여 협업 **편의의 향상**과 **평가의 객관화**를 이룩하기 위해 단계별 목표를 설정, 고도화 할 예정에 있습니다.


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
 
# Project Members
 ### Sea Jung 
  - 👩‍💼 __Project Leader__
  - 🖥 __Business Logistics__
 ### Hyeseon Lee 
  - 👩‍💻 __Developer__
  - 📊 __Logic·DataBase__
  - 💻 __Front-End·UI/UX Interface__
 ### Taewon Jin 
  - 🧑‍💻 __Developer__
  - 💻 __Dev·Logic·Network__
 ### Jaehoon Kim 
  - 🧑‍💻 __Developer__
  - 📊 __DataScience·Algorithm__
 ### Ina Woo 
  - 👩‍💻 __Designer__
  - 🎨 __Design·UI/UX Interface__
 
 --------------
# License
FromNode with Assistant Kim Project is licensed under the terms of the Apache License 2.0.
