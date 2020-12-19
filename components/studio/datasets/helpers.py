#from fpdf import FPDF
import itertools
from .forms import DatasheetForm

def create_pdf(qa, name):
    pdf = FPDF()
    pdf.set_left_margin(35)
    pdf.add_page()
    pdf.set_fill_color(243, 243, 243)
    pdf.rect(0 , 0 , 30, 297 ,'F')
    pdf.image('./static/img/stackn.png', 3, 3, 25)
    pdf.add_font('IBMPlexSans', '', './static/fonts/IBMPlexSans-Regular.ttf', uni=True)
    pdf.add_font('IBMPlexSans-Light', '' , './static/fonts/IBMPlexSans-Light.ttf', uni=True)
    pdf.set_font("IBMPlexSans", size=18)
    pdf.cell(170, 15, txt="Datasheet for dataset: {}".format(name[10:]), ln=1, align="L")
    pdf.set_draw_color(224, 238, 255)
    pdf.set_fill_color(241, 248, 255)
    pdf.set_font('IBMPlexSans-Light', size=8)
    pdf.multi_cell(170, 5, txt="A datasheet is a standardized document used in order to provide information about the provenance, creation, and usage of a particular dataset. They serve to increase transparancy and to make it easier for new users of the dataset to avoid unwanted biases. You can read more about Datasheets for Datasets at: https://arxiv.org/abs/1803.09010", 
    border=1, align="L", fill=True)
    for question, answer in qa.items():
        pdf.cell(170, 3, ln=1)
        pdf.set_font("IBMPlexSans", size=8)
        pdf.multi_cell(170, 5, txt=question, align="L")
        pdf.set_draw_color(226, 229, 233)
        pdf.set_fill_color(243, 243, 243)
        pdf.set_font("IBMPlexSans-Light", size=8)
        if len(answer) > 0:
            pdf.multi_cell(170, 5, txt=answer, border=1, align="L", fill=True)
        else:
            pdf.multi_cell(170, 5, txt="No answer provided.", border=1, align="L", fill=True)
    return pdf
    
    
    
    