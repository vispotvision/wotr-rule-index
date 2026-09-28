// Markdown in-world document -> house docx (dark ground, gold EB Garamond).
//   node codex_docx.js IN.md OUT.docx "Running head"
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, Footer, PageNumber,
  BorderStyle, PageBreak,
} = require("docx");

const [, , inPath, outPath, runningHead] = process.argv;
const GROUND = "15120F", GOLD = "D4AF37", BODY = "E3CFA0", DIM = "A8925F";
const FONT = "EB Garamond";

// **bold**, *italic*, `code` inline runs
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), ...base, bold: true }));
    else if (t.startsWith("*")) out.push(new TextRun({ text: t.slice(1, -1), ...base, italics: !base.italics }));
    else out.push(new TextRun({ text: t.slice(1, -1), ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

const lines = fs.readFileSync(inPath, "utf8").replace(/\r\n/g, "\n").split("\n");
const kids = [];
let quote = [];
let seenChapter = false;

function flushQuote() {
  if (!quote.length) return;
  const parts = quote.join("\n").split(/\n\s*\n/);
  for (const p of parts) {
    const s = p.replace(/\n/g, " ").trim();
    if (!s) continue;
    kids.push(new Paragraph({
      children: runs(s, { italics: true, color: BODY }),
      indent: { left: 720, right: 720 },
      spacing: { before: 120, after: 120, line: 300 },
      alignment: AlignmentType.JUSTIFIED,
    }));
  }
  quote = [];
}

for (const raw of lines) {
  const s = raw.trim();
  if (s.startsWith(">")) { quote.push(s.slice(1).trim()); continue; }
  flushQuote();
  if (!s) continue;
  let m;
  if ((m = s.match(/^# (.*)$/))) {
    kids.push(new Paragraph({ children: [new TextRun({ text: m[1], color: GOLD, size: 56, bold: true, characterSpacing: 60 })],
      alignment: AlignmentType.CENTER, spacing: { before: 2400, after: 240 } }));
  } else if ((m = s.match(/^### (.*)$/)) && seenChapter) {
    kids.push(new Paragraph({ children: [new TextRun({ text: m[1], color: GOLD, size: 26, bold: true, italics: true })],
      spacing: { before: 280, after: 120 } }));
  } else if ((m = s.match(/^### (.*)$/))) {
    kids.push(new Paragraph({ children: [new TextRun({ text: m[1], color: DIM, size: 28, italics: true })],
      alignment: AlignmentType.CENTER, spacing: { before: 120, after: 1200 } }));
  } else if ((m = s.match(/^## (.*)$/))) {
    const isChapter = /^(Chapter|Appendix|A Note|Entry|Preliminary|Exhibit|Closing|The Case File|Edition|Preface|Book|Part)/.test(m[1]);
    if (isChapter) seenChapter = true;
    if (isChapter) {
      kids.push(new Paragraph({ children: [new PageBreak()] }));
      kids.push(new Paragraph({ children: [new TextRun({ text: m[1], color: GOLD, size: 36, bold: true })],
        alignment: AlignmentType.CENTER, spacing: { before: 600, after: 480 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: DIM, space: 8 } } }));
    } else {
      kids.push(new Paragraph({ children: [new TextRun({ text: m[1], color: GOLD, size: 40, italics: true })],
        alignment: AlignmentType.CENTER, spacing: { before: 120, after: 120 } }));
    }
  } else if (/^(-{3,}|\*{3,})$/.test(s)) {
    kids.push(new Paragraph({ children: [new TextRun({ text: "❦", color: DIM, size: 28 })],
      alignment: AlignmentType.CENTER, spacing: { before: 240, after: 240 } }));
  } else {
    kids.push(new Paragraph({ children: runs(s, { color: BODY }),
      alignment: AlignmentType.JUSTIFIED, indent: { firstLine: 360 },
      spacing: { after: 160, line: 312 } }));
  }
}
flushQuote();

const doc = new Document({
  background: { color: GROUND },
  styles: { default: { document: { run: { font: FONT, size: 24, color: BODY } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
      margin: { top: 1440, bottom: 1440, left: 1620, right: 1620 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: runningHead + "  ·  ", color: DIM, size: 18, italics: true }),
                 new TextRun({ children: [PageNumber.CURRENT], color: DIM, size: 18 })] })] }) },
    children: kids,
  }],
});
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(outPath, b); console.log("wrote", outPath, b.length); });
