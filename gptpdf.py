


class Gptpdf:
    pass

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_pdf(conversation, output_file):
    # Create a PDF document
    pdf = canvas.Canvas(output_file, pagesize=letter)
    
    # Set font and size
    pdf.setFont("Helvetica", 12)
    
    # Iterate through the conversation and write each message to the PDF
    for sender, message in conversation:
        pdf.drawString(50, pdf._pagesize[1] - pdf._pagesize[1]/8, f"{sender}: {message}")
        pdf.showPage()  # Start a new page for each message
    
    # Save the PDF
    pdf.save()

# Example conversation
example_conversation = [("User", "Hello, ChatGPT!"), ("ChatGPT", "Hi there! How can I help you today?")]

# Export the conversation to a PDF file
export_to_pdf(example_conversation, "conversation_export.pdf")
