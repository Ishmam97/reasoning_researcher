import docx2txt 

class DocumentReader:

    @staticmethod
    def doc_extract_content(doc_file):
        
        text = ""

        for doc in doc_file:
            try:
                text += docx2txt.process(doc)
            except Exception as e:
                raise Exception(f"Error occured while extracting text from {doc}. Error: {e} ")
     
        return text
