'use strict';

const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');
const storage = require('../config/storage');
const db = require('../config/db');

/**
 * PDF generation service.
 * Matches NP POWER TECH SOLAR's standard quotation format.
 * Bank details priority: quotation-specific → settings → default
 * Logo support added.
 */

const COLORS = {
  primary: '#1F2937',
  accent: '#F59E0B',
  gray: '#6B7280',
  light: '#F3F4F6',
  border: '#D1D5DB',
  header: '#1F2937',
  white: '#FFFFFF',
  rowAlt: '#F9FAFB',
};

// ---------- Load settings from DB ----------
async function loadSettings() {
  const result = await db.query(
    `SELECT key, value FROM website_settings 
     WHERE category IN ('general', 'contact', 'legal', 'bank', 'quotations', 'branding')`,
  );
  const settings = {};
  for (const row of result.rows) {
    if (row.value && row.value.trim() !== '') {
      settings[row.key] = row.value;
    }
  }

  // Fallback defaults
  const DEFAULTS = {
    company_name: 'NP POWER TECH SOLAR',
    company_office: 'POLICE THANE KE PICHIE, GOVINDGARH - 303712',
    company_email: 'D7357968185@GMAIL.COM',
    company_gst: '08BGUPY4859C1ZJ',
    contact_person_1: 'MR. DINESH YADAV',
    contact_phone_1: '9610991048',
    contact_phone_2: '7357968185',
    bank_name: 'SBI BANK',
    bank_account_no: '44941015635',
    bank_ifsc: 'SBIN0031042',
    bank_branch: 'GOVINDGARH',
    payment_terms: '10% Mobilization Advance + 85% Before Delivery + 5% After Commissioning',
    project_completion_days: '10-15',
    validity_days: '2',
    warranty_system: '5 Year Complete System Warranty',
    warranty_module: '25 Year Solar Module Performance Warranty (as per MNRE Norms)',
    warranty_inverter: '10 Year Solar Inverter Warranty',
    client_scope: 'Cleaning of solar modules|One person from client side for basic training|Roof to be arranged by client|Electricity & water during construction|Safe storage space for material|Electricity supply for inverter synchronization|Connection space in LT panel|Internet connection for remote monitoring',
  };

  for (const [key, value] of Object.entries(DEFAULTS)) {
    if (!settings[key]) {
      settings[key] = value;
    }
  }

  return settings;
}

