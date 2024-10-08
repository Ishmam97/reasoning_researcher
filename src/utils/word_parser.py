import docx2txt 

class DocumentReader:
    def doc_extract_content(self,doc_file):
        
        self.text = ""

        for doc in doc_file:
            try:
                self.text += docx2txt.process(doc)
            except Exception as e:
                raise Exception(f"Error occured while extracting text from {doc}. Error: {e} ")
     
        return self.text
