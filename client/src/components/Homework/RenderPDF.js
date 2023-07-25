import React, { useEffect, useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';


const RenderPDF = (props) => {
  const [file, setFile] = useState(null);
  const [numPages, setNumPages] = useState(null);

  useEffect(() => {
    pdfjs.GlobalWorkerOptions.workerSrc=`https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
  });

  useEffect(() => {
    if (props.file) {
      setFile(props.file);
    }
  }, [props]);

  function onDocumentLoadSuccess(document) {
    const { numPages } = document;
    setNumPages(numPages);
  }

  if (file) {
    return (
      <Document file={file} onLoadSuccess={onDocumentLoadSuccess} className="w-100">
        {Array.from(new Array(numPages), (el, index) => (
          <Page
            style={{ width: '100%', height: 'auto'}}
            key={`page_${index + 1}`}
            pageNumber={index + 1}
            wrap
          />
        ))}
      </Document>
    );
  } else {
    return null;
  }
}

export default RenderPDF;

