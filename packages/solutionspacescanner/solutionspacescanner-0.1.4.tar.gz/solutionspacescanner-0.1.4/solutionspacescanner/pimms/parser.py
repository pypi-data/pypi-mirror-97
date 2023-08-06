





def keyfile_parser(filename):

    return_dict = {}

    with open(filename) as fh:
        content = fh.readlines(filename)

    for line in content:
        sline = line.strip()

        # skip comments
        if sline[0] == "#":
            continue

        line_data = [x.strip() for x in sline.split('#')[0].strip().split(':')]

        if line_data[0] == 'CHAIN':
            return_dict['CHAIN'] = line_data[1:]
        else:
            try:
                return_dict[line_data[0]] = line_data[1]
            except IndexError:
                print('Skipping line %s' %(line))

    return return_dict


def parameter_filer_parser(filename):
    return_dict = {}

    with open(filename) as fh:
        content = fh.readlines(filename)


    for line in content:
        sline = line.strip()

        # skip comments
        if sline[0] == "#":
            continue

        line_data = [x.strip() for x in sline.split('#')[0].strip().split()]

        # for now skip angle penalties
        if line_data[0] == 'ANGLE_PENALTY':
            continue
        
        r1 = line_data[0]
        r2 = line_data[1]

        SR = int(line_data[2])
        LR = None
        SLR = None

        if len(line_data) == 4:
            LR = int(line_data[3])
        elif if len(line_data) == 5:
            LR = int(line_data[3])
            SLR = int(line_data[4])
        else:
            raise Exception('Gosh darn it this aint right!')

        if r1  not in return_dict:
            return_dict[r1] = {}

        if r2 not in return_dict:
            return_dict[r2] = {}

        return_dict[r1][r2] = [SR, LR, SLR]
        return_dict[r2][r1] = [SR, LR, SLR]

    return return_dict
        
        
            

    

    
                
            
        
            
