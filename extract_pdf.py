"""Extract page-indexed PDF text; never overwrite an existing output."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if not args.pdf.is_file() or args.pdf.suffix.lower() != '.pdf':
        parser.error('Input must be an existing PDF file')
    if args.output.exists():
        parser.error('Output already exists; choose a new path')
    try:
        from pypdf import PdfReader
    except ImportError:
        parser.exit(2, 'Missing dependency: pypdf. Select a runtime with pypdf installed.\n')
    try:
        reader = PdfReader(str(args.pdf))
        if reader.is_encrypted and not reader.decrypt(''):
            parser.error('Password-protected PDF; supply an unlocked copy')
        pages = []
        for number, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text() or ''
                pages.append({'pdf_page': number, 'text': text,
                              'status': 'text_extracted' if text.strip() else 'needs_visual_or_ocr'})
            except Exception as exc:
                pages.append({'pdf_page': number, 'text': '', 'status': 'failed', 'error': str(exc)})
        result = {'source': str(args.pdf.resolve()),
                  'sha256': hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
                  'page_count': len(pages), 'pages': pages}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
        print(json.dumps({'pages': len(pages), 'needs_review': sum(p['status'] != 'text_extracted' for p in pages)}, ensure_ascii=False))
    except Exception as exc:
        parser.exit(1, f'Extraction failed: {exc}\n')


if __name__ == '__main__':
    main()
