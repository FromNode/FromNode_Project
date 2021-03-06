from docx import Document
import docx


def convert(target_document):
    # FileName Extension
    # fn_extension = target_document.split(".")[-1]
    fn_extension = "docx"  # 함수 내에서 처리하면 오류 발생하여 일단 all true로 처리함
    if fn_extension == "docx":
        return docx.Document(target_document)


def show_paragraph(converted_document, index):
    docu_type_str = str(type(converted_document))
    if "docx.document.Document" in docu_type_str:
        if index == "all":
            for x, paragraph in enumerate(converted_document.paragraphs):
                print(str(x) + " : " + paragraph.text)
            return None
        elif type(index) == int:
            return converted_document.paragraphs[index].text
    else:
        raise Exception("Unsupported file extension. Only use docx or ...")


def get_str(converted_document):
    docu_type_str = str(type(converted_document))
    if "docx.document.Document" in docu_type_str:
        document_string = ""
        for paragraph in converted_document.paragraphs:
            document_string = document_string + paragraph.text.rstrip()
        return document_string
    else:
        raise Exception("Unsupported file extension. Only use docx or ...")
