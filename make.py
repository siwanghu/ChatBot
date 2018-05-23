# -*- coding: utf-8 -*-
import os
from xml.dom.minidom import Document

if os.path.exists("./mybot/ketian.aiml"):
    os.remove("./mybot/ketian.aiml")

doc=Document()
aiml=doc.createElement("aiml")
aiml.setAttribute("version","1.0.1")
aiml.setAttribute("encoding","UTF-8")
doc.appendChild(aiml)

with open("./samples/question","rb") as file_question:
    with open("./samples/answer","rb") as file_answer:
        question=str(file_question.readline(),"utf-8")
        answer=str(file_answer.readline(),"utf-8")
        while question and answer:
            category=doc.createElement("category")
            pattern=doc.createElement("pattern")
            pattern_text=doc.createTextNode(question)
            pattern.appendChild(pattern_text)
            template=doc.createElement("template")
            template_text=doc.createTextNode(answer)
            template.appendChild(template_text)
            category.appendChild(pattern)
            category.appendChild(template)
            aiml.appendChild(category)
            question=str(file_question.readline(),"utf-8")
            answer=str(file_answer.readline(),"utf-8")

with open("./mybot/ketian.aiml","wb") as file:
    file.write(doc.toprettyxml(indent='\t', encoding='utf-8'))

lines=open("./mybot/ketian.aiml","rb").readlines()
open("./mybot/ketian.aiml","wb").writelines(lines[1:])




