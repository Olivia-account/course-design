import re

# 解析INI配置文件
def parse_ini_file(file_path):
    ini_config = {}  # 初始化配置字典
    with open(file_path, 'r') as file:
        current_section = None
        for line in file:
            line = line.strip()  # 去除行首尾的空白字符
            if line.startswith('[') and line.endswith(']'):  # [Sequences]
                current_section = line[1:-1]  # 解析当前节的名称，Sequences
                ini_config[current_section] = {}  # 在配置字典中创建当前节的空字典
            elif '=' in line:  # FrontSequence = AGCTAGGCTTAATCG
                key, value = line.split('=', 1)  # 解析键值对
                ini_config[current_section][key.strip()] = value.strip()  # 去除行首尾的空白字符,将键值对存储在当前节的字典中
    return ini_config


def front_fuzzy_match(pattern, sequence):
    patternCopy = pattern
    pattern = list(pattern)
    sequence = list(sequence)
    len_pattern = len(pattern)
    len_sequence = len(sequence)
    if len_pattern > len_sequence + 1:
        return [-1, '-1', '未匹配成功', len_pattern]
    if pattern == sequence[:len_pattern]:
        return [''.join(pattern), '0', '无突变', len_pattern]
    # 判断是否为替换
    count = 0
    pos = -1
    c = ''
    for i in range(len_pattern):
        if pattern[i] != sequence[i]:
            count += 1
            pos = i
            c = sequence[i]
            if count >= 2:
                break
    if count <= 1:
        return [''.join(sequence[:len_pattern]),  '='+str(pos)+c, f'替换了索引{pos}的位置为{c}', len_pattern]
    
    else:  
        # 判断是否缺失
        pos = -1
        count = 0
        c = ''
        for i in range(len_pattern-1):
            if pattern[i] != sequence[i]:
                count += 1
                if count >= 2:
                    break
                pos = i
                c = pattern[i]
                del pattern[i]
        if count <= 1:
            return [''.join(sequence[:len_pattern]),  '-'+str(pos)+c, f'缺失了索引{pos}的位置，缺失了{c}', len_pattern-1]
        else: # 判断是否新增
            pattern = patternCopy
            pos = -1
            count = 0
            c = ''
            for i in range(len_pattern):
                if pattern[i] != sequence[i]:
                    
                    count += 1
                    if count >= 2:
                        break
                    pos = i
                    c = sequence[i]
                    del sequence[i]
            if count <= 1:
                return [''.join(sequence[:len_pattern+1]), '+'+str(pos)+c, f'新增了索引{pos}的位置，新增了{c}', len_pattern+1]
    return [-1, '-1', '未匹配成功', len_pattern]
def back_fuzzy_match(pattern, sequence):
    patternCopy = pattern
    sequenceCopy = sequence
    pattern = list(pattern)
    sequence = list(sequence)
    len_pattern = len(pattern)
    len_sequence = len(sequence)
    if len_pattern > len_sequence + 1:
        return [-1, '-1', '未匹配成功', len_pattern]
    if pattern == sequence[-len_pattern:]:
        return [''.join(pattern), '0', '无突变', len_pattern]
    # 判断是否为替换
    count = 0
    pos = -1
    c = ''
    for i in range(len_pattern):
        if pattern[i] != sequence[len_sequence - len_pattern + i]:
            count += 1
            pos = i
            c = sequence[len_sequence - len_pattern + i]
            if count >= 2:
                break
    if count <= 1:
        return [''.join(sequence[-len_pattern:]),  '='+str(pos)+c, f'替换了索引{pos}的位置为{c}', len_pattern]
    
    else:  
        # 判断是否缺失
        pos = -1
        count = 0
        c = ''
        for i in range(len_pattern-1):
            if pattern[i] != sequence[len_sequence - len_pattern + i + 1]:
                count += 1
                if count >= 2:
                    break
                pos = i
                c = pattern[i]
                del pattern[i]
        if count <= 1:
            if pos == -1:
                c = pattern[-1]
                return [''.join(sequence[-len_pattern+1:]),  '-'+str(len_pattern-1)+c, f'缺失了索引{len_pattern-1}的位置，缺失了{c}', len_pattern-1]
            print(pos, i, c, len_pattern, pattern)
            return [''.join(sequence[-len_pattern+1:]),  '-'+str(pos)+c, f'缺失了索引{pos}的位置，缺失了{c}', len_pattern-1]
        else: # 判断是否新增
            pattern = patternCopy
            pos = -1
            count = 0
            c = ''
            for i in range(len_pattern):
                if pattern[i] != sequence[len_sequence - len_pattern + i - 1]:
                    
                    count += 1
                    if count >= 2:
                        break
                    pos = i
                    c = sequence[len_sequence - len_pattern + i - 1]
                    del sequence[len_sequence - len_pattern + i - 1]
            if count <= 1:
                if pos == -1:
                    c = sequenceCopy[-1] # pos
                    return [''.join(sequenceCopy[-len_pattern-1:]), '+'+str(len_pattern)+c, f'新增了索引{len_pattern}的位置，新增了{c}', len_pattern+1]
                return [''.join(sequenceCopy[-len_pattern-1:]), '+'+str(pos)+c, f'新增了索引{pos}的位置，新增了{c}', len_pattern+1]
    return [-1, '-1', '未匹配成功', len_pattern]

