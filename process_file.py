import re

def takeClosest(num,collection):
    temp_collection = [x for x in collection if x < num]
    closest = min(temp_collection,key=lambda x:abs(x-num))
    collection.remove(closest)
    return closest

def extract_1a_text(file_read_cleaner):
    # This whiffs, if it is correct in the beginning but wrong later.
    # "Item 1a." in table of contents but then
    # "Item 1 a." when it matters.
    # see 20210115_10-K_edgar_data_1582249_0001213900-21-002479.txt
    string = 'item 1 a'.lower()
    risk_ends = [m.end() for m in re.finditer(string, file_read_cleaner)]
    
    if risk_ends == []:
        string = 'item 1a'.lower()
        risk_ends = [m.end() for m in re.finditer(string, file_read_cleaner)]
        
    if risk_ends == []:
        string = '1a'.lower()
        risk_ends = [m.end() for m in re.finditer(string, file_read_cleaner)]
    
    string = 'item 1b'.lower()
    next_section_starts = [m.start() for m in re.finditer(string, file_read_cleaner)]
    
    if next_section_starts == []:
        # The occasional spelling error - catching an edge case.
        string = '1b.'.lower()
        next_section_starts = [m.start() for m in re.finditer(string, file_read_cleaner)]
            
    if next_section_starts == []:
        string = 'item 2'.lower()
        next_section_starts = [m.start() for m in re.finditer(string, file_read_cleaner)]
        
    coords = []
    for end_coord in next_section_starts:
        closest = takeClosest(end_coord, risk_ends)
        coords.append([closest,end_coord])
        
    skipped_sections = 0
    section_list = ""
    for coord_pair in coords:
        section = file_read_cleaner[coord_pair[0]:coord_pair[1]]
        if len(section) > 40:
            section_list += section
        else:
            skipped_sections += 1
            # function to track this goes here
            
    if section_list == "":
        section_list = None
    
    return section_list, skipped_sections

def return_tracker(file):
    file_read = open(file,"r").read()
    file_read_cleaner = file_read.replace('\n',' ').replace('\t', ' ').lower()
    
    try:
        string = 'conformed submission type:'
        doc_type_start = [m.end() for m in re.finditer(string, file_read_cleaner)][0]
    
        string = 'public document count:'
        doc_type_end = [m.start() for m in re.finditer(string, file_read_cleaner)][0]-1
        ten_k = 'k' in file_read_cleaner[doc_type_start:doc_type_end]
    except IndexError:
        print('Beginning string not found.')
        tek_k = False
        # This could cause some files to be skipped.

    
    if ten_k:
        try:
            # filing_date
            string = 'FILED AS OF DATE:'.lower()
            filed_date_start = [m.end() for m in re.finditer(string, file_read_cleaner)][0]
            string = 'DATE AS OF CHANGE:'.lower()
            filed_date_end = [m.start() for m in re.finditer(string, file_read_cleaner)][0]-1
            filed_date = file_read_cleaner[filed_date_start:filed_date_end]
        except:
            filed_date = None
        
        try:
            # company name
            string = 'COMPANY CONFORMED NAME:'.lower()
            name_start = [m.end() for m in re.finditer(string, file_read_cleaner)][0]
            string = 'CENTRAL INDEX KEY:'.lower()
            name_end = [m.start() for m in re.finditer(string, file_read_cleaner)][0]-1
            company_name = file_read_cleaner[name_start:name_end]
        except:
            company_name = None
        
        try:
            # central index key
            string = 'CENTRAL INDEX KEY:'.lower()
            key_start = [m.end() for m in re.finditer(string, file_read_cleaner)][0]
            string = 'STANDARD INDUSTRIAL CLASSIFICATION:'.lower()
            key_end = [m.start() for m in re.finditer(string, file_read_cleaner)][0]-1
            central_index_key = file_read_cleaner[key_start:key_end]
        except:
            central_index_key = None
            
        # fiscal year end
        try:
            string = 'FISCAL YEAR END:'.lower()
            key_start = [m.end() for m in re.finditer(string, file_read_cleaner)][0]
            string = 'FILING VALUES:'.lower()
            key_end = [m.start() for m in re.finditer(string, file_read_cleaner)][0]-1
            fiscal_year_end = file_read_cleaner[key_start:key_end]
        except:
            fiscal_year_end = None
    
        # sections
        try:
            section_list, skipped_sections = extract_1a_text(file_read_cleaner)
        except:
            section_list, skipped_sections = None, None
        
        tracker = {'filename':file,
                   'type':'10-K',
                         'filed_date':filed_date,
                         'company_name':company_name,
                         'central_index_key': central_index_key,
                         'fiscal_year_end': fiscal_year_end,
                         'section_list': section_list,
                         'skipped_sections':skipped_sections}
        return tracker
    else:
        tracker = {'filename':file,
                   'type':'Other',
                         'filed_date':None,
                         'company_name':None,
                         'central_index_key': None,
                         'fiscal_year_end': None,
                         'section_list': None,
                         'skipped_sections':None}
        return tracker
        