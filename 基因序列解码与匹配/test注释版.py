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

    patternCopy = pattern  # 备份模式序列
    pattern = list(pattern)  # 将模式序列转换为列表
    sequence = list(sequence)  # 将待匹配序列转换为列表
    len_pattern = len(pattern)  # 模式序列长度
    len_sequence = len(sequence)  # 待匹配序列长度
    if len_pattern > len_sequence + 1:  # 如果模式序列长度大于待匹配序列长度加1，则匹配失败
        return [-1, '-1', '未匹配成功', len_pattern]
    if pattern == sequence[:len_pattern]:  # 如果模式序列与待匹配序列的前缀部分完全匹配
        return [''.join(pattern), '0', '无突变', len_pattern]
    # 判断是否为替换
    # abcd
    # abdd、abdc
    count = 0  # 记录替换操作的次数
    pos = -1  # 记录替换操作的位置
    c = ''  # 记录替换操作的字符
    for i in range(len_pattern):
        if pattern[i] != sequence[i]:  # 如果模式序列与待匹配序列在位置i上的字符不相等
            count += 1  # 替换操作次数加1
            pos = i  # 记录替换操作的位置为i
            c = sequence[i]  # 记录替换操作的字符为待匹配序列在位置i上的字符
            if count >= 2:  # 如果替换操作次数超过2次，则不符合替换条件，直接退出循环
                break
    if count <= 1:  # 如果替换操作次数小于等于1次
        return [''.join(sequence[:len_pattern]),  '='+str(pos)+c, f'替换了索引{pos}的位置为{c}', len_pattern]
        # 返回匹配成功的序列、替换操作的描述信息和长度
    else:
        # 判断是否缺失
            # abcd
            # abd、abe
        pos = -1  # 记录缺失操作的位置
        count = 0  # 记录缺失操作的次数
        c = ''  # 记录缺失操作的字符
        for i in range(len_pattern-1):
            if pattern[i] != sequence[i]:  # 如果模式序列与待匹配序列在位置i上的字符不相等
                count += 1  # 缺失操作次数加1
                if count >= 2:  # 如果缺失操作次数超过2次，则不符合缺失条件，直接退出循环
                    break
                pos = i  # 记录缺失操作的位置为i
                c = pattern[i]  # 记录缺失操作的字符为模式序列在位置i上的字符
                del pattern[i]  # 在模式序列中删除位置i上的字符
        if count <= 1:  # 如果缺失操作次数小于等于1次
            return [''.join(sequence[:len_pattern]),  '-'+str(pos)+c, f'缺失了索引{pos}的位置，缺失了{c}', len_pattern-1]
            # 返回匹配成功的序列、缺失操作的描述信息和长度
        else:
            # 判断是否新增
                # abcd
                # abcd、abcc
            pattern = patternCopy  # 恢复模式序列为初始状态
            pos = -1  # 记录新增操作的位置
            count = 0  # 记录新增操作的次数
            c = ''  # 记录新增操作的字符
            for i in range(len_pattern):
                if pattern[i] != sequence[i]:  # 如果模式序列与待匹配序列在位置i上的字符不相等
                    count += 1  # 新增操作次数加1
                    if count >= 2:  # 如果新增操作次数超过2次，则不符合新增条件，直接退出循环
                        break
                    pos = i  # 记录新增操作的位置为i
                    c = sequence[i]  # 记录新增操作的字符为待匹配序列在位置i上的字符
                    del sequence[i]  # 在待匹配序列中删除位置i上的字符
            if count <= 1:  # 如果新增操作次数小于等于1次
                return [''.join(sequence[:len_pattern+1]), '+'+str(pos)+c, f'新增了索引{pos}的位置，新增了{c}', len_pattern+1]
                # 返回匹配成功的序列、新增操作的描述信息和长度
    return [-1, '-1', '前侧翼序列未匹配成功', len_pattern]  # 如果以上情况都不符合，则匹配失败

def back_fuzzy_match(pattern, sequence):
    patternCopy = pattern  # 备份模式序列
    sequenceCopy = sequence  # 备份待匹配序列
    pattern = list(pattern)  # 将模式序列转换为列表
    sequence = list(sequence)  # 将待匹配序列转换为列表
    len_pattern = len(pattern)  # 模式序列长度
    len_sequence = len(sequence)  # 待匹配序列长度
    if len_pattern > len_sequence + 1:  # 如果模式序列长度大于待匹配序列长度加1，则匹配失败
        return [-1, '-1', '未匹配成功', len_pattern]
    if pattern == sequence[-len_pattern:]:  # 如果模式序列与待匹配序列的后缀部分完全匹配
        return [''.join(pattern), '0', '无突变', len_pattern]
    # 判断是否为替换
    # abcd
    # abdd、abdc
    count = 0  # 记录替换操作的次数
    pos = -1  # 记录替换操作的位置
    c = ''  # 记录替换操作的字符
    for i in range(len_pattern):
        if pattern[i] != sequence[len_sequence - len_pattern + i]:  # 如果模式序列与待匹配序列在位置i上的字符不相等
            count += 1  # 替换操作次数加1
            pos = i  # 记录替换操作的位置为i
            c = sequence[len_sequence - len_pattern + i]  # 记录替换操作的字符为待匹配序列在位置[len_sequence - len_pattern + i]上的字符
            if count >= 2:  # 如果替换操作次数超过2次，则不符合替换条件，直接退出循环
                break
    if count <= 1:  # 如果替换操作次数小于等于1次
        return [''.join(sequence[-len_pattern:]),  '='+str(pos)+c, f'替换了索引{pos}的位置为{c}', len_pattern]
        # 返回匹配成功的序列、替换操作的描述信息和长度
    else:
        # 判断是否缺失
        # abcd
        # cdsrvvabd、fescsdaec
        pos = -1  # 记录缺失操作的位置
        count = 0  # 记录缺失操作的次数
        c = ''  # 记录缺失操作的字符
        for i in range(len_pattern-1):
            if pattern[i] != sequence[len_sequence - len_pattern + i + 1]:  # 如果模式序列与待匹配序列在位置[len_sequence - len_pattern + i + 1]上的字符不相等
                count += 1  # 缺失操作次数加1
                if count >= 2:  # 如果缺失操作次数超过2次，则不符合缺失条件，直接退出循环
                    break
                pos = i  # 记录缺失操作的位置为i
                c = pattern[i]  # 记录缺失操作的字符为模式序列在位置i上的字符
                del pattern[i]  # 在模式序列中删除位置i上的字符
        if count <= 1:  # 如果缺失操作次数小于等于1次
            if pos == -1:
                c = pattern[-1]
                return [''.join(sequence[-len_pattern+1:]),  '-'+str(len_pattern-1)+c, f'缺失了索引{len_pattern-1}的位置，缺失了{c}', len_pattern-1]
            # print(pos, i, c, len_pattern, pattern)
            return [''.join(sequence[-len_pattern+1:]),  '-'+str(pos)+c, f'缺失了索引{pos}的位置，缺失了{c}', len_pattern-1]
            # 返回匹配成功的序列、缺失操作的描述信息和长度
        else:  # 判断是否新增
            pattern = patternCopy  # 恢复模式序列为初始状态
            pos = -1  # 记录新增操作的位置
            count = 0  # 记录新增操作的次数
            c = ''  # 记录新增操作的字符
            for i in range(len_pattern):
                if pattern[i] != sequence[len_sequence - len_pattern + i - 1]:  # 如果模式序列与待匹配序列在位置[len_sequence - len_pattern + i - 1]上的字符不相等
                    count += 1  # 新增操作次数加1
                    if count >= 2:  # 如果新增操作次数超过2次，则不符合新增条件，直接退出循环
                        break
                    pos = i  # 记录新增操作的位置为i
                    c = sequence[len_sequence - len_pattern + i - 1]  # 记录新增操作的字符为待匹配序列在位置[len_sequence - len_pattern + i - 1]上的字符
                    del sequence[len_sequence - len_pattern + i - 1]  # 在待匹配序列中删除位置[len_sequence - len_pattern + i - 1]上的字符
            if count <= 1:  # 如果新增操作次数小于等于1次
                if pos == -1:
                    c = sequenceCopy[-1] # pos
                    return [''.join(sequenceCopy[-len_pattern-1:]), '+'+str(len_pattern)+c, f'新增了索引{len_pattern}的位置，新增了{c}', len_pattern+1]
                return [''.join(sequenceCopy[-len_pattern-1:]), '+'+str(pos)+c, f'新增了索引{pos}的位置，新增了{c}', len_pattern+1]
                # 返回匹配成功的序列、新增操作的描述信息和长度
    return [-1, '-1', '后侧翼序列未匹配成功', len_pattern]  # 如果以上情况都不符合，则匹配失败

import re

def decode_core(patterns, sequence):
    for i in patterns:
        pattern = '(' + i + ')+'
        # 使用sub函数替换匹配项为[ATCG]n形式
        # re.sub(pattern, replacement, string): 这是re模块中用于替换的函数。它接受三个参数：
        # pattern: 正则表达式，用于匹配需要替换的文本。
        # replacement: 替换的内容。在这里我们使用了一个lambda表达式来动态计算重复的次数，并拼接成形如[ATCG]n的格式。
        # string: 要搜索和替换的原始字符串。
        # '(ATCG)+': 这是正则表达式的模式，用于匹配连续出现的ATCG序列。+表示匹配前面的表达式（这里是ATCG）一次或多次，因此它会匹配一个或多个连续的ATCG字符串。
        # lambda x: f"[ATCG]{int(len(x.group())/4)}": 这是替换函数，使用lambda表达式定义。当re.sub找到匹配项后，它将调用这个函数来生成替换内容。这个函数的输入x是一个re.Match对象，表示找到的匹配项。
        # x.group(): 这是re.Match对象的方法，用于返回找到的匹配项。在这里，x.group()会返回匹配的连续ATCG序列。
        # len(x.group()): 这将计算匹配项的长度，也就是连续ATCG序列的字符个数。
        # int(len(x.group())/4): 这是计算重复的次数n。因为我们知道每个[ATCG]的长度是4，所以通过将匹配项长度除以4取整即可得到重复的次数。
        # f"[ATCG]{int(len(x.group())/4)}": 这将构建替换内容，使用f-string来将计算得到的重复次数n插入到"[ATCG]"中，形成形如[ATCG]n的格式。
        # 最终，re.sub函数将匹配到的连续ATCG序列替换为了[ATCG]n的形式
        # AGCTAGGCTTAATCGATCGATVJCGATCGATCGATCGATCGATCGTTGGAGATCGATCGATCGATCGTTGGAGTCA
        # ATCGATCGATCGATCG fgds[ATCG]3[ATCG]4AGTTAGTTfds
        sequence = re.sub(pattern, lambda x: f"[{i}]{int(len(x.group())/len(i))}", sequence)
        # 将目标序列中匹配到的模式替换为解码格式的字符串
        # 匹配到的模式使用方括号括起来，并在括号内注明模式本身以及出现的次数
    return sequence



def decode_ini(file_path, sequence):
    # 解析INI配置文件
    ini_config = parse_ini_file(file_path)
    # 获取前侧翼序列、后侧翼序列和核心区模式列表
    FrontSequence = ini_config['Sequences']['FrontSequence']
    BackSequence = ini_config['Sequences']['BackSequence']
    CoreUnit = ini_config['Sequences']['CoreUnit'].split(',')
    
    # 进行前侧翼序列模糊匹配
    # 举例：['AATAGG', '+2A', '新增了索引2的位置，新增了A', 6]
    frontLi = front_fuzzy_match(FrontSequence, sequence)
    Front = sequence[:frontLi[3]]  # 获取前侧翼序列的部分
    
    # 进行后侧翼序列模糊匹配
    # 举例：['CGATCGTTGGAGTACA', '+13A', '新增了索引13的位置，新增了A', 16]
    backLi = back_fuzzy_match(BackSequence, sequence)
    Back = sequence[len(sequence) - backLi[3]:]  # 获取后侧翼序列的部分
    
    # 提取核心区的序列
    core_sequence = sequence[frontLi[3]:len(sequence) - backLi[3]]
    # 对核心区进行解码
    core = decode_core(CoreUnit, core_sequence)
    
    # 打印解码结果
    print("前侧翼序列：", Front, frontLi[1], frontLi[2])
    print("后侧翼序列：", Back, backLi[1], backLi[2])
    print("核心区：", core)


# AGCTAGGCTTAATCG ATCG ATCG ATCG ATCG ATCG ATCG ATCG TTGGAG ATCG ATCG ATCG ATCGTTGGAGTCA
print('测试')
print('\n正常：')
decode_ini('example.ini', 'AGCTAGGCTTAATCG ATCGATVJCGATCGATCGATCGATCGATCGTTGGAGATCGATCGATCG ATCGTTGGAGTCA')
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










