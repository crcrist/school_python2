import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd

def generate_pdf_report(df, image_paths, text_report_path, output_pdf_path='results/spotify_analysis_report.pdf'):
    """
    Generate a PDF report with analysis findings, visualizations, and summary info
    
    Parameters:
    -----------
    df : pandas DataFrame
        The cleaned Spotify songs dataset
    image_paths : list
        Paths to generated visualization images
    text_report_path : str
        Path to the text report with analysis findings
    output_pdf_path : str
        Path where the PDF report should be saved
    """
    # Create PDF document
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for PDF elements
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=12,
        leading=28
    )
    
    heading_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=10,
        spaceBefore=20
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6,
        leading=14
    )
    
    # Title
    elements.append(Paragraph("Most Streamed Spotify Songs 2024", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Dataset Overview
    elements.append(Paragraph("Dataset Overview", heading_style))
    
    # Create summary statistics table
    total_songs = len(df)
    total_artists = df['Artist'].nunique()
    total_streams = df['Spotify Streams'].sum() if 'Spotify Streams' in df.columns else "N/A"
    top_artist = df.groupby('Artist')['Spotify Streams'].sum().idxmax() if 'Spotify Streams' in df.columns else "N/A"
    latest_year = df['Release Year'].max() if 'Release Year' in df.columns else "N/A"
    
    overview_data = [
        ["Metric", "Value"],
        ["Total Songs", f"{total_songs:,}"],
        ["Unique Artists", f"{total_artists:,}"],
        ["Total Spotify Streams", f"{total_streams:,}"],
        ["Top Artist", top_artist],
        ["Most Recent Year", str(latest_year)]
    ]
    
    overview_table = Table(overview_data, colWidths=[2.5*inch, 3*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.teal),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 1), (1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (1, -1), 10),
        ('GRID', (0, 0), (1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(overview_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Read and add key findings from the text report
    if os.path.exists(text_report_path):
        with open(text_report_path, 'r') as f:
            report_text = f.read()
        
        # Parse the report sections
        sections = report_text.split('##')
        
        # Add Key Findings section
        for section in sections:
            if section.strip().startswith('Key Findings'):
                elements.append(Paragraph("Key Findings", heading_style))
                
                # Process findings
                findings = section.replace('Key Findings', '').strip().split('\n\n')
                for finding in findings:
                    if finding:
                        # Strip numbering
                        if finding[0].isdigit() and finding[1] == '.':
                            finding = finding[2:].strip()
                        elements.append(Paragraph(finding, normal_style))
                        elements.append(Spacer(1, 0.1*inch))
    
    # Add visualizations
    elements.append(Paragraph("Key Visualizations", heading_style))
    
    # Filter to include only the most important visualizations
    important_viz = [
        'results/correlation_matrix.png',
        'results/spotify_vs_shazam.png',
        'results/top_artists_by_spotify_streams.png',
        'results/explicit_vs_nonexplicit.png',
        'results/yearly_streams.png',
        'results/distribution_spotify_streams.png',
        'results/monthly_seasonal_pattern.png'
    ]
    
    actual_viz = [img for img in important_viz if img in image_paths]
    
    # Add visualization descriptions
    viz_descriptions = {
        'results/correlation_matrix.png': "Correlation matrix showing relationships between key metrics",
        'results/spotify_vs_shazam.png': "Scatter plot shows a strong relationship between Spotify Streams and Shazam Counts",
        'results/top_artists_by_spotify_streams.png': "Top artists by total Spotify streams",
        'results/explicit_vs_nonexplicit.png': "Percentage of songs classified as explicit in the dataset",
        'results/yearly_streams.png': "Distribution of songs released per year",
        'results/distribution_spotify_streams.png': "Distribution of Spotify streams across songs (log scale)",
        'results/monthly_seasonal_pattern.png': "Monthly release patterns showing seasonality in music releases"
    }
    
    # Add each visualization with its description
    for img_path in actual_viz:
        if os.path.exists(img_path):
            # Add description
            if img_path in viz_descriptions:
                elements.append(Paragraph(viz_descriptions[img_path], normal_style))
            
            # Add image - scale to fit page width
            img = Image(img_path, width=6*inch, height=4*inch)
            elements.append(img)
            elements.append(Spacer(1, 0.2*inch))
    
    # Add conclusion section
    if os.path.exists(text_report_path):
        for section in sections:
            if section.strip().startswith('Conclusion'):
                elements.append(Paragraph("Conclusion", heading_style))
                conclusion_text = section.replace('Conclusion', '').strip()
                elements.append(Paragraph(conclusion_text, normal_style))
    
    # Build the PDF
    doc.build(elements)
    
    print(f"PDF report successfully generated at {output_pdf_path}")

if __name__ == "__main__":
    # This code will run if this script is executed directly
    try:
        # Import cleaned data
        df = pd.read_csv('results/cleaned_spotify_songs.csv')
        
        # Get list of all PNG images in results directory
        image_paths = [os.path.join('results', f) for f in os.listdir('results') if f.endswith('.png')]
        
        # Path to text report
        text_report_path = 'results/analysis_report.txt'
        
        # Generate the PDF
        generate_pdf_report(df, image_paths, text_report_path)
        
    except Exception as e:
        print(f"Error generating PDF report: {e}")
        import traceback
        traceback.print_exc()