def decode_core(patterns, sequence):
    for i in patterns:
        pattern = '('+i+')+'
        sequence = re.sub(pattern, lambda x: f"[{i}]{int(len(x.group())/len(i))}", sequence)
    return sequence


def decode_ini(file_path, sequence):
    ini_config = parse_ini_file(file_path)
    FrontSequence = ini_config['Sequences']['FrontSequence']
    BackSequence = ini_config['Sequences']['BackSequence']
    CoreUnit = ini_config['Sequences']['CoreUnit'].split(',')
    frontLi = front_fuzzy_match(FrontSequence, sequence)
    Front = sequence[:frontLi[3]]

    backLi = back_fuzzy_match(BackSequence, sequence)

    Back = sequence[len(sequence)-backLi[3]:]

    core_sequence = sequence[frontLi[3]:len(sequence)-backLi[3]]
    core = decode_core(CoreUnit, core_sequence)

    print("前侧翼序列：", Front, frontLi[1], frontLi[2])
    print("后侧翼序列：", Back, backLi[1], backLi[2])
    print("核心区：", core)

# AGCTAGGCTTAATCG ATCG ATCG ATCG ATCG ATCG ATCG ATCG TTGGAG ATCG ATCG ATCG ATCGTTGGAGTCA
print('测试')
print('\n正常：')
decode_ini('example.ini', 'AGCTAGGCTTAATCGATCGATVJCGATCGATCGATCGATCGATCGTTGGAGATCGATCGATCGATCGTTGGAGTCA')
print('\n替换：')
decode_ini('example.ini', 'ACCTAGGCTTAATCGATCGATCGATCGATCGATCGATCGATCGTTGGAGATCGATCGATCGATCGTTGGAGCCA')
print('\n缺少：')
decode_ini('example.ini', 'ACTAGGCTTAATCGATCGATCGATCGTAGGATCGATCGATCGATCGTTGGAGATCGATCGATCGATCGTTGGAGCA')
print('\n新增：')
decode_ini('example.ini', 'AGGCTAGGCTTAATCGATCGATCGATCGATCGATCGATCGATCGTTGGAGATCGATCGATCGATCGTTGGAGTTCA')
print('\n文件示例：')
# AAGCTAGGCTTAATCG ATCGATCGATCG ATCGTTGGAGTCA
decode_ini('example.ini', 'AAGCTAGGCTTAATCGATCGATCGATCGATCGTTGGAGTCA')
print('\n无法匹配：')
decode_ini('example.ini', 'CTTAATCGATCGATCGATCGTAGGATCGATCGATCGATCGTTGGAGATCGATCGATCGATCGTTGGAGCA')

print('\nTAGG示例：')
decode_ini('example.ini', 'ATCGATCGTAGGTAGGTAGGATCGATCGTAGGTAGGTAGGTAGGATCGATCG')










