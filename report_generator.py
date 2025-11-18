from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import List, Dict
import os

def create_pdf_report(costed_items: List[Dict], output_path: str) -> str:
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch,
        title="Road Safety Cost Estimation Report",
        author="Estimate",
        subject="Road Safety Intervention Cost Analysis"
    )
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5282'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 14
    title = Paragraph("ROAD SAFETY NATIONAL HACKATHON", title_style)
    subtitle = Paragraph("COST ESTIMATION REPORT(MATERIALS ONLY)", title_style)
    elements.append(title)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.3*inch))
    report_date = datetime.now().strftime("%B %d, %Y")
    metadata = [
        ['Report Generated:', report_date],
        ['Project:', 'National Road Safety Hackathon 2025'],
        ['Prepared by:', 'Estimator Tool - AI System'],
        ['Total Interventions:', str(len(costed_items))]
    ]
    meta_table = Table(metadata, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c5282')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 0.5*inch))
    heading = Paragraph("ITEMIZED COST BREAKDOWN", heading_style)
    elements.append(heading)
    elements.append(Spacer(1, 0.2*inch))
    table_data = [
        ['S.No', 'Material/Intervention', 'Quantity', 'Unit', 'Rate (INR)', 'Cost (INR)']
    ]
    grand_total = 0.0
    for idx, item in enumerate(costed_items, 1):
        material = item['material_name']
        quantity = f"{item['quantity']:.2f}"
        unit = item['unit']
        rate = f"{item['rate']:.2f}"
        cost = f"{item['cost']:.2f}"
        grand_total += item['cost']
        if len(material) > 45:
            material_para = Paragraph(material, normal_style)
        else:
            material_para = material
        table_data.append([
            str(idx),
            material_para,
            quantity,
            unit,
            rate,
            cost
        ])
    col_widths = [0.6*inch, 2.8*inch, 0.9*inch, 0.7*inch, 1*inch, 1*inch]
    item_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2c5282')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])
    item_table.setStyle(table_style)
    elements.append(item_table)
    elements.append(Spacer(1, 0.3*inch))
    total_data = [
        ['', '', '', '', 'GRAND TOTAL:', f"{grand_total:.2f}"]
    ]
    total_table = Table(total_data, colWidths=col_widths)
    total_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TEXTCOLOR', (4, 0), (-1, -1), colors.HexColor('#1a365d')),
        ('ALIGN', (4, 0), (-1, -1), 'RIGHT'),
        ('LINEABOVE', (4, 0), (-1, -1), 2, colors.HexColor('#2c5282')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 0.5*inch))
    notes_style = ParagraphStyle(
        'Notes',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        leading=12
    )
    notes_text = """
    <b>Notes:</b><br/>
    1. All prices shown are MATERIAL COSTS ONLY (based on CPWD DSR 2024 and GeM portal rates).<br/>
    2. Labor, installation, and contractor charges are NOT included in the above rates.<br/>
    3. GST and other statutory taxes are not included in the above rates.<br/>
    4. Actual quantities should be verified through detailed site survey.<br/>
    5. Prices are subject to market fluctuations and regional variations.<br/>
    6. Add appropriate labor and installation charges as per local standards.
    """
    notes = Paragraph(notes_text, notes_style)
    elements.append(notes)
    doc.build(elements)
    return output_path
