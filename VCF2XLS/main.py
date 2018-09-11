import os
import csv
import quopri

VCFDICT = {
    'begin': 'BEGIN:VCARD',
    'end': 'END:VCARD',
    'name_q': 'N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE',
    'fname_q': 'FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE',
    'isfav': 'ISFAVORITE',
    'tel': 'TEL;CELL',
    'tel_w': 'TEL;WORK',
    'email': 'EMAIL;HOME',
    'version': 'VERSION',
    'name': 'N',
    'fname': 'FN'
}


def vcf2csv(filename):
    plist = []
    vcf = os.path.splitext(filename)
    if vcf[1] != '.vcf':
        return False
    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline().strip()
            # print(line)
            if not line:
                print('读取结束')
                break
            if line == VCFDICT['begin']:
                pinfo = {}
            elif line == VCFDICT['end']:
                plist.append(pinfo)
            else:
                [k, v] = line.split(':')
                pinfo[k] = v
    write2csv(vcf[0], plist)
    return True


def csv2vcf(filename):
    plist = []
    csv = os.path.splitext(filename)
    if csv[1] != '.csv':
        return False
    with open(filename, 'r') as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            pinfo = line.split(',')
            if len(pinfo) >= 2:
                plist.append(pinfo)
            else:
                continue
    write2vcf(csv[0], plist)
    print(len(plist))
    return True


def write2vcf(filename, plist):
    with open(filename + '.vcf', 'w') as f:
        for pinfo in plist:
            f.write(VCFDICT['begin'] + '\n')
            f.write(VCFDICT['version'] + ':2.1\n')
            f.write(VCFDICT['name_q'] + ':;' + str2quopri(pinfo[0]) + ';;;\n')
            f.write(VCFDICT['fname_q'] + ':' + str2quopri(pinfo[0]) + '\n')
            f.write(VCFDICT['isfav'] + ':0\n')
            f.write(VCFDICT['tel'] + ':' + pinfo[1] + '\n')
            f.write(VCFDICT['end'] + '\n')


def write2csv(filename, plist):
    with open(filename + '.csv', 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        for p in plist:
            if VCFDICT['fname'] in p.keys():
                name = p[VCFDICT['fname']]
            elif VCFDICT['fname_q'] in p.keys():
                name = quopri2str(p[VCFDICT['fname_q']])
            if VCFDICT['tel'] in p.keys():
                tel = p[VCFDICT['tel']]
            else:
                tel = ''
            if VCFDICT['tel_w'] in p.keys():
                tel_w = p[VCFDICT['tel_w']]
            else:
                tel_w = ''
            writer.writerow([name.encode('gbk', errors='ignore').decode('gbk'), tel, tel_w])
    return True


def quopri2str(quo):
    return quopri.decodestring(quo).decode('utf-8')


def str2quopri(str):
    return quopri.encodestring(str.encode('utf-8')).decode('utf-8')


if __name__ == '__main__':
    pass

    # 功能1
    # csv转换为vcf
    # csv中第一列为姓名，第二列为电话
    # csv2vcf('gen_2100.csv')

    # 功能2
    # vcf转换为csv
    # csv2vcf('gen_2100.csv')
