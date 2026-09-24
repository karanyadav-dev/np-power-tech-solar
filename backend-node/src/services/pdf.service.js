'use strict';

const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');
const storage = require('../config/storage');

/**
 * PDF generation service.
 * Generates quotations, invoices, and reports.
 */

const COLORS = {
  primary: '#F59E0B',
  dark: '#1F2937',
  gray: '#6B7280',
  light: '#FEF3C7',
  green: '#10B981',
  red: '#EF4444',
};

const COMPANY = {
  name: 'NP POWER TECH SOLAR',
  tagline: 'Power Your Future with Solar',
  phone: process.env.PUBLIC_COMPANY_PHONE || '+91-96109-91048',
  email: process.env.PUBLIC_COMPANY_EMAIL || 'raokarankumar93@gmail.com',
  address: process.env.PUBLIC_COMPANY_ADDRESS || 'Govindgarh',
};

function header(doc) {
  doc.rect(0, 0, doc.page.width, 100).fill(COLORS.primary);
  doc.fillColor('#FFFFFF').fontSize(24).font('Helvetica-Bold').text(COMPANY.name, 40, 25);
  doc.fontSize(10).font('Helvetica').text(COMPANY.tagline, 40, 55);
  doc.fontSize(9).text(COMPANY.phone, 400, 30, { align: 'right', width: 160 })
     .text(COMPANY.email, 400, 45, { align: 'right', width: 160 })
     .text(COMPANY.address, 400, 60, { align: 'right', width: 160 });
  doc.moveDown(4);
}

function footer(doc) {
  const bottom = doc.page.height - 60;
  doc.fontSize(8).fillColor(COLORS.gray)
     .text('This is a computer-generated document. Subject to verification and site survey.', 40, bottom, { align: 'center', width: doc.page.width - 80 });
  doc.fontSize(8).text(`${COMPANY.name} | ${COMPANY.phone} | ${COMPANY.email}`, 40, bottom + 15, { align: 'center', width: doc.page.width - 80 });
}

function drawTable(doc, headers, rows, startY) {
  const colWidths = headers.map(h => h.width);
  const startX = 40;
  const rowHeight = 25;
  let y = startY;

  doc.rect(startX, y, colWidths.reduce((a, b) => a + b, 0), rowHeight).fill(COLORS.dark);
  doc.fillColor('#FFFFFF').fontSize(9).font('Helvetica-Bold');

  let x = startX + 8;
  headers.forEach((h, i) => {
    doc.text(h.label, x, y + 8, { width: colWidths[i] - 16, align: h.align || 'left' });
    x += colWidths[i];
  });

  y += rowHeight;
  doc.font('Helvetica').fontSize(9).fillColor(COLORS.dark);

  rows.forEach((row, rowIdx) => {
    if (rowIdx % 2 === 0) {
      doc.rect(startX, y, colWidths.reduce((a, b) => a + b, 0), rowHeight).fill('#F9FAFB');
    }
    doc.fillColor(COLORS.dark);
    x = startX + 8;
    headers.forEach((h, i) => {
      doc.text(String(row[h.field] ?? ''), x, y + 8, { width: colWidths[i] - 16, align: h.align || 'left' });
      x += colWidths[i];
    });
    y += rowHeight;
  });

  return y;
}

async function generateQuotationPDF(quotation, customer, items) {
  return new Promise((resolve, reject) => {
    try {
      const dir = storage.getUploadPath('quotation_pdfs');
      const filename = `${quotation.quotation_number}.pdf`;
      const filepath = path.join(dir, filename);
      const relativePath = storage.getRelativePath('quotation_pdfs', filename);

      const doc = new PDFDocument({ margin: 40, size: 'A4' });
      const stream = fs.createWriteStream(filepath);
      doc.pipe(stream);

      header(doc);

      doc.fillColor(COLORS.dark).fontSize(20).font('Helvetica-Bold').text('QUOTATION', 40, 120);
      doc.fontSize(10).font('Helvetica').fillColor(COLORS.gray)
         .text(`Quotation #: ${quotation.quotation_number}`, 40, 150)
         .text(`Date: ${new Date(quotation.created_at).toLocaleDateString('en-IN')}`, 40, 165);

      if (quotation.valid_until) {
        doc.text(`Valid Until: ${new Date(quotation.valid_until).toLocaleDateString('en-IN')}`, 40, 180);
      }

      doc.fillColor(COLORS.dark).fontSize(11).font('Helvetica-Bold').text('Customer Details:', 40, 210);
      doc.fontSize(9).font('Helvetica').fillColor(COLORS.gray)
         .text(`Name: ${customer.full_name || quotation.customer_name || 'N/A'}`, 40, 230)
         .text(`Phone: ${customer.phone || quotation.customer_phone || 'N/A'}`, 40, 245)
         .text(`Email: ${customer.email || quotation.customer_email || 'N/A'}`, 40, 260)
         .text(`Address: ${customer.address || quotation.customer_address || 'N/A'}`, 40, 275)
         .text(`City: ${customer.city || quotation.customer_city || 'N/A'} - ${customer.pincode || quotation.customer_pincode || ''}`, 40, 290);

      doc.fillColor(COLORS.dark).fontSize(11).font('Helvetica-Bold').text('System Configuration:', 40, 320);
      doc.fontSize(9).font('Helvetica').fillColor(COLORS.gray)
         .text(`System Size: ${quotation.system_size_kw} kW`, 40, 340)
         .text(`System Type: ${quotation.system_type || 'on-grid'}`, 40, 355);

      const tableHeaders = [
        { label: '#', field: 'sno', width: 40, align: 'center' },
        { label: 'Item', field: 'item_name', width: 220 },
        { label: 'Qty', field: 'quantity', width: 50, align: 'center' },
        { label: 'Unit Price', field: 'unit_price_fmt', width: 100, align: 'right' },
        { label: 'Total', field: 'total_price_fmt', width: 100, align: 'right' },
      ];

      const tableRows = items.map((item, idx) => ({
        sno: idx + 1,
        item_name: item.item_name,
        quantity: item.quantity,
        unit_price_fmt: `Rs ${Number(item.unit_price).toLocaleString('en-IN')}`,
        total_price_fmt: `Rs ${Number(item.total_price).toLocaleString('en-IN')}`,
      }));

      let y = drawTable(doc, tableHeaders, tableRows, 390);
      y += 20;

      const summaryX = 350;
      const valueX = 460;

      doc.fontSize(9).fillColor(COLORS.dark).font('Helvetica');
      doc.text('Subtotal:', summaryX, y);
      doc.text(`Rs ${Number(quotation.subtotal || 0).toLocaleString('en-IN')}`, valueX, y, { align: 'right', width: 100 });

      doc.text('Discount:', summaryX, y + 18);
      doc.text(`- Rs ${Number(quotation.discount || 0).toLocaleString('en-IN')}`, valueX, y + 18, { align: 'right', width: 100 });

      doc.text('GST:', summaryX, y + 36);
      doc.text(`Rs ${Number(quotation.gst_amount || 0).toLocaleString('en-IN')}`, valueX, y + 36, { align: 'right', width: 100 });

      doc.text('Subsidy:', summaryX, y + 54);
      doc.fillColor(COLORS.green);
      doc.text(`- Rs ${Number(quotation.subsidy_amount || 0).toLocaleString('en-IN')}`, valueX, y + 54, { align: 'right', width: 100 });

      doc.rect(summaryX - 10, y + 80, 210, 30).fill(COLORS.primary);
      doc.fillColor('#FFFFFF').font('Helvetica-Bold').fontSize(12);
      doc.text('Final Amount:', summaryX, y + 88);
      doc.text(`Rs ${Number(quotation.final_amount || 0).toLocaleString('en-IN')}`, valueX, y + 88, { align: 'right', width: 100 });

      const termsY = y + 130;
      doc.fillColor(COLORS.dark).fontSize(10).font('Helvetica-Bold').text('Terms & Conditions:', 40, termsY);
      doc.fontSize(8).font('Helvetica').fillColor(COLORS.gray);
      doc.text(quotation.terms_conditions || 'Subject to site survey, DISCOM approval, and final verification.', 40, termsY + 15, { width: 500 });
      doc.text(quotation.payment_terms || '30% advance, 70% before installation.', 40, termsY + 40, { width: 500 });
      doc.text(quotation.warranty_terms || '25 years panel warranty, 5 years inverter.', 40, termsY + 55, { width: 500 });

      footer(doc);
      doc.end();

      stream.on('finish', () => resolve({ filepath, relativePath, filename }));
      stream.on('error', reject);
    } catch (err) {
      reject(err);
    }
  });
}

module.exports = { generateQuotationPDF, COMPANY };