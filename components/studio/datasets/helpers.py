from fpdf import FPDF

def create_pdf(questions, answers, dataset):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(200, 10, txt = "Datasheet for " + dataset, ln = 1, allign = "C")
    for q, a in questions, answers:
        pdf.cell(200, 10, txt = "", ln =1, allign = "L")
        pdf.set_font("Arial", "B", 11)
        pdf.cell(200, 10, txt = q , ln = 1, allign = "L")
        pdf.set_font("Arial", "", 11)
        pdf.cell(200, 10, txt = a, ln = 1, alligt = "L")
    pdf.output("datasheet_{}".format(dataset))
        