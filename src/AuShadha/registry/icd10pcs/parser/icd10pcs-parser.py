#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==============================================================
        >>>>> Copy or link to XML before running! <<<<<
==============================================================

@desc: Parses ICD10-PCS XML and save JSON suitable for plug-in fixture
@author: dmoc

HISTORY:
    140524-0900:
        First version
    
NOTES:
    
"""

#======================================================================
# IMPORTS

from datetime import datetime
import xml.etree.cElementTree as ET
import pprint
import json

# ToDo: json.dumps() crashes when used with Python zip...
#from zipfile import ZipFile

#======================================================================
# CONSTANTS

JSON_PATH = "../fixtures/"
JSON_FILENAME = JSON_PATH + "initial_data.json"

AXIS_NAMES = (
    '<dummy>', 
    'Section', 
    'BodySystem', 
    'Operation', 
    'BodyPart', 
    'Approach', 
    'Device', 
    'Qualifier'
)

APP_PREFIX = "icd10pcs." # dot not underscore!

MDLAppCfg = APP_PREFIX + 'AppCfg'
MDLAppTxt = APP_PREFIX + 'AppTxt'

MDLCodePageRow = APP_PREFIX + 'CodePageRow'

MDLAxis = tuple(map((APP_PREFIX+'{0}').format, AXIS_NAMES))


#======================================================================
# GLOBALS

table_count = 0
axis_count = [0]*8 # First for MDLCodePage
data = []
unique_text = None


#======================================================================
# UTILITIES

def time_stamp(fmt='%Y%m%d-%H%M%S'):
    return datetime.now().strftime(fmt)

tid = lambda text: unique_text.index(text)+1 # 1-based Text ID (TID)


#======================================================================
# XML HELPERS

xtables = lambda root: root.iter('pcsTable')
xrows = lambda table: table.iter('pcsRow')
xaxes = lambda e, max_num: e.findall('axis')[:max_num]
xtitle = lambda e: e.text if e.tag == 'title' else e.find('title').text
xlabel = lambda e: e.text if e.tag == 'label' else e.find('label').text
xattrib = lambda e, attrib: e.attrib[attrib]
xtable_axes = lambda table: xaxes(table, 3)
xrow_axes = lambda row: xaxes(row, 4)
xaxis_labels = lambda axis: axis.findall("label")


def defn_txt(e):
    try:
        return e.find('definition').text
    except:
        return ''

axis_pos = lambda axis: int(xattrib(axis, "pos"))
title_fk = lambda e: tid(xtitle(e))
label_code = lambda e: xattrib(e, "code")
label_fk = lambda e: tid(xlabel(e))
defn_fk = lambda e: tid(defn_txt(e))

axis_label_code = lambda axis: label_code(xaxis_labels(axis)[0])

#def xlabel_fields(e): 
##    return xattrib(e, "code"), tid(xlabel(e))
#    return pcs_code(e), label_fk(e)

#xaxis_label = lambda axis: xaxis_labels(axis)[0]
#xlabel_code = lambda e: xattrib(e, "code")
#xlabel_title_fk = lambda e: tid(xlabel(e))


#======================================================================
# JSON FOR FIXTURES

def add_data(model, pk, fields):
    """Append a new data chunk."""
    data.append({
         'model': model,
            'pk': pk,
        'fields': fields
    })


#======================================================================
# TEXT HANDLING

def extract_pcs_text(root):
    """Title & Label text combined to remove redundancy"""
    global unique_text
    
    def get_unique(root, xpath, target=None):
        """Returns unique set"""
        uniq = target if target!=None else set()
        for e in root.iterfind(xpath):
            try:
                uniq.add(e.text)
            except:
                pass
        return uniq
    
    unique_text = get_unique(root, ".//title")
    get_unique(root, ".//label", target=unique_text)
    get_unique(root, ".//axis[@pos='3']/definition", target=unique_text)
    
    unique_text = list(unique_text)
    unique_text.sort()
    unique_text = [''] + unique_text
    
    for idx,txt in enumerate(unique_text):
        idx += 1 # 1-based indexing
        add_data(MDLAppTxt, idx, {'id': idx, 'txt': txt})
    
    print "\t- Unique text extracted: {}".format(len(unique_text))


#========================================================================
# MAIN FUNCTIONS

def parse_xml(root):
    global table_count
    
    extract_pcs_text(root)
    
    for table_count, table in enumerate(xtables(root)):
        table_count += 1
        
        axes = xtable_axes(table)
        
        # Axis 1..3, codepage is concatenated to previous axis...
        # (assumes axes in "pos" order)
        codepage = ''.join(axis_label_code(a) for a in axes)
        
        for axis in xtable_axes(table):
            #======================================= Axis fields
            pos = axis_pos(axis)
            axis_count[pos] += 1
            idx = axis_count[pos]
            
            fields = {
                       'id': idx, 
                 'codepage': codepage, 
                     'code': axis_label_code(axis), 
                 'label_fk': label_fk(axis), 
                 'title_fk': title_fk(axis), 
            }
            if pos == 3:
                fields['defn_fk'] = defn_fk(axis)
            add_data(MDLAxis[pos], idx, fields)
            
        for row_num, row in enumerate(xrows(table)):
            row_num += 1 # Want 1-based (sqlite leftover?)
            
            axis_count[0] += 1
            codepage_row_id = '{}-{}'.format(codepage, row_num)
            add_data(MDLCodePageRow, codepage_row_id, {
                      'id': codepage_row_id, 
                'codepage': codepage, 
                 'row_num': row_num, 
            })
            
            for axis in xrow_axes(row):
                pos = axis_pos(axis)
                axis_count[pos] += 1
                idx = axis_count[pos]
                model = MDLAxis[pos]
                axis_title_fk = title_fk(axis)
                
                for label in xaxis_labels(axis):
                    axis_count[pos] += 1
                    idx = axis_count[pos]
                    add_data(model, idx, {
                               'id': idx, 
                           'row_id': codepage_row_id, 
                         'codepage': codepage, 
                          'row_num': row_num, 
                              'pos': pos, 
                         'title_fk': axis_title_fk, 
                             'code': label_code(label), 
                         'label_fk': label_fk(label), 
                    })
                    

def set_cfg(cfg_key, cfg_value):
    # "static" var...
    if not hasattr(set_cfg, "idx"):
        set_cfg.idx = 0
    set_cfg.idx += 1
    
    add_data(MDLAppCfg, set_cfg.idx, {
               'id': set_cfg.idx,
          'cfg_key': "build-date",
        'cfg_value': time_stamp(),
    })

    
def main():
    try:
        tree = ET.parse("icd10pcs_tabular_2014.xml")
    except IOError:
        print "Error - Not found: icd10pcs_tabular_2014.xml"
        return
    
    
    print "Parsing:"
    
    parse_xml(tree.getroot())
    set_cfg("build-date", time_stamp())
    with file(JSON_FILENAME,'w') as f:
        f.write(json.dumps(data, indent=4))
    
    # Was going to zip but ran into errors...
#    with ZipFile(JSON_FILENAME+'.zip', 'w') as f:
##        f.write(json.dumps(data, indent=4))
#        json.dump(data, f, indent=4)
#    print "Created zipped JSON fixture."
    
    print "\t- Code Pages: {}".format(table_count)
    print "\t- CodePage Rows: {}".format(axis_count[0])
    print "\tAxis Counts:"
    for pos in range(1,8):
        print "\t\t{}: {}".format(AXIS_NAMES[pos], axis_count[pos])
    
    print "\t- Created JSON fixture (now zip it!)."
    
#======================================================================
if __name__ == "__main__":
    # >>>>> Copy or link to XML before running! <<<<<
    main()
    print "\tDone."

