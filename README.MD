
# 📧 EML to PDF Converter (Streamlit App)

A simple, secure, and user-friendly web application that converts **`.eml` email files** into beautifully formatted **PDF documents**.

Built using **Streamlit** and **ReportLab**, this app allows users to upload one or multiple email files and instantly download them as PDFs — all processed securely in memory.

---

## 🚀 Features

* ✅ Convert `.eml` files to `.pdf`
* ✅ Supports multiple file uploads (batch conversion)
* ✅ Clean and structured PDF layout
* ✅ Displays email metadata (Subject, From, To, Date)
* ✅ Proper text wrapping for long emails
* ✅ Secure – no files are stored on the server
* ✅ Simple, modern Streamlit UI
* ✅ Progress bar & conversion status tracking

---

## 🖥️ Demo Overview

The app allows users to:

1. Upload one or more `.eml` files
2. View uploaded file details
3. Click the **Convert** button
4. Download the generated PDF files instantly

All conversions are handled entirely in memory.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** – Web Interface
* **ReportLab** – PDF generation
* **email (Python Standard Library)** – EML parsing
* **BytesIO** – In-memory file handling

---

## 📂 Project Structure

```
📦 eml-to-pdf-streamlit
 ┣ 📄 streamlit_app.py
 ┗ 📄 README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/eml-to-pdf-converter.git
cd eml-to-pdf-converter
```


### 2️⃣ Install Dependencies

```bash
pip install streamlit reportlab
```


## 📄 What Gets Included in the PDF?

Each generated PDF contains:

* 📌 Email Header
* 📝 Subject
* 👤 From
* 📩 To
* 📅 Date
* ✉️ Message Body (formatted with automatic line wrapping)
* Multi-page support for long emails

---

## 🔒 Security & Privacy

* All files are processed **in memory**
* No uploads are saved on disk
* No external servers store your files
* Secure and lightweight processing

---

## ⚠️ Limitations

* Supports only `.eml` files
* Maximum file size: **10MB**
* Only **text content** is included
* Attachments are not embedded in the generated PDF


## ❤️ Made With

Built with ❤️ using [Streamlit](https://streamlit.io/) and ReportLab.




