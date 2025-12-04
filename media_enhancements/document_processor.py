"""
Document Processing Module
Handles PDF preview generation, OCR, text extraction, and metadata
"""

import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class DocumentProcessor:
    """
    Document processing toolkit for PDFs and other documents.
    """
    
    def __init__(self, document_path):
        """
        Initialize with document file path.
        """
        self.document_path = document_path
        self.is_pdf = document_path.lower().endswith('.pdf')
    
    def extract_metadata(self):
        """
        Extract document metadata (title, author, subject, keywords, page count).
        
        Returns:
            Dict with metadata
        """
        if not self.is_pdf:
            return {}
        
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(self.document_path)
            metadata = reader.metadata
            
            result = {
                'page_count': len(reader.pages),
                'title': metadata.get('/Title', ''),
                'author': metadata.get('/Author', ''),
                'subject': metadata.get('/Subject', ''),
                'keywords': metadata.get('/Keywords', ''),
                'creator': metadata.get('/Creator', ''),
                'producer': metadata.get('/Producer', ''),
            }
            
            # Clean up metadata
            result = {k: str(v) if v else '' for k, v in result.items()}
            
            return result
            
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}
    
    def extract_text(self, max_pages=None):
        """
        Extract text from PDF.
        
        Args:
            max_pages: Maximum number of pages to extract (None = all)
        
        Returns:
            Extracted text as string
        """
        if not self.is_pdf:
            return ''
        
        try:
            import pdfplumber
            
            text_parts = []
            
            with pdfplumber.open(self.document_path) as pdf:
                pages_to_process = pdf.pages[:max_pages] if max_pages else pdf.pages
                
                for page in pages_to_process:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            
            return '\n\n'.join(text_parts)
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            
            # Fallback to PyPDF2
            try:
                from PyPDF2 import PdfReader
                
                reader = PdfReader(self.document_path)
                text_parts = []
                
                pages_to_process = reader.pages[:max_pages] if max_pages else reader.pages
                
                for page in pages_to_process:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                
                return '\n\n'.join(text_parts)
                
            except Exception as e2:
                print(f"Error with fallback text extraction: {e2}")
                return ''
    
    def perform_ocr(self, language='eng', max_pages=None):
        """
        Perform OCR on PDF (for scanned documents).
        
        Args:
            language: OCR language code (e.g., 'eng', 'fra', 'deu')
            max_pages: Maximum number of pages to OCR
        
        Returns:
            Extracted text from OCR
        """
        if not self.is_pdf:
            return ''
        
        try:
            from pdf2image import convert_from_path
            import pytesseract
            
            # Convert PDF to images
            images = convert_from_path(
                self.document_path,
                first_page=1,
                last_page=max_pages
            )
            
            # Perform OCR on each page
            text_parts = []
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image, lang=language)
                if text.strip():
                    text_parts.append(f"--- Page {i+1} ---\n{text}")
            
            return '\n\n'.join(text_parts)
            
        except Exception as e:
            print(f"Error performing OCR: {e}")
            return ''
    
    def generate_preview_image(self, page_number=1, dpi=150, output_path=None):
        """
        Generate preview image of PDF page.
        
        Args:
            page_number: Page number to preview (1-indexed)
            dpi: Resolution for preview
            output_path: Output file path
        
        Returns:
            Path to generated preview image
        """
        if not self.is_pdf:
            return None
        
        try:
            from pdf2image import convert_from_path
            
            # Convert specific page to image
            images = convert_from_path(
                self.document_path,
                first_page=page_number,
                last_page=page_number,
                dpi=dpi
            )
            
            if not images:
                return None
            
            image = images[0]
            
            # Save image
            if output_path is None:
                output_path = self.document_path.rsplit('.', 1)[0] + '_preview.jpg'
            
            image.save(output_path, 'JPEG', quality=85)
            
            return output_path
            
        except Exception as e:
            print(f"Error generating preview: {e}")
            return None
    
    def generate_preview_django(self, page_number=1, dpi=150):
        """
        Generate preview and return as Django ContentFile.
        
        Returns:
            ContentFile object
        """
        import tempfile
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Generate preview
            self.generate_preview_image(page_number, dpi, tmp_path)
            
            # Read and return as ContentFile
            with open(tmp_path, 'rb') as f:
                content = f.read()
            
            filename = os.path.basename(self.document_path).rsplit('.', 1)[0] + '_preview.jpg'
            return ContentFile(content, name=filename)
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def generate_thumbnails(self, max_pages=5, dpi=100):
        """
        Generate thumbnail images for multiple pages.
        
        Args:
            max_pages: Maximum number of pages to generate thumbnails for
            dpi: Resolution for thumbnails
        
        Returns:
            List of thumbnail paths
        """
        if not self.is_pdf:
            return []
        
        try:
            from pdf2image import convert_from_path
            
            # Convert pages to images
            images = convert_from_path(
                self.document_path,
                first_page=1,
                last_page=max_pages,
                dpi=dpi
            )
            
            thumbnails = []
            base_path = self.document_path.rsplit('.', 1)[0]
            
            for i, image in enumerate(images):
                thumb_path = f"{base_path}_thumb_{i+1}.jpg"
                image.save(thumb_path, 'JPEG', quality=75)
                thumbnails.append(thumb_path)
            
            return thumbnails
            
        except Exception as e:
            print(f"Error generating thumbnails: {e}")
            return []
    
    def count_words(self, text=None):
        """
        Count words in document.
        
        Args:
            text: Text to count (if None, extracts from document)
        
        Returns:
            Word count
        """
        if text is None:
            text = self.extract_text()
        
        if not text:
            return 0
        
        # Simple word count
        words = text.split()
        return len(words)
    
    def search_text(self, query, case_sensitive=False):
        """
        Search for text in document.
        
        Args:
            query: Search query
            case_sensitive: Whether search is case-sensitive
        
        Returns:
            List of (page_number, context) tuples
        """
        if not self.is_pdf:
            return []
        
        try:
            import pdfplumber
            
            results = []
            
            with pdfplumber.open(self.document_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    # Search in text
                    search_text = text if case_sensitive else text.lower()
                    search_query = query if case_sensitive else query.lower()
                    
                    if search_query in search_text:
                        # Find context around match
                        index = search_text.find(search_query)
                        start = max(0, index - 50)
                        end = min(len(text), index + len(query) + 50)
                        context = text[start:end]
                        
                        results.append((i + 1, context))
            
            return results
            
        except Exception as e:
            print(f"Error searching text: {e}")
            return []
    
    def split_pdf(self, page_ranges):
        """
        Split PDF into multiple files.
        
        Args:
            page_ranges: List of (start, end) tuples for page ranges
        
        Returns:
            List of output file paths
        """
        if not self.is_pdf:
            return []
        
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            reader = PdfReader(self.document_path)
            output_files = []
            base_path = self.document_path.rsplit('.', 1)[0]
            
            for i, (start, end) in enumerate(page_ranges):
                writer = PdfWriter()
                
                # Add pages (0-indexed)
                for page_num in range(start - 1, end):
                    if page_num < len(reader.pages):
                        writer.add_page(reader.pages[page_num])
                
                # Write output
                output_path = f"{base_path}_part{i+1}.pdf"
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                
                output_files.append(output_path)
            
            return output_files
            
        except Exception as e:
            print(f"Error splitting PDF: {e}")
            return []
    
    def merge_pdfs(self, pdf_paths, output_path=None):
        """
        Merge multiple PDFs into one.
        
        Args:
            pdf_paths: List of PDF file paths to merge
            output_path: Output file path
        
        Returns:
            Path to merged PDF
        """
        try:
            from PyPDF2 import PdfMerger
            
            merger = PdfMerger()
            
            for pdf_path in pdf_paths:
                merger.append(pdf_path)
            
            if output_path is None:
                output_path = self.document_path.rsplit('.', 1)[0] + '_merged.pdf'
            
            merger.write(output_path)
            merger.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error merging PDFs: {e}")
            return None
    
    def add_watermark(self, watermark_text, output_path=None):
        """
        Add watermark to PDF.
        
        Args:
            watermark_text: Text to use as watermark
            output_path: Output file path
        
        Returns:
            Path to watermarked PDF
        """
        # This would require reportlab or similar
        # Simplified implementation
        print("Watermarking requires additional setup")
        return None
    
    def get_document_info(self):
        """
        Get comprehensive document information.
        
        Returns:
            Dict with all document properties
        """
        info = self.extract_metadata()
        
        if self.is_pdf:
            # Add text extraction info
            text = self.extract_text(max_pages=1)
            info['has_text'] = bool(text.strip())
            info['word_count'] = self.count_words(text) if text else 0
        
        return info


# Convenience functions

def process_uploaded_document(document_instance):
    """
    Process newly uploaded document: extract metadata, text, and generate preview.
    
    Args:
        document_instance: CustomDocument model instance
    """
    if document_instance.file and document_instance.is_pdf():
        processor = DocumentProcessor(document_instance.file.path)
        
        # Extract metadata
        metadata = processor.extract_metadata()
        if metadata:
            document_instance.page_count = metadata.get('page_count')
            document_instance.author = metadata.get('author', '')
            document_instance.subject = metadata.get('subject', '')
            document_instance.keywords = metadata.get('keywords', '')
        
        # Extract text
        text = processor.extract_text(max_pages=10)  # First 10 pages
        if text:
            document_instance.extracted_text = text[:10000]  # Limit to 10k chars
            document_instance.word_count = processor.count_words(text)
            document_instance.is_searchable = True
        else:
            # Try OCR if no text found
            ocr_text = processor.perform_ocr(
                language=document_instance.ocr_language,
                max_pages=5
            )
            if ocr_text:
                document_instance.extracted_text = ocr_text[:10000]
                document_instance.word_count = processor.count_words(ocr_text)
                document_instance.ocr_performed = True
                document_instance.is_searchable = True
        
        # Generate preview
        if not document_instance.preview_image:
            try:
                preview_file = processor.generate_preview_django()
                if preview_file:
                    document_instance.preview_image.save(preview_file.name, preview_file, save=False)
                    document_instance.preview_generated = True
            except Exception as e:
                print(f"Error generating preview: {e}")
        
        document_instance.save()


def generate_preview_for_document(document_instance):
    """
    Generate preview for existing document instance.
    
    Args:
        document_instance: CustomDocument model instance
    """
    if document_instance.file and document_instance.is_pdf():
        processor = DocumentProcessor(document_instance.file.path)
        
        # Generate preview
        preview_file = processor.generate_preview_django()
        if preview_file:
            document_instance.preview_image.save(preview_file.name, preview_file, save=False)
            document_instance.preview_generated = True
            document_instance.save()


def perform_ocr_on_document(document_instance, language='eng'):
    """
    Perform OCR on document.
    
    Args:
        document_instance: CustomDocument model instance
        language: OCR language code
    """
    if document_instance.file and document_instance.is_pdf():
        processor = DocumentProcessor(document_instance.file.path)
        
        # Perform OCR
        ocr_text = processor.perform_ocr(language=language)
        if ocr_text:
            document_instance.extracted_text = ocr_text[:10000]
            document_instance.word_count = processor.count_words(ocr_text)
            document_instance.ocr_performed = True
            document_instance.ocr_language = language
            document_instance.is_searchable = True
            document_instance.save()
