# No-Limit_PDF

Minimalist black-and-white Streamlit app by **RelaxLife-Apps** for merging multiple PDFs contained in a `.rar` file.

## Features

- Upload `.rar` files directly from the browser.
- Extract PDFs recursively, including subfolders.
- Merge PDFs in natural filename order.
- Download a single merged PDF.
- Automatic language detection: English, Spanish, Portuguese.
- Manual language switch with `?lang=en`, `?lang=es`, `?lang=pt`.

## Required structure

```text
no_limit_pdf_app/
├── app.py
├── requirements.txt
├── packages.txt
├── README.md
├── README.txt
├── .streamlit/
│   └── config.toml
└── assets/
    ├── no_limit_pdf.png
    └── relaxlife_apps.png
```

## Deploy on Streamlit Cloud

1. Upload the full folder to GitHub.
2. Go to Streamlit Cloud.
3. Create a new app from your repository.
4. Set main file path to `app.py`.
5. Deploy.

## Notes

GitHub Pages cannot run Python backends. Use Streamlit Cloud or another Python backend service.
