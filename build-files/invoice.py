#!/usr/bin/python3.6

#Part of: alpha-build-v0.1
#Author: Vignesh Burugina

import os
from io import BytesIO
import PyPDF2
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, NumberObject
from sys import argv
from num2words import num2words
from datetime import datetime
import pickle as pk
import webbrowser

def gen(a,b):
    """Fills template form and generates invoice"""
    
    def set_need_appearances_writer(writer):
        try:
            catalog = writer._root_object
            if "/AcroForm" not in catalog:
                writer._root_object.update({
                    NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

            need_appearances = NameObject("/NeedAppearances")
            writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
            
        except Exception as e:
            print('set_need_appearances_writer() catch : ', repr(e))

        return writer
    
    outfile = f'{home}/Documents/Invoices/{b}.pdf' 
    input_stream = open(template, "rb")
    pdf_reader = PyPDF2.PdfFileReader(input_stream, strict=False)
    if "/AcroForm" in pdf_reader.trailer["/Root"]:
        pdf_reader.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})
    pdf_writer = PyPDF2.PdfFileWriter()
    set_need_appearances_writer(pdf_writer)
    if "/AcroForm" in pdf_writer._root_object:
        pdf_writer._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})
    data_dict = a
    pdf_writer.addPage(pdf_reader.getPage(0))
    page = pdf_writer.getPage(0)
    pdf_writer.updatePageFormFieldValues(page, data_dict)
    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].getObject()
        for field in data_dict:
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject("/Ff"): NumberObject(1)
                })
    output_stream = BytesIO()
    pdf_writer.write(output_stream)
    input_stream.close()
    with open(outfile,'wb') as fl:
        fl.write(output_stream.getvalue())
 

def calc():
    global data_dict
    total = 0
    for i in range(1,6):
        val = data_dict[f'amount{i}']
        if val != "":
            total += float(val)
    return f'{float(total):.2f}'


def get_words(num_str):
    n = f'{float(num_str):.2f}'
    return num2words(float(n))

def getdate():
    date = datetime.now()
    return str(date.strftime("%x"))

def getbillno():
    try:
        with open(f'{home}/.alphacount','rb') as fl:
            c = pk.load(fl)
    except FileNotFoundError:
        print('Counter Not Found, Creating New Counter')
        c = 1
        with open(f'{home}/.alphacount','wb') as fl:
            pk.dump(c,fl)
    date = datetime.now()
    res = str(date.strftime("%b")).upper() + str(c)
    c += 1
    with open(f'{home}/.alphacount','wb') as fl:
        pk.dump(c, fl)
    return res

home = os.environ['HOME']
template = f'{home}/Templates/Invoice.pdf'
mainl = []
data_dict = {}
_slcount = 0

if argv[1] in ['help','HELP']:
    webbrowser.open('https://github.com/VigneshBurugina/Alpha-v0.1',2)

if len(argv) == 1:
    for i in range(6):
        msg = f'Enter Item {i}:'
        if i == 0:
            msg = 'Enter Customer Data:'
            pass
        mainl.append(input(msg))
else:
    with open(argv[1]) as fl:
        data = fl.readlines()
    for i in data:
        mainl.append(i.rstrip('\n'))
    
for i in range(7):
    if i == 0:
        data_dict['name'],data_dict['address'],data_dict['city'],data_dict['pin'],data_dict['state'],data_dict['regno'] = mainl[i].split(',')
    elif i < len(mainl):
        data_dict[f'sl{i}'] = str(_slcount)
        data_dict[f'desc{i}'],data_dict[f'hsn{i}'],data_dict[f'qty{i}'],data_dict[f'rate{i}'] = mainl[i].split(',')
        if data_dict[f'rate{i}'] != "" and data_dict[f'qty{i}'] != "":
            data_dict[f'amount{i}'] = f"{float(data_dict[f'qty{i}'])*float(data_dict[f'rate{i}']):.2f}"
        elif data_dict[f'rate{i}'] == "" and data_dict[f'qty{i}'] == "":
            data_dict[f'amount{i}'] = ""
            data_dict[f'sl{i}'] = ""
            _slcount += 1
    else:
        data_dict[f'sl{i}'],data_dict[f'desc{i}'],data_dict[f'hsn{i}'],data_dict[f'qty{i}'],data_dict[f'rate{i}'],data_dict[f'amount{i}'] = ",,,,,".split(',')

data_dict['total_amount'] = calc()
data_dict['total_amount_words'] = get_words(data_dict['total_amount'])
data_dict['date'] = getdate()
data_dict['billno'] = getbillno()
for i in range(1,7):
    if data_dict[f'amount{i}'] != "":
        data_dict[f'amount{i}'] = "Rs. " + data_dict[f'amount{i}']
    if data_dict[f'rate{i}'] != "":
        data_dict[f'rate{i}'] = "Rs. " + data_dict[f'rate{i}']
data_dict['total_amount'] = 'Rs. ' + data_dict['total_amount']
data_dict['total_amount_words'] = 'Rupees ' + data_dict['total_amount_words'].title()
gen(data_dict,data_dict['name'])
print('Invoice generated for:', f'Name: {data_dict["name"]}', f'Reg No. : {data_dict["regno"]}',sep='\n')
