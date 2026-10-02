'use strict';

const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');
const storage = require('../config/storage');
const db = require('../config/db');

/**
 * NP POWER TECH SOLAR - PDF Generation Service
 * 3-page quotation format - all values dynamic from DB.
 */

const COLORS = {
  primary: '#000000',
  gray: '#333333',
  border: '#000000',
  header: '#1F2937',
  white: '#FFFFFF',
};

// ---------- Load settings ----------
async function loadSettings() {
  const result = await db.query(
    `SELECT key, value FROM website_settings 
     WHERE category IN ('general', 'contact', 'legal', 'bank', 'quotations')`,
  );
  const settings = {};
  for (const row of result.rows) settings[row.key] = row.value;
  return settings;
}

// ---------- BOM Table ----------
function drawBOMTable(doc, items, startX, startY) {
  const headers = ['SR. NO.', 'TECHNICAL DETAILS', 'MAKE', 'CAPACITY', 'QUANTITY'];
  const colWidths = [50, 175, 110, 105, 80];
  const rowHeight = 22;

  let y = startY;
  const tableWidth = colWidths.reduce((a, b) => a + b, 0);

  // Header row
  doc.rect(startX, y, tableWidth, rowHeight).fill(COLORS.header);
  doc.fillColor(COLORS.white).fontSize(8).font('Helvetica-Bold');

  let x = startX;
  headers.forEach((h, i) => {
    doc.text(h, x + 4, y + 7, { width: colWidths[i] - 8, align: 'left' });
    x += colWidths[i];
  });
  y += rowHeight;

  // Data rows
  doc.font('Helvetica').fontSize(8).fillColor(COLORS.primary);

  items.forEach((item) => {
    x = startX;
    const row = [
      String(item.sr || ''),
      item.technical_details || '',
      item.make || '',
      item.capacity || '',
      item.quantity || '',
    ];
    row.forEach((cell, i) => {
      doc.text(String(cell), x + 4, y + 6, { width: colWidths[i] - 8, align: 'left' });
      x += colWidths[i];
    });
    doc.rect(startX, y, tableWidth, rowHeight).strokeColor(COLORS.border).stroke();
    y += rowHeight;
  });

  return y;
}

// ---------- Header ----------
function drawHeader(doc, settings) {
  const startX = 40;
  let y = 40;

  const logoPath = path.join(__dirname, '..', '..', 'assets', 'logo.png');
  if (fs.existsSync(logoPath)) {
    try {
      doc.image(logoPath, doc.page.width / 2 - 30, 30, { width: 60 });
      y = 100;
    } catch (err) {
      // Continue without logo
    }
  }

  const companyName = settings.company_name || 'NP POWER TECH SOLAR';

  doc.fontSize(16).font('Helvetica-Bold').fillColor(COLORS.primary)
     .text(companyName, startX, y, { align: 'center', width: doc.page.width - 80 });
  y += 22;

  return y;
}

// ---------- Footer (EMPTY - removed) ----------
function drawFooter(doc) {
  return;
}

// ---------- MAIN: Generate Quotation PDF ----------
async function generateQuotationPDF(quotation, customer, items) {
  return new Promise(async (resolve, reject) => {
    try {
      const settings = await loadSettings();

      // Prepare BOM items — filter out empty/invalid
      let bomItems = items
        .filter((item) => item.item_name && item.item_name.trim().length > 0)
        .map((item, idx) => ({
          sr: idx + 1,
          technical_details: item.item_name || '',
          make: item.make || item.brand || 'STANDARD',
          capacity: item.capacity || '-',
          quantity: `${item.quantity || 1}`,
        }));

      // Use default template if real items not available
      if (bomItems.length < 5) {
        bomItems = [
          { sr: 1, technical_details: 'SOLAR MODULE', make: 'INA', capacity: '600W', quantity: '5' },
          { sr: 2, technical_details: 'PCU/INVERTER', make: 'FESTON', capacity: '5 KW', quantity: '1' },
          { sr: 3, technical_details: 'COMPLETE SET OF STRUCTURE', make: 'G. I STANDARD', capacity: 'TATA', quantity: '1 SET' },
          { sr: 4, technical_details: 'DC CABLE', make: 'POLYCAB/FINOLAX/STD. MAKE', capacity: '1C*4sq mm Tin Coated', quantity: 'AS PER SITE REQUIRED' },
          { sr: 5, technical_details: 'AC CABLE', make: 'POLYCAB/FINOLAX/STD. MAKE', capacity: '10sq mm', quantity: 'AS PER SITE REQUIRED' },
          { sr: 6, technical_details: 'EARTHING SET WITH LA', make: 'STANDARD', capacity: 'SET', quantity: '3' },
          { sr: 7, technical_details: 'DCBB', make: 'STANDARD', capacity: 'SET', quantity: '1' },
          { sr: 8, technical_details: 'ACDB', make: 'STANDARD', capacity: 'SET', quantity: '1' },
          { sr: 9, technical_details: 'BALANCE OF SYSTEM', make: 'STANDARD', capacity: 'SET', quantity: 'AS PER SYSTEM' },
          { sr: 10, technical_details: 'NET/SOLAR METER', make: 'L&T', capacity: 'SET', quantity: '1' },
        ];
      }

      const dir = storage.getUploadPath('quotation_pdfs');
      const filename = `${quotation.quotation_number}.pdf`;
      const filepath = path.join(dir, filename);
      const relativePath = storage.getRelativePath('quotation_pdfs', filename);

      const doc = new PDFDocument({ margin: 40, size: 'A4', autoFirstPage: true });
      const stream = fs.createWriteStream(filepath);
      doc.pipe(stream);

      const startX = 40;

      // ============================================================
      // PAGE 1 - Header + Customer + BOM Table
      // ============================================================
      let y = drawHeader(doc, settings);

      // Date
      const today = new Date().toLocaleDateString('en-IN', {
        day: '2-digit', month: '2-digit', year: 'numeric',
      }).replace(/\//g, '-');

      doc.fontSize(11).font('Helvetica-Bold').fillColor(COLORS.primary);
      doc.text(`DATE: ${today}`, startX, y);
      y += 22;

      // TO
      doc.fontSize(11).font('Helvetica-Bold').text('TO,', startX, y);
      y += 16;
      doc.text(`MR. ${customer.full_name || quotation.customer_name || 'CUSTOMER'}`, startX, y);
      y += 14;
      doc.text(`ADDRESS: ${customer.city || quotation.customer_city || 'INDIA'}`, startX, y);
      y += 25;

      // Title — fix double "ON"
      let systemType = (quotation.system_type || 'on-grid').toUpperCase().replace('-', ' ');
      systemType = systemType.replace(/^ON\s+/i, '');
      doc.fontSize(11).font('Helvetica-Bold').fillColor(COLORS.primary);
      doc.text(
        `ERECTION & COMMISSIONING OF ${quotation.system_size_kw} KWP SOLAR ON ${systemType} POWER PLANT.`,
        startX, y,
        { width: doc.page.width - 80 },
      );
      y += 30;

      // Reference paragraph
      doc.fontSize(9).font('Helvetica').fillColor(COLORS.primary);
      doc.text(
        'WITH REFERENCE TO OUR DISCUSSION, WE ARE VERY PLEASED TO OFFER YOU OF OUR BEST PROPOSAL FOR ROOF TOP SOLAR ON GRID POWER PLANT AS FOLLOWS:',
        startX, y,
        { width: doc.page.width - 80 },
      );
      y += 28;

      // BOM Table
      doc.fontSize(11).font('Helvetica-Bold').fillColor(COLORS.primary);
      doc.text('BILL OF MATERIAL ON GRID SOLAR SYSTEM', startX, y);
      y += 18;

      y = drawBOMTable(doc, bomItems, startX, y);

      // ============================================================
      // PAGE 2 - Commercial Details
      // ============================================================
      doc.addPage();
      y = 40;

      // 1. PROJECT COST
      doc.fontSize(11).font('Helvetica-Bold').fillColor(COLORS.primary);
      doc.text('1 PROJECT COST', startX, y);
      y += 18;

      const systemCost = Number(quotation.final_amount || 0).toLocaleString('en-IN');
      const gstStatus = settings.gst_status || 'NIL';
      const discomStatus = settings.discom_status || 'INCLUDED';

      doc.fontSize(9).font('Helvetica').fillColor(COLORS.primary);
      doc.text(`PLANT SIZE: ${quotation.system_size_kw} KW`, startX + 20, y);
      y += 13;
      doc.text(`SYSTEM COST: INR ${systemCost}/-`, startX + 20, y);
      y += 13;
      doc.text(`GST PAID EXTRA: ${gstStatus}`, startX + 20, y);
      y += 13;
      doc.text(`DISCOM CHARGE: ${discomStatus}`, startX + 20, y);
      y += 25;

      // 2. PAYMENT TERMS
      doc.fontSize(11).font('Helvetica-Bold').text('2 PAYMENT TERMS', startX, y);
      y += 15;
      doc.fontSize(9).font('Helvetica');
      doc.text('* 10% - MOBILIZATION ADVANCE AGAINST WORK ORDER.', startX + 20, y);
      y += 12;
      doc.text('* 85% - BEFORE DELIVERY OF MATERIAL', startX + 20, y);
      y += 12;
      doc.text('* 5% - AFTER SUCCESSFUL COMMISSIONING OF PLANT.', startX + 20, y);
      y += 22;

      // 3. PROJECT COMPLETION
      doc.fontSize(11).font('Helvetica-Bold').text('3 PROJECT COMPLETION', startX, y);
      y += 15;
      doc.fontSize(9).font('Helvetica');
      const compDays = settings.project_completion_days || '10-15';
      const compStart = settings.project_completion_start || 'FROM THE CLEAR ORDER AND ADVANCE PAYMENT';
      doc.text(compDays + ' DAYS ' + compStart, startX + 20, y);
      y += 22;

      // 4. VALIDITY OF OFFER
      doc.fontSize(11).font('Helvetica-Bold').text('4 VALIDITY OF OFFER', startX, y);
      y += 15;
      doc.fontSize(9).font('Helvetica');
      const validityDays = settings.validity_days || '2';
      const validityMsg = settings.validity_message || '';
      doc.text(validityDays + ' DAYS FROM THE DATE OF OFFER. ' + validityMsg, startX + 20, y, { width: doc.page.width - 100 });
      y += 22;

      // 5. CLIENT SCOPE
      doc.fontSize(11).font('Helvetica-Bold').text('5 CLIENT SCOPE', startX, y);
      y += 15;
      doc.fontSize(9).font('Helvetica');
      const clientScope = [];
      for (let i = 1; i <= 10; i++) {
        const s = settings['client_scope_' + i];
        if (s && s.trim()) clientScope.push(s);
      }
      if (clientScope.length === 0) {
        clientScope.push('CLEANING OF SOLAR MODULES IN YOUR SCOPE.');
        clientScope.push('ONE PERSON FROM CLIENT SIDE FOR BASIC TRAINING.');
      }
      clientScope.forEach((point) => {
        doc.text('* ' + point, startX + 20, y, { width: doc.page.width - 100 });
        y += doc.heightOfString('* ' + point, { width: doc.page.width - 100 }) + 3;
      });
      y += 8;

      // 6. TRANSPORTATION
      doc.fontSize(11).font('Helvetica-Bold').text('6 TRANSPORTATION', startX, y);
      y += 15;
      doc.fontSize(9).font('Helvetica');
      doc.text(settings.transportation_status || 'INCLUDED', startX + 20, y);
      y += 22;

      // 7. OFFICIAL FEES
      doc.fontSize(11).font('Helvetica-Bold').text('7 OFFICIAL FEES', startX, y);
      y += 15;
      doc.fontSize(9).font('Helvetica');
      doc.text(settings.official_fees || 'AS APPLICABLE', startX + 20, y);

      // ============================================================
      // PAGE 3 - Warranty + Bank + Signature
      // ============================================================
      doc.addPage();
      y = 40;

      // WARRANTY
      doc.fontSize(11).font('Helvetica-Bold').fillColor(COLORS.primary);
      doc.text('WARRANTY', startX, y);
      y += 15;
      doc.fontSize(9).font('Helvetica');
      doc.text('5 YEAR COMPLETE SYSTEM WARRANTY.', startX + 20, y);
      y += 12;
      doc.text('SOLAR MODULE PERFORMANCE WARRANTY 25 YEAR (AS PER MNRE NORMS)', startX + 20, y);
      y += 12;
      doc.text('SOLAR INVERTER 10 YEAR.', startX + 20, y);
      y += 22;

      // SPACE REQUIREMENT
      doc.text(
        'SPACE REQUIREMENT: - SHADOW FREE SPACE FOR INSTALLATION OF SOLAR MODULE.',
        startX, y,
        { width: doc.page.width - 80 },
      );
      y += 18;

      doc.text(
        'HOPE THE ABOVE WILL BE IN LINE WITH YOUR REQUIREMENTS, HOWEVER IF YOU REQUIRE FURTHER INFORMATION PLEASE FEEL FREE TO CONTACT US. THANKING YOU AND ASSURING YOU OF OUR VERY BEST & PROMPT ATTENTION AT ALL TIMES, WE REMAIN.',
        startX, y,
        { width: doc.page.width - 80 },
      );
      y += 30;

      // YOURS FAITHFULLY
      doc.fontSize(9).font('Helvetica').fillColor(COLORS.primary);
      doc.text('YOURS FAITHFULLY', startX, y);
      y += 12;
      doc.text('THANKS & REGARDS,', startX, y);
      y += 12;
      doc.text('FOR, NP POWER TECH SOLAR', startX, y);
      y += 25;

      // OFFICE + CONTACT
      const office = settings.company_office || 'POLICE THANE KE PICHIE, GOVINDGARH - 303712';
      const contact = settings.contact_person_1 || 'MR. DINESH YADAV';
      const phone1 = settings.contact_phone_1 || '9610991048';
      const phone2 = settings.contact_phone_2 || '7357968185';
      const gst = settings.company_gst || '08BGUPY4859C1ZJ';
      const email = settings.company_email || 'nppowertechsolar@gmail.com';

      doc.fontSize(8).font('Helvetica').fillColor(COLORS.primary);
      doc.text(`OFFICE: - ${office}`, startX, y, { width: doc.page.width - 80 });
      y += 12;
      doc.text(`${contact}, MOB.- ${phone1}, ${phone2}`, startX, y, { width: doc.page.width - 80 });
      y += 12;
      doc.text(`GST IN: - ${gst}`, startX, y);
      y += 12;
      doc.text(`E- MAIL: - ${email}`, startX, y);
      y += 25;

      // COMPANY'S BANK DETAILS
      doc.fontSize(11).font('Helvetica-Bold').text("COMPANY'S BANK DETAILS", startX, y);
      y += 15;

      const bankRows = [
        ['BANK NAME', settings.bank_name || 'SBI BANK'],
        ['A/C NO.', settings.bank_account_no || '44941015635'],
        ['BRANCH & IFSC CODE', `${settings.bank_branch || 'GOVINDGARH'}, ${settings.bank_ifsc || 'SBIN0031042'}`],
      ];

      const bankTableWidth = doc.page.width - 80;
      const bankRowHeight = 16;

      doc.fontSize(8).font('Helvetica').fillColor(COLORS.primary);
      bankRows.forEach(([label, value]) => {
        doc.font('Helvetica-Bold').text(label, startX, y, { width: 150 });
        doc.font('Helvetica').text(value, startX + 160, y, { width: bankTableWidth - 160 });
        y += bankRowHeight;
      });

      doc.end();

      stream.on('finish', () => resolve({ filepath, relativePath, filename }));
      stream.on('error', reject);
    } catch (err) {
      reject(err);
    }
  });
}

async function generateInvoicePDF(invoice, customer, items) {
  throw new Error('Invoice PDF not yet implemented');
}

module.exports = { generateQuotationPDF, generateInvoicePDF };