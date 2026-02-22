"""
EML to PDF Converter - Streamlit Version
Unified application for easy deployment
"""

import streamlit as st
from email import policy
from email.parser import BytesParser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from io import BytesIO
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="EML to PDF Converter",
    page_icon="📧",
    layout="centered"
     menu_items={
        'Get Help': 'https://github.com/Gattupalli-Saketh/eml-to-pdf-streamlit',  
        'Report a bug': 'https://github.com/Gattupalli-Saketh/eml-to-pdf-streamlit/issues',
        'About': "Free browser-based tool to convert EML files to PDF. No sign-up, no data stored. Batch support."
    }
)
#Meta tags for SEO and social sharing
st.markdown("""
    <meta name="description" content="Free online EML to PDF converter. Convert .eml email files to clean PDF documents securely in your browser. Batch upload supported – no registration, no server storage, instant download.">
    <meta name="keywords" content="eml to pdf, eml converter, email to pdf converter, convert eml to pdf online, free eml to pdf, eml file to pdf, batch eml converter, streamlit eml tool">
    <meta name="robots" content="index, follow">

    <!-- Open Graph -->
    <meta property="og:title" content="EML to PDF Converter – Free & Secure Online Tool">
    <meta property="og:description" content="Instantly convert .eml email files to PDF. Private, browser-only processing. Multiple files at once. No installation required.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://eml2pdf-gvs.streamlit.app/">
    <meta property="og:image" content="https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png"> <!-- replace with real screenshot if you have one -->

    <!-- Twitter / X Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Free Online EML to PDF Converter">
    <meta name="twitter:description" content="Convert email (.eml) files to PDF – secure, fast, supports batch conversion.">
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)


def convert_eml_to_pdf(eml_file):
    """
    Convert EML file to PDF
    Returns: BytesIO object containing the PDF
    """
    try:
        # Parse the .eml file
        msg = BytesParser(policy=policy.default).parse(eml_file)
        
        # Extract Email details
        subject = msg['subject'] or 'No subject'
        from_ = msg['from'] or 'Unknown sender'
        to_ = msg['to'] or 'Unknown recipient'
        date_ = msg['date'] or 'Unknown date'
        
        # Extract body
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode(errors='ignore') + '\n'
                    except Exception as e:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors='ignore')
            except Exception as e:
                body = 'Unable to decode email body'
        
        # Generate PDF in memory
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        
        # Page setup
        width, height = letter
        left_margin = 100
        right_margin = width - 100
        bottom_margin = 50
        
        # Draw the Email metadata
        y = 750  # Start from top
        
        # Header
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(left_margin, y, "Email Document")
        y -= 30
        
        # Subject
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(left_margin, y, "Subject:")
        pdf.setFont("Helvetica", 12)
        y -= 20
        for line in simpleSplit(str(subject), "Helvetica", 12, right_margin - left_margin):
            pdf.drawString(left_margin, y, line)
            y -= 15
        
        y -= 10
        
        # From
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(left_margin, y, "From:")
        pdf.setFont("Helvetica", 12)
        y -= 20
        pdf.drawString(left_margin, y, str(from_))
        y -= 20
        
        # To
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(left_margin, y, "To:")
        pdf.setFont("Helvetica", 12)
        y -= 20
        pdf.drawString(left_margin, y, str(to_))
        y -= 20
        
        # Date
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(left_margin, y, "Date:")
        pdf.setFont("Helvetica", 12)
        y -= 20
        pdf.drawString(left_margin, y, str(date_))
        y -= 30
        
        # Separator line
        pdf.line(left_margin, y, right_margin, y)
        y -= 20
        
        # Body header
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(left_margin, y, "Message:")
        y -= 20
        
        # Draw Body
        pdf.setFont("Helvetica", 10)
        lines = body.split("\n")
        for line in lines:
            if not line.strip():
                y -= 15
                if y < bottom_margin:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    y = 750
                continue
            
            wrapped_lines = simpleSplit(line, "Helvetica", 10, right_margin - left_margin)
            for wrapped_line in wrapped_lines:
                pdf.drawString(left_margin, y, wrapped_line)
                y -= 15
                
                # Check if we need a new page
                if y < bottom_margin:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    y = 750
        
        # Save PDF
        pdf.save()
        buffer.seek(0)
        
        return buffer, None
        
    except Exception as e:
        return None, str(e)


# Main UI
st.title("📧 EML to PDF Converter")
st.markdown("Convert your email (.eml) files to PDF format easily")

# Info box
st.info("ℹ️ Upload .eml files (max 10MB each). Multiple files supported.")

# File uploader
uploaded_files = st.file_uploader(
    "Choose EML files",
    type=['eml'],
    accept_multiple_files=True,
    help="Select .eml files to convert to PDF"
)

# Process uploaded files
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
    
    # Show file details
    with st.expander("📋 View uploaded files", expanded=True):
        for idx, file in enumerate(uploaded_files, 1):
            file_size_mb = len(file.getvalue()) / (1024 * 1024)
            st.write(f"{idx}. **{file.name}** - {file_size_mb:.2f} MB")
    
    st.markdown("---")
    
    # Convert button
    if st.button(f"🔄 Convert {len(uploaded_files)} File{'s' if len(uploaded_files) > 1 else ''} to PDF"):
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        success_count = 0
        error_count = 0
        converted_files = []
        
        # Process each file
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Converting {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}...")
            progress_bar.progress((idx) / len(uploaded_files))
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Convert to PDF
            pdf_buffer, error = convert_eml_to_pdf(uploaded_file)
            
            if pdf_buffer and not error:
                pdf_filename = uploaded_file.name.replace('.eml', '.pdf')
                converted_files.append({
                    'name': pdf_filename,
                    'data': pdf_buffer.getvalue()
                })
                success_count += 1
            else:
                st.error(f"❌ Failed to convert {uploaded_file.name}: {error}")
                error_count += 1
        
        # Update progress to 100%
        progress_bar.progress(1.0)
        status_text.text("Conversion complete!")
        
        st.markdown("---")
        
        # Display results
        if success_count > 0:
            st.success(f"✅ Successfully converted {success_count} file{'s' if success_count > 1 else ''}!")
            
            st.markdown("### 📥 Download Your PDFs:")
            
            # Create download buttons for each converted file
            for file_info in converted_files:
                st.download_button(
                    label=f"📄 Download {file_info['name']}",
                    data=file_info['data'],
                    file_name=file_info['name'],
                    mime="application/pdf",
                    key=f"download_{file_info['name']}"
                )
        
        if error_count > 0:
            st.warning(f"⚠️ {error_count} file(s) failed to convert. Check errors above.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>💡 <strong>Note:</strong> All conversions happen in memory. No files are stored on the server.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with info
with st.sidebar:
    st.header("📖 About")
    
    st.markdown("""
    ### EML to PDF Converter
    
    This application converts email files (.eml format) 
    to PDF documents.
    
    ### Features:
    - ✅ Multiple file upload
    - ✅ Batch conversion
    - ✅ Secure processing
    - ✅ No file storage
    - ✅ Easy download
    
    ### Supported Format:
    - `.eml` files only
    
    ### Limitations:
    - Max 10MB per file
    - Text content only
    - No attachments in PDF
    
    ### How to Use:
    1. Upload your .eml file(s)
    2. Click "Convert to PDF"
    3. Download the converted PDF(s)
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")
