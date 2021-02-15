from docx import Document
import docx


def convert(target_document):
    # FileName Extension
    fn_extension = target_document.split(".")[-1]
    if fn_extension == "docx":
        return docx.Document(target_document)


def show_paragraph(converted_document, index):
    docu_type_str = str(type(converted_document))
    if "docx.document.Document" in docu_type_str:
        print("h")
    else:
        raise Exception("Unsupported file extension. Only use docx or ...")