// ---------- Draw header (with logo support) ----------
function drawHeader(doc, settings) {
  const companyName = settings.company_name;

  // ---------- Try to load logo ----------
  let logoRendered = false;
  if (settings.company_logo_path) {
    try {
      const logoRelPath = settings.company_logo_path.replace(/^\/uploads\//, '');
      const logoPath = path.join(__dirname, '..', '..', '..', 'storage', 'uploads', logoRelPath);

      if (fs.existsSync(logoPath)) {
        doc.image(logoPath, 40, 40, { fit: [90, 90] });
        logoRendered = true;
      }
    } catch (err) {
      logoRendered = false;
    }
  }

  // ---------- Company info ----------
  if (logoRendered) {
    // Logo on left → text aligned left starting at x=145
    const textX = 145;
    const textWidth = doc.page.width - textX - 40;

    doc.fontSize(20)
       .font('Helvetica-Bold')
       .fillColor(COLORS.primary)
       .text(companyName, textX, 45, { align: 'left', width: textWidth });

    doc.fontSize(9)
       .font('Helvetica')
       .fillColor(COLORS.gray)
       .text(`OFFICE: ${settings.company_office}`, textX, 72, { align: 'left', width: textWidth });

    doc.fontSize(9)
       .text(`${settings.contact_person_1}, MOB: ${settings.contact_phone_1}, ${settings.contact_phone_2}`, textX, 85, { align: 'left', width: textWidth });

    doc.fontSize(9)
       .text(`GST IN: ${settings.company_gst}   E-MAIL: ${settings.company_email}`, textX, 98, { align: 'left', width: textWidth });
  } else {
    // No logo → original centered layout
    doc.fontSize(22)
       .font('Helvetica-Bold')
       .fillColor(COLORS.primary)
       .text(companyName, 0, 50, { align: 'center' });

    doc.fontSize(10)
       .font('Helvetica')
       .fillColor(COLORS.gray)
       .text(`OFFICE: ${settings.company_office}`, 0, 80, { align: 'center' });

    doc.fontSize(10)
       .text(`${settings.contact_person_1}, MOB: ${settings.contact_phone_1}, ${settings.contact_phone_2}`, 0, 95, { align: 'center' });

    doc.fontSize(10)
       .text(`GST IN: ${settings.company_gst}   E-MAIL: ${settings.company_email}`, 0, 110, { align: 'center' });
  }

  // Divider
  doc.moveTo(40, 135).lineTo(doc.page.width - 40, 135).strokeColor(COLORS.border).stroke();
}

// ---------- Draw BOM table ----------
function drawBOMTable(doc, items, startY) {
  const startX = 40;
  const tableWidth = doc.page.width - 80;
  const headers = ['SR. NO.', 'TECHNICAL DETAILS', 'MAKE', 'CAPACITY', 'QUANTITY'];
  const colWidths = [50, 190, 110, 110, 60];
  const rowHeight = 25;

  let y = startY;

  doc.fontSize(14)
     .font('Helvetica-Bold')
     .fillColor(COLORS.primary)
     .text('BILL OF MATERIAL ON GRID SOLAR SYSTEM', startX, y);
  y += 25;

  doc.rect(startX, y, tableWidth, rowHeight).fill(COLORS.header);
  doc.fillColor(COLORS.white).fontSize(9).font('Helvetica-Bold');

  let x = startX;
  headers.forEach((h, i) => {
    doc.text(h, x + 5, y + 8, { width: colWidths[i] - 10, align: 'left' });
    x += colWidths[i];
  });
  y += rowHeight;

  doc.font('Helvetica').fontSize(9).fillColor(COLORS.primary);

  items.forEach((item, idx) => {
    if (idx % 2 === 0) {
      doc.rect(startX, y, tableWidth, rowHeight).fill(COLORS.rowAlt);
    }
    doc.fillColor(COLORS.primary);

    x = startX;
    const row = [
      String(idx + 1),
      item.technical_details || '',
      item.make || '',
      item.capacity || '',
      item.quantity || '',
    ];

    row.forEach((cell, i) => {
      doc.text(String(cell), x + 5, y + 8, { width: colWidths[i] - 10, align: 'left' });
      x += colWidths[i];
    });

    doc.moveTo(startX, y + rowHeight).lineTo(startX + tableWidth, y + rowHeight)
       .strokeColor(COLORS.border).stroke();

    y += rowHeight;
  });

  doc.rect(startX, startY + 25, tableWidth, y - (startY + 25)).strokeColor(COLORS.border).stroke();

  return y + 15;
}

// ---------- Draw commercial details ----------
function drawCommercialDetails(doc, quotation, settings, startY) {
  const startX = 40;
  const contentWidth = doc.page.width - 80;

  if (startY > doc.page.height - 300) {
    doc.addPage();
    startY = 40;
  }

  doc.fontSize(14)
     .font('Helvetica-Bold')
     .fillColor(COLORS.primary)
     .text('COMMERCIAL DETAILS', startX, startY);

  let y = startY + 30;

  const rows = [
    {
      label: '1. PROJECT COST',
      value: `Plant Size: ${quotation.system_size_kw} KW\nSystem Cost: INR ${Number(quotation.final_amount || 0).toLocaleString('en-IN')}/-\nGST: Extra as applicable\nDISCOM Charge: Included`,
    },
    {
      label: '2. PAYMENT TERMS',
      value: settings.payment_terms,
    },
    {
      label: '3. PROJECT COMPLETION',
      value: `${settings.project_completion_days} days from clear order & advance payment`,
    },
    {
      label: '4. VALIDITY OF OFFER',
      value: `${settings.validity_days} days from date of offer`,
    },
    {
      label: '5. CLIENT SCOPE',
      value: settings.client_scope.split('|').map((s, i) => `${i + 1}. ${s}`).join('\n'),
    },
    {
      label: '6. TRANSPORTATION',
      value: 'Included',
    },
    {
      label: '7. OFFICIAL FEES',
      value: 'As applicable',
    },
  ];

  rows.forEach((row) => {
    doc.fontSize(10).font('Helvetica-Bold').fillColor(COLORS.primary);
    doc.text(row.label, startX, y, { width: 140 });

    doc.fontSize(9).font('Helvetica').fillColor('#374151');
    doc.text(row.value, startX + 150, y, { width: contentWidth - 150 });

    const textHeight = doc.heightOfString(row.value, { width: contentWidth - 150 });
    y += Math.max(textHeight + 10, 25);
  });

  return y + 10;
}

// ---------- Draw warranty ----------
function drawWarranty(doc, settings, startY) {
  const startX = 40;

  if (startY > doc.page.height - 200) {
    doc.addPage();
    startY = 40;
  }

  let y = startY + 10;

  doc.fontSize(14)
     .font('Helvetica-Bold')
     .fillColor(COLORS.primary)
     .text('WARRANTY', startX, y);
  y += 25;

  const warranties = [
    settings.warranty_system,
    settings.warranty_module,
    settings.warranty_inverter,
  ];

  doc.fontSize(10).font('Helvetica').fillColor('#374151');
  warranties.forEach((w) => {
    doc.text(`•  ${w}`, startX, y);
    y += 18;
  });

  return y + 15;
}

// ---------- Draw bank details (TABLE FORMAT with priority) ----------
function drawBankDetails(doc, settings, startY, quotation = null) {
  const startX = 40;
  const tableWidth = doc.page.width - 80;
  const rowHeight = 25;
  const col1Width = 180;
  const col2Width = tableWidth - col1Width;

  if (startY > doc.page.height - 200) {
    doc.addPage();
    startY = 40;
  }

  let y = startY + 10;

  doc.fontSize(14)
     .font('Helvetica-Bold')
     .fillColor(COLORS.primary)
     .text("COMPANY'S BANK DETAILS", startX, y);
  y += 25;

  // Header row
  doc.rect(startX, y, tableWidth, rowHeight).fill(COLORS.header);
  doc.fillColor(COLORS.white).fontSize(11).font('Helvetica-Bold');
  doc.text("COMPANY'S BANK DETAILS", startX + 10, y + 7, { width: tableWidth - 20, align: 'center' });
  y += rowHeight;

  // Company name row
  doc.rect(startX, y, tableWidth, rowHeight).fill(COLORS.light);
  doc.rect(startX, y, tableWidth, rowHeight).strokeColor(COLORS.border).stroke();
  doc.fillColor(COLORS.primary).fontSize(10).font('Helvetica-Bold');
  doc.text(settings.company_name, startX + 10, y + 8, { width: tableWidth - 20 });
  y += rowHeight;

  // PRIORITY: quotation → settings → default
  const bankName = (quotation && quotation.bank_name) || settings.bank_name || 'SBI BANK';
  const bankAcc = (quotation && quotation.bank_account_no) || settings.bank_account_no || '44941015635';
  const bankIfsc = (quotation && quotation.bank_ifsc) || settings.bank_ifsc || 'SBIN0031042';
  const bankBranch = (quotation && quotation.bank_branch) || settings.bank_branch || 'GOVINDGARH';

  const bankRows = [
    ['BANK NAME', bankName],
    ['A/C NO.', bankAcc],
    ['BRANCH & IFSC CODE', `${bankBranch}, ${bankIfsc}`],
  ];

  bankRows.forEach(([label, value], idx) => {
    const bgColor = idx % 2 === 0 ? COLORS.white : COLORS.rowAlt;

    doc.rect(startX, y, tableWidth, rowHeight).fill(bgColor);
    doc.rect(startX, y, col1Width, rowHeight).fill(COLORS.light);
    doc.rect(startX, y, tableWidth, rowHeight).strokeColor(COLORS.border).stroke();
    doc.moveTo(startX + col1Width, y).lineTo(startX + col1Width, y + rowHeight).strokeColor(COLORS.border).stroke();

    doc.fillColor(COLORS.primary).fontSize(9).font('Helvetica-Bold');
    doc.text(label, startX + 10, y + 8, { width: col1Width - 20 });

    doc.fillColor('#374151').font('Helvetica').fontSize(10);
    doc.text(value, startX + col1Width + 10, y + 8, { width: col2Width - 20 });

    y += rowHeight;
  });

  return y + 20;
}

// ---------- Draw footer ----------
function drawFooter(doc) {
  const bottom = doc.page.height - 40;
  doc.fontSize(8)
     .fillColor(COLORS.gray)
     .text(
       'This is a computer-generated quotation. Subject to verification and site survey.',
       40, bottom, { align: 'center', width: doc.page.width - 80 },
     );
}

// ---------- Draw signature ----------
function drawSignature(doc, startY) {
  if (startY > doc.page.height - 150) {
    doc.addPage();
    startY = 40;
  }

  const startX = doc.page.width - 220;
  let y = startY + 20;

  doc.fontSize(10)
     .font('Helvetica')
     .fillColor(COLORS.primary)
     .text('Yours Faithfully,', startX, y);
  y += 18;
  doc.text('Thanks & Regards,', startX, y);
  y += 18;
  doc.font('Helvetica-Bold').text('FOR, NP POWER TECH SOLAR', startX, y);
  y += 45;

  doc.moveTo(startX, y).lineTo(startX + 150, y).strokeColor(COLORS.border).stroke();
  y += 5;

  doc.fontSize(9).font('Helvetica').fillColor(COLORS.gray);
  doc.text('Authorised Signatory', startX, y);

  return y;
}

// ============================================================
// MAIN: Generate Quotation PDF
// ============================================================
async function generateQuotationPDF(quotation, customer, items) {
  return new Promise(async (resolve, reject) => {
    try {
      const settings = await loadSettings();

      const bomItems = items.map((item) => ({
        technical_details: item.item_name || '',
        make: item.make || item.brand || 'STANDARD',
        capacity: item.capacity || '',
        quantity: `${item.quantity || 1} ${item.unit || 'SET'}`,
      }));

      if (bomItems.length === 0) {
        bomItems.push(
          { technical_details: 'SOLAR MODULE', make: 'INA', capacity: '600W', quantity: '5' },
          { technical_details: 'PCU/INVERTER', make: 'FESTON', capacity: '5 KW', quantity: '1' },
          { technical_details: 'COMPLETE SET OF STRUCTURE', make: 'G.I STANDARD', capacity: '-', quantity: '1 SET' },
          { technical_details: 'DC CABLE', make: 'POLYCAB', capacity: '1C*4sq mm', quantity: 'As per site' },
          { technical_details: 'AC CABLE', make: 'POLYCAB', capacity: '10sq mm', quantity: 'As per site' },
          { technical_details: 'EARTHING SET WITH LA', make: 'STANDARD', capacity: '-', quantity: '3 SET' },
          { technical_details: 'DCBB', make: 'STANDARD', capacity: '-', quantity: '1' },
          { technical_details: 'ACDB', make: 'STANDARD', capacity: '-', quantity: '1' },
          { technical_details: 'BALANCE OF SYSTEM', make: 'STANDARD', capacity: '-', quantity: 'As per system' },
          { technical_details: 'NET/SOLAR METER', make: 'L&T', capacity: '-', quantity: '1 SET' },
        );
      }

      const dir = storage.getUploadPath('quotation_pdfs');
      const filename = `${quotation.quotation_number}.pdf`;
      const filepath = path.join(dir, filename);
      const relativePath = storage.getRelativePath('quotation_pdfs', filename);

      const doc = new PDFDocument({ margin: 40, size: 'A4' });
      const stream = fs.createWriteStream(filepath);
      doc.pipe(stream);

      drawHeader(doc, settings);

      const today = new Date().toLocaleDateString('en-IN', {
        day: '2-digit', month: '2-digit', year: 'numeric',
      }).replace(/\//g, '-');

      doc.fontSize(10).font('Helvetica-Bold').fillColor(COLORS.primary);
      doc.text(`DATE: ${today}`, 40, 150);

      doc.fontSize(10).font('Helvetica-Bold').text('TO,', 40, 175);
      doc.fontSize(11).text(`MR. ${customer.full_name || quotation.customer_name || 'CUSTOMER'}`, 40, 190);
      doc.fontSize(10).font('Helvetica').text(`ADDRESS: ${customer.city || quotation.customer_city || 'INDIA'}`, 40, 205);

      doc.fontSize(11).font('Helvetica-Bold').fillColor(COLORS.primary);
      doc.text(
        `ERECTION & COMMISSIONING OF ${quotation.system_size_kw} KWP SOLAR ON GRID POWER PLANT`,
        40, 235,
        { align: 'left' },
      );

      doc.fontSize(9).font('Helvetica').fillColor('#374151');
      doc.text(
        'WITH REFERENCE TO OUR DISCUSSION, WE ARE VERY PLEASED TO OFFER YOU OF OUR BEST PROPOSAL FOR ROOF TOP SOLAR ON GRID POWER PLANT AS FOLLOWS:',
        40, 260,
        { width: doc.page.width - 80 },
      );

      let y = 295;
      y = drawBOMTable(doc, bomItems, y);
      y = drawCommercialDetails(doc, quotation, settings, y + 10);
      y = drawWarranty(doc, settings, y);
      y = drawBankDetails(doc, settings, y, quotation);
      drawSignature(doc, y);
      drawFooter(doc);

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

module.exports = {
  generateQuotationPDF,
  generateInvoicePDF,
};