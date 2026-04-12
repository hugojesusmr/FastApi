import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import api from '../utils/api';
import type { RegionExtractResponse } from '../types/pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import './PdfUpload.css';

pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface Selection {
  x0: number;
  y0: number;
  x1: number;
  y1: number;
  pageNumber: number;
}

interface PageDimensions {
  width: number;
  height: number;
}

const INITIAL_RENDER_PAGES = 5;
const PAGE_LOAD_MARGIN = 3;

export const PdfUpload: React.FC = () => {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [totalPages, setTotalPages] = useState(0);
  const [pageDimensions, setPageDimensions] = useState<Record<number, PageDimensions>>({});
  const [selection, setSelection] = useState<Selection | null>(null);
  const [isSelecting, setIsSelecting] = useState(false);
  const [startPoint, setStartPoint] = useState<{ x: number; y: number; page: number } | null>(null);
  const [result, setResult] = useState<RegionExtractResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadedPages, setLoadedPages] = useState<number[]>([]);

  const containerRef = useRef<HTMLDivElement>(null);
  const pageRefs = useRef<Map<number, HTMLDivElement>>(new Map());
  const canvasRefs = useRef<Map<number, HTMLDivElement>>(new Map());
  const lastScrollTop = useRef(0);

  const getPageElement = useCallback((pageNumber: number): HTMLDivElement | null => {
    return pageRefs.current.get(pageNumber) || null;
  }, []);

  const getCanvasElement = useCallback((pageNumber: number): HTMLDivElement | null => {
    return canvasRefs.current.get(pageNumber) || null;
  }, []);

  useEffect(() => {
    if (!pdfUrl || totalPages === 0) {
      setLoadedPages([]);
      return;
    }

    const initialPages = Array.from({ length: Math.min(INITIAL_RENDER_PAGES, totalPages) }, (_, i) => i + 1);
    setLoadedPages(initialPages);
  }, [pdfUrl, totalPages]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container || totalPages === 0) return;

    const handleScroll = () => {
      const scrollTop = container.scrollTop;
      if (Math.abs(scrollTop - lastScrollTop.current) < 50) return;
      lastScrollTop.current = scrollTop;

      const containerHeight = container.clientHeight;
      const containerRect = container.getBoundingClientRect();

      const lastLoaded = loadedPages.length > 0 ? Math.max(...loadedPages) : 0;

      const newPages: number[] = [];
      for (let i = lastLoaded + 1; i <= Math.min(lastLoaded + PAGE_LOAD_MARGIN, totalPages); i++) {
        const pageEl = pageRefs.current.get(i);
        if (pageEl) {
          const rect = pageEl.getBoundingClientRect();
          if (rect.top - containerRect.top < containerHeight + 200) {
            newPages.push(i);
          }
        }
      }

      if (newPages.length > 0) {
        setLoadedPages((prev) => [...new Set([...prev, ...newPages])].sort((a, b) => a - b));
      }
    };

    container.addEventListener('scroll', handleScroll, { passive: true });
    return () => container.removeEventListener('scroll', handleScroll);
  }, [totalPages, loadedPages]);

  const setPageRef = useCallback((pageNumber: number) => (el: HTMLDivElement | null) => {
    if (el) pageRefs.current.set(pageNumber, el);
  }, []);

  const setCanvasRef = useCallback((pageNumber: number) => (el: HTMLDivElement | null) => {
    if (el) canvasRefs.current.set(pageNumber, el);
  }, []);

  const handlePageLoadSuccess = useCallback((pageNumber: number, page: { width: number; height: number }) => {
    setPageDimensions((prev) => ({ ...prev, [pageNumber]: { width: page.width, height: page.height } }));
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (pdfUrl) URL.revokeObjectURL(pdfUrl);
    setPdfFile(file);
    setPdfUrl(URL.createObjectURL(file));
    setSelection(null);
    setResult(null);
    setError(null);
    setTotalPages(0);
    setPageDimensions({});
    setLoadedPages([]);
    pageRefs.current.clear();
    canvasRefs.current.clear();
  };

  const getRelativeCoords = (e: React.MouseEvent, pageEl: HTMLElement) => {
    const rect = pageEl.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    };
  };

  const handleMouseDown = (e: React.MouseEvent, pageNumber: number) => {
    if (e.button !== 0) return;
    const pageEl = getCanvasElement(pageNumber);
    if (!pageEl) return;
    const { x, y } = getRelativeCoords(e, pageEl);
    setStartPoint({ x, y, page: pageNumber });
    setIsSelecting(true);
    setSelection({ x0: x, y0: y, x1: x, y1: y, pageNumber });
    setResult(null);
  };

  const handleMouseMove = useCallback((e: React.MouseEvent, pageNumber: number) => {
    if (!isSelecting || !startPoint || startPoint.page !== pageNumber) return;
    const pageEl = getCanvasElement(pageNumber);
    if (!pageEl) return;
    const { x, y } = getRelativeCoords(e, pageEl);
    setSelection({ x0: startPoint.x, y0: startPoint.y, x1: x, y1: y, pageNumber });
  }, [isSelecting, startPoint, getCanvasElement]);

  const handleMouseUp = () => {
    setIsSelecting(false);
  };

  const handleExtract = async () => {
    if (!pdfFile || !selection) return;
    if (Math.abs(selection.x1 - selection.x0) < 5 || Math.abs(selection.y1 - selection.y0) < 5) {
      setError('Selecciona un área más grande');
      return;
    }

    setLoading(true);
    setError(null);

    const pageEl = getCanvasElement(selection.pageNumber);
    if (!pageEl) return;
    const rect = pageEl.getBoundingClientRect();

    const region = {
      page_number: selection.pageNumber,
      x0: Math.min(selection.x0, selection.x1),
      y0: Math.min(selection.y0, selection.y1),
      x1: Math.max(selection.x0, selection.x1),
      y1: Math.max(selection.y0, selection.y1),
      pdf_width: rect.width,
      pdf_height: rect.height,
    };

    const formData = new FormData();
    formData.append('file', pdfFile);
    formData.append('region', JSON.stringify(region));

    try {
      const response = await api.post<RegionExtractResponse>('/api/pdf/extract-region', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al extraer la región');
    } finally {
      setLoading(false);
    }
  };

  const getSelectionStyle = (pageNumber: number) => {
    if (!selection || selection.pageNumber !== pageNumber) return {};
    return {
      left: Math.min(selection.x0, selection.x1),
      top: Math.min(selection.y0, selection.y1),
      width: Math.abs(selection.x1 - selection.x0),
      height: Math.abs(selection.y1 - selection.y0),
    };
  };

  return (
    <div className="pdf-upload-container">

      {/* Barra superior */}
      <div className="pdf-toolbar">
        <div className="toolbar-left">
          <input type="file" accept=".pdf" onChange={handleFileChange} id="pdf-input" />
          <label htmlFor="pdf-input" className="btn-select">
            Seleccionar PDF
          </label>
          {pdfFile && <span className="filename">{pdfFile.name}</span>}
        </div>
        {selection && (
          <button onClick={handleExtract} disabled={loading} className="btn-extract">
            {loading ? 'Extrayendo...' : 'Extraer selección'}
          </button>
        )}
      </div>

      {error && <p className="error-msg">{error}</p>}

      <div className="pdf-workspace">

        {/* Visor PDF */}
        {pdfUrl && (
          <div className="pdf-viewer" ref={containerRef}>
            <p className="hint">Dibuja un rectángulo sobre el área que quieres extraer</p>
            <Document
              file={pdfUrl}
              onLoadSuccess={({ numPages }) => setTotalPages(numPages)}
            >
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((pageNumber) => (
                <div
                  key={pageNumber}
                  className="pdf-page-wrapper"
                  data-page={pageNumber}
                  ref={setPageRef(pageNumber)}
                  onMouseDown={(e) => handleMouseDown(e, pageNumber)}
                  onMouseMove={(e) => handleMouseMove(e, pageNumber)}
                  onMouseUp={handleMouseUp}
                >
                  <span className="page-label">Página {pageNumber}</span>
                  <div className="page-canvas-wrapper" ref={setCanvasRef(pageNumber)}>
                    {loadedPages.includes(pageNumber) ? (
                      <Page
                        pageNumber={pageNumber}
                        width={700}
                        onLoadSuccess={(page) => handlePageLoadSuccess(pageNumber, page)}
                      />
                    ) : (
                      <div style={{ width: 700, height: pageDimensions[pageNumber]?.height || 900 }} />
                    )}
                    {selection?.pageNumber === pageNumber && (
                      <div className="selection-box" style={getSelectionStyle(pageNumber)} />
                    )}
                  </div>
                </div>
              ))}
            </Document>
          </div>
        )}

        {/* Panel de resultados */}
        {result && (
          <div className="result-panel">
            <h3>Resultado — Página {result.page_number}</h3>

            {result.type === 'table' && result.headers && (
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      {result.headers.map((h, i) => <th key={i}>{h}</th>)}
                    </tr>
                  </thead>
                  <tbody>
                    {result.rows?.map((row, i) => (
                      <tr key={i}>
                        {row.map((cell, j) => <td key={j}>{cell}</td>)}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {result.type === 'text' && (
              <pre className="text-result">{result.text}</pre>
            )}
          </div>
        )}

      </div>
    </div>
  );
};