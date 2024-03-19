import subprocess
import re
import codecs
import json

def decode_hex_utf_8_string(hex_string):
    if hex_string.startswith("0x"):
        hex_string = hex_string[2:]
    return codecs.decode(hex_string, 'hex').decode('utf-8')
    
def get_keyboard_layout():
    # Run the xkbcomp command to dump the current keyboard mapping to a file
    proc = subprocess.Popen(["xkbcomp", ":0", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    name_group1_match = re.search(r'name\[group1\]\s*=\s*"([^"]+)', stdout.decode("utf-8"))
    if name_group1_match:
        layout_name = name_group1_match.group(1)
        return layout_name
    else:
        return None

# Extract the keybaord layout to be set from the keyboardlayout settings file
keyboard_mappings = []

with open('boardlayouts.json', 'r') as file:
    data = json.loads(file.read())
    for mapping in data.values():
        keyboard_mappings.append({
            "model": mapping["model"],
            "layout": mapping["layout"],
            "variant": mapping["variant"]
        })

for mapping in keyboard_mappings:
    model = mapping["model"]
    layout = mapping["layout"]
    variant = mapping["variant"]
    subprocess.run(["setxkbmap", "-model", model, "-layout", layout, "-variant", variant])
    # Extract the value of the name[group1] property

    

# Initialize an 8x8 matrix with keycodes of the keyboard input 2
    keycode_index_matrix = [[19  , 20, 21, 22, 25, 26, 27, 28],
                            [256, 259, 262, 23, 24, 59, 269, 29],
                            [33, 48, 263, 36, 39, 40, 41, 42],
                            [257, 260, 264, 37, 38, 267, 30, 43],
                            [47, 34, 49, 50, 53, 54, 55, 46],
                            [258, 261, 265, 51, 52, 268, 270, 56],
                            [44, 35, 266, 9, 10, 16, 271, 15],
                            [5, 6, 7, 8, 11, 12, 13, 14]]

    keyboard_layout = get_keyboard_layout()

    # Get the actual key code values using xmodmap -pk
    proc = subprocess.Popen(["xmodmap", "-pk"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    keycodes = []

    keysyms_nomodifier_lc = []
    keysyms_shift_uc = []
    keysyms_algr_lc = []
    keysyms_altgr_shift_uc = []

    for line in stdout.decode("utf-8").strip().split("\n"):
        if line:
            parts = re.split(r"\s+", line.strip())
            
            #print("line ",i)
            #print("lenth line ",parts)
            #print("lenth line ",len(parts))

            if len(parts) > 14 and  len(parts) < 16:
                keysym_nomodifier_lc = parts[1]
                keysyms_nomodifier_lc.append(str(keysym_nomodifier_lc))
                keysym_shift_uc = parts[3]
                keysyms_shift_uc.append(str(keysym_shift_uc))
                keysym_algr_lc = parts[9]
                keysyms_algr_lc.append(str(keysym_algr_lc))
                keysym_altgr_shift_uc = parts[11]
                keysyms_altgr_shift_uc.append(str(keysym_altgr_shift_uc))
                keycode = parts[0]
                keycodes.append(str(keycode))

            elif len(parts) > 8 and len(parts) < 10:          
                keysym_nomodifier_lc = parts[1]
                keysyms_nomodifier_lc.append(str(keysym_nomodifier_lc))
                keysym_shift_uc = parts[3]
                keysyms_shift_uc.append(str(keysym_shift_uc))
                keysym_algr_lc = parts[5]
                keysyms_algr_lc.append(str(keysym_algr_lc))
                keysym_altgr_shift_uc = parts[7]
                keysyms_altgr_shift_uc.append(str(keysym_altgr_shift_uc))
                keycode = parts[0]
                keycodes.append(str(keycode))  

            else:  
                keysym_nomodifier_lc = "  "
                keysyms_nomodifier_lc.append(str(keysym_nomodifier_lc))
                keysym_shift_uc = "  "
                keysyms_shift_uc.append(str(keysym_shift_uc))
                keysym_algr_lc = "  "
                keysyms_algr_lc.append(str(keysym_algr_lc))
                keysym_altgr_shift_uc = " "
                keysyms_altgr_shift_uc.append(str(keysym_altgr_shift_uc))
                keycode = "  "
                keycodes.append(str(keycode))
        

    # Create a new matrix with the keysym names
    mod_types = ["no_modifier","shift","altgr","altgr_shift"]
    hex = ""

    new_matrix_nomod = [["" for _ in range(8)] for _ in range(8)]
    new_matrix_shift = [["" for _ in range(8)] for _ in range(8)]
    new_matrix_altgr = [["" for _ in range(8)] for _ in range(8)]
    new_matrix_altgrshift = [["" for _ in range(8)] for _ in range(8)]

    for modifier in mod_types:
    
                    
        if modifier == "no_modifier":
            for i, keycode in enumerate(keycode_index_matrix):
                for j, k in enumerate(keycode):
                        
                    # Get the actual keysym values for the keycode
                    if k == 44:
                        #print(keysyms_algr_lc[k])
                        try:
                            hex = keysyms_nomodifier_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            
                            hex = keysyms_nomodifier_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","
                            
                    
                    elif k == 43:
                        try:
                            hex = keysyms_nomodifier_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "\\"+hex
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_nomodifier_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","
                    
                    elif k == 46:
                        try:
                            hex = keysyms_nomodifier_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "\\"+hex
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_nomodifier_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","
                    elif k == 59:
                        hex = " "
                        hex = "'"+hex+"',"
                    
                    elif k == 14:
                        try:
                            hex = keysyms_nomodifier_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"'"
                        except Exception:
                            hex = keysyms_nomodifier_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex


                    elif k < 256:
                        try:
                            hex = keysyms_nomodifier_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_nomodifier_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","
                          

                    
                    new_matrix_nomod[i][j] = hex
            
        if modifier == "shift":
            for i, keycode in enumerate(keycode_index_matrix):
                for j, k in enumerate(keycode):
            
                    # Get the actual keysym values for the keycode
                    if k == 44:
                        try:
                            hex = keysyms_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:           
                            hex = keysyms_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","

                    elif k == 10:
                        try:
                            hex = keysyms_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","

                    elif k == 43:
                        try:
                            hex = keysyms_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","
                    
                    elif k == 46:
                        try:
                            hex = keysyms_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()             
                            hex = "0x"+hex+","

                    elif k == 59:
                        hex = " "
                        hex = "'"+hex+"',"
                    
                    elif k == 14:
                         try:
                            hex = keysyms_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"'"
                         except Exception:
                            hex = keysyms_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex
                    elif k < 256:
                        try:
                            hex = keysyms_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                            
                        except Exception:
                            hex = keysyms_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","

                    
                    new_matrix_shift[i][j] = hex
                
        if modifier == "altgr":
            for i, keycode in enumerate(keycode_index_matrix):
                for j, k in enumerate(keycode):
                
                    # Get the actual keysym values for the keycode
                    if k == 44:
                        try:
                            hex = keysyms_algr_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_algr_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","

                    elif k == 10:
                        try:
                            hex = keysyms_algr_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_algr_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","


                    elif k == 43:
                        try:
                            hex = keysyms_algr_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "\\"+hex
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_algr_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","
 

                    elif k == 46:
                        try:
                            hex = keysyms_algr_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_algr_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","


                    elif k == 59:
                        hex = " "
                        hex = "'"+hex+"',"
                    
                    elif k == 14:
                         try:
                            hex = keysyms_algr_lc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"'"
                         except Exception:
                            hex = keysyms_algr_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex
  

                    elif k < 256:
                        try:
                            hex = keysyms_algr_lc[k].replace("0x00", "").strip()                
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_algr_lc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","


                    
                    new_matrix_altgr[i][j] = hex

        if modifier == "altgr_shift": 
            for i, keycode in enumerate(keycode_index_matrix):
                for j, k in enumerate(keycode):

                    # Get the actual keysym values for the keycode
                    if k == 44:
                        try:
                            hex = keysyms_altgr_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_altgr_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","


                    elif k == 10:
                        try:
                            hex = keysyms_altgr_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_altgr_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","

                    elif k == 43:
                        try:
                            hex = keysyms_altgr_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "\\"+hex
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_altgr_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","
    
                    elif k == 46:
                        try:
                            hex = keysyms_altgr_shift_uc[k].replace("0x00", "").strip()                  
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_altgr_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","

                    elif k == 59:
                        hex = " "
                        hex = "'"+hex+"',"
                    
                    elif k == 14:
                         try:
                            hex = keysyms_altgr_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"'"
                         except Exception:
                            hex = keysyms_altgr_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex


                    elif k < 256:
                        try:
                            hex = keysyms_altgr_shift_uc[k].replace("0x00", "").strip()
                            hex = decode_hex_utf_8_string(hex)
                            hex = "'"+hex+"',"
                        except Exception:
                            hex = keysyms_altgr_shift_uc[k].replace("0x", "").strip()
                            if hex.startswith("100"):
                                hex = hex[3:]
                            elif hex.startswith("000x"):
                                hex = hex[4:]
                            elif hex.startswith("000x100"):
                                hex = hex[7:]
                            hex = hex.upper()
                            hex = "0x"+hex+","

                  
                    new_matrix_altgrshift[i][j] = hex    

        # Hardcoded ASCII keys that should not be overwritten   
        keycode_map = {
        256: ("ASCII_TAB,", "ASCII_TAB,", "ASCII_TAB,", "ASCII_TAB,"),
        257: ("ASCII_SEND,", "ASCII_SEND,", "ASCII_SEND,", "ASCII_SEND,"),
        258: ("ASCII_NEWL,", "ASCII_NEWL,", "ASCII_NEWL,", "ASCII_NEWL,"),
        259: ("ASCII_CAPS,", "ASCII_CAPS,", "ASCII_CAPS,", "ASCII_CAPS,"),
        260: ("0x00,", "0x00,", "0x00,", "0x00,"),
        261: ("ASCII_NEWR,", "ASCII_NEWR,", "ASCII_NEWR,", "ASCII_NEWR,"),
        262: ("ASCII_SHFL,", "ASCII_SHFL,", "ASCII_SHFL,", "ASCII_SHFL,"),
        263: ("ASCII_PGUP,", "ASCII_PGUP,", "ASCII_PGUP,", "ASCII_PGUP,"),
        264: ("ASCII_SHFR,", "ASCII_SHFR,", "ASCII_SHFR,", "ASCII_SHFR,"),
        265: ("0x00,", "0x00,", "0x00,", "0x00,"),
        266: ("ASCII_PGDN,", "ASCII_PGDN,", "ASCII_PGDN,", "ASCII_PGDN,"),
        268: ("ASCII_ALTG,", "ASCII_ALTG,", "ASCII_ALTG,", "ASCII_ALTG,"),
        269: ("ASCII_BKSP,", "ASCII_BKSP,", "ASCII_BKSP,", "ASCII_BKSP,"),
        270: ("ASCII_SPCL,", "ASCII_SPCL,", "ASCII_SPCL,", "ASCII_SPCL,"),
        271: ("ASCII_CR,", "ASCII_CR,", "ASCII_CR,", "ASCII_CR,"),
    }

    for i, keycode in enumerate(keycode_index_matrix):
        for j, k in enumerate(keycode):
            if k in keycode_map:
                new_matrix_nomod[i][j], new_matrix_shift[i][j], new_matrix_altgr[i][j], new_matrix_altgrshift[i][j] = keycode_map[k]


    ############################## Build the oput matrices for all 4 modifier types ##############################


    # Calculate the width of each column in the matrix
    column_width = max(len(str(keysym)) for row in new_matrix_nomod for keysym in row) + 1

    # Create a string with the matrix cells, separated by spaces
    matrix_string = ""
    for row in new_matrix_nomod:
        for cell in row:
            matrix_string += cell.rjust(column_width, " ") + " "
        matrix_string += "\n"
        
    # Create a string with the matrix cells, separated by spaces
    matrix_string = "const unsigned char keylookup[SWMAT_LAYOUTS][MODIFIER_LAYERS][ROWS*COLS] {\n"
    matrix_string += "\t {\n"
    matrix_string += "\t // " + keyboard_layout  + "\n"

    #First Matrix
    matrix_string += "\t\t // No Modifier (Lower case)\n"
    matrix_string += "\t\t {\n"
    

    for row in new_matrix_nomod:
       for i, cell in enumerate(row):
            if i == 0:
                matrix_string += "\t\t\t" + cell.ljust(column_width, " ") + " "
            else:
                matrix_string += "   " + cell.ljust(column_width, " ") + " "
       matrix_string += "\n"

    # Calculate the height of each row in the matrix
    row_height = 1

    # Add spacing between rows
    matrix_string_spaced = ""
    for i, row in enumerate(matrix_string.strip().split("\n")):
        matrix_string_spaced += row
        if i < len(matrix_string.strip().split()) - 1:
            matrix_string_spaced += "\t\t\t\t"
            matrix_string_spaced += "\n" * row_height

    #Second Matrix
    matrix_string += "\t\t }, \n\t\t // Shift (upper case)\n"
    matrix_string += "\t\t {\n"

    for row in new_matrix_shift:
        for i, cell in enumerate(row):
            if i == 0:
                matrix_string += "\t\t\t" + cell.ljust(column_width, " ") + " "
            else:
                matrix_string += "   " + cell.ljust(column_width, " ") + " "
        matrix_string += "\n"

    # Calculate the height of each row in the matrix
    row_height = 1

    # Add spacing between rows
    matrix_string_spaced = ""

    #Third Matrix
    matrix_string += "\t\t }, \n\t\t //AltGr (lower case) x, k, %\n"
    matrix_string += "\t\t {\n"

    for row in new_matrix_altgr:
        for i, cell in enumerate(row):
            if i == 0:
                matrix_string += "\t\t\t" + cell.ljust(column_width, " ") + " "
            else:
                matrix_string += "   " + cell.ljust(column_width, " ") + " "
        matrix_string += "\n"

    # Calculate the height of each row in the matrix
    row_height = 1

    # Add spacing between rows
    matrix_string_spaced = ""

    #Fourth Matrix
    matrix_string += "\t\t }, \n\t\t // Shift+AltGr (upper case) {, X, K \n"
    matrix_string += "\t\t {\n"

    for row in new_matrix_altgrshift:
        for i, cell in enumerate(row):
            if i == 0:
                matrix_string += "\t\t\t" + cell.ljust(column_width, " ") + " "
            else:
                matrix_string += "   " + cell.ljust(column_width, " ") + " "
        matrix_string += "\n"

    # Calculate the height of each row in the matrix
    row_height = 1

    # Add spacing between rows
    matrix_string_spaced = ""

    for i, row in enumerate(matrix_string.strip().split("\n")):
        matrix_string_spaced += row
        if i < len(matrix_string.strip().split()) - 1:
            matrix_string_spaced += "\t\t\t\t"
            matrix_string_spaced += "\n" * row_height
    matrix_string_spaced += "\t\t }, \n"
    matrix_string_spaced += "\t }, \n"
    matrix_string_spaced += "};"


    #Save the matrix to a text file
    with open("customkeyboardlayout_{}.txt".format(keyboard_layout), "w") as f:
        f.write(matrix_string_spaced)