export interface PdfPage {
  page_number: number;
  text_content: string;
  word_count: number;
}

export interface PdfExtractResponse {
  filename: string;
  total_pages: number;
  pages: PdfPage[];
}

export interface RegionExtractResponse {
  page_number: number;
  type: 'table' | 'text';
  text?: string;
  headers?: string[];
  rows?: string[][];
}
