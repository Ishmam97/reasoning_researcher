from PyPDF2 import PdfReader

class PDFReader:
    def pdf_extract_content(self,pdf_file):

        self.text=""

        for pdf in pdf_file:
            try:
                pdf_reader = PdfReader(pdf)
            except Exception as e:
                raise Exception(f"Failed to read the PDF file: {pdf}.Error: {e}")
            
            try:
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        self.text += page_text
                    else:
                        raise Exception(f"Failed to extract text from a page in {pdf}.")
            except Exception as e:
                raise Exception(f"Error occurred while extracting text from {pdf}. Error: {e}")
            
        return self.text
