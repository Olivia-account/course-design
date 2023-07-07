function game2048()
% 游戏主函数

% 创建figure窗口
h = figure('Name', '2048',... % 窗口名称
    'NumberTitle', 'off',... % 不显示标题序号
    'Menubar', 'none',... % 不显示菜单栏
    'Position', [450 200 400 440],... % 窗口位置和大小
    'KeyPressFcn', @keyevent); % 键盘按键事件回调函数

% 创建4x4的按钮格子
for m = 1:4
    for n = 1:4
        uicontrol('Style', 'pushbutton',... % 按钮风格
            'String', '',... % 显示内容为空
            'FontSize', 20,... % 字体大小
            'Position', [(m-1)*80+40 (n-1)*80+40 80 80]); % 按钮位置和大小
    end
end
hb = findall(gcf, 'Style', 'pushbutton'); % 获取所有按钮句柄
pbcolor = get(hb(1), 'BackgroundColor'); % 获取按钮的背景色
numcolor = [0.11 0.23 0.57]; % 数字方块的颜色

% 创建分数文本
hscoretext = uicontrol('Style', 'text',... % 文本风格
    'BackgroundColor', get(h, 'Color'),... % 背景色与窗口相同
    'String', '0',... % 初始分数为0
    'FontSize', 20,... % 字体大小
    'Position', [100 385 200 30]); % 文本位置和大小

% 初始化游戏
[mymatrix, score] = gameini();

%% 初始化游戏
% 游戏初始化函数，设置按钮为空，背景色为初始颜色
% 初始化矩阵为全零矩阵
% 第一个随机位置为2
function [mymatrix, score] = gameini()
    set(hb, 'String', '') % 将所有按钮的显示内容设置为空
    set(hb, 'BackgroundColor', pbcolor) % 将所有按钮的背景色设置为初始颜色

    mymatrix = zeros(4, 4); % 创建4x4的全零矩阵

    % 第一个位置为2
    inxrandi1 = randi(16); % 在1到16之间随机生成一个数
    mymatrix(inxrandi1) = 2; % 将随机位置的值设置为2
    set(hb(inxrandi1), 'String', mymatrix(inxrandi1)); % 设置对应按钮的显示内容为2
    set(hb(inxrandi1), 'BackgroundColor', mod(log2(mymatrix(inxrandi1))*numcolor,1)); % 设置对应按钮的背景色

    % 第二个位置为2或4
    inxrandi2 = randi(16); % 在1到16之间随机生成一个数
    while inxrandi2 == inxrandi1 % 如果第二个位置与第一个位置相同，则重新生成随机数
        inxrandi2 = randi(16);
    end
    mymatrix(inxrandi2) = randi([1, 2]) * 2; % 将随机位置的值设置为2或4
    set(hb(inxrandi2), 'String', mymatrix(inxrandi2)); % 设置对应按钮的显示内容
    set(hb(inxrandi2), 'BackgroundColor', mod(log2(mymatrix(inxrandi2))*numcolor,1)); % 设置对应按钮的背景色

    score = 0; % 初始化分数为0
    set(hscoretext, 'String', '0') % 设置分数文本的显示内容为0
end

%% 移动事件
% 将每行数据中的非零元素向左移动并合并相邻相同的元素
function moveevent()
    for i = 1:4
        myarray = mymatrix(i, :); % 取出第i行数据
        myarray(myarray==0) = []; % 去除数据中的0

        for j = 1:(length(myarray)-1)
            if myarray(j) == myarray(j+1) % 如果相邻两个元素相同
                myarray(j) = myarray(j) + myarray(j+1); % 合并两个元素
                myarray(j+1) = 0; % 合并后的元素置为0
                score = score + myarray(j); % 分数增加
            end
        end

        myarray(myarray==0) = []; % 去除合并后产生的0
        myarray((length(myarray)+1):4) = 0; % 补充0使长度为4
        mymatrix(i, :) = myarray; % 更新第i行数据
    end
end

%% 键盘事件
% 根据键盘按键进行相应操作，如上下左右移动，重新开始游戏等
function keyevent(~, event)
    mymatrixtemp = mymatrix; % 保存移动前的矩阵

    switch event.Key
        case 'uparrow'
            mymatrix = mymatrix'; % 转置矩阵
            moveevent(); % 调用移动事件
            mymatrix = mymatrix'; % 再次转置矩阵
        case 'leftarrow'
            mymatrix = mymatrix(:, end:-1:1); % 将每行数据进行反向排序
            moveevent(); % 调用移动事件
            mymatrix = mymatrix(:, end:-1:1); % 将每行数据再次反向排序
        case 'downarrow'
            mymatrix = mymatrix'; % 转置矩阵
            mymatrix = mymatrix(:, end:-1:1); % 将每行数据进行反向排序
            moveevent(); % 调用移动事件
            mymatrix = mymatrix(:, end:-1:1); % 将每行数据再次反向排序
            mymatrix = mymatrix'; % 再次转置矩阵
        case 'rightarrow'
            moveevent(); % 调用移动事件
        case 'escape'
            [mymatrix, score] = gameini(); % 重新开始游戏
            return
        otherwise
            return
    end

    if isempty(find(mymatrixtemp ~= mymatrix, 1)) % 判断矩阵是否发生变化
        return
    end

    set(hscoretext, 'String', score) % 更新分数文本

    inx = find(mymatrix == 0); % 找到矩阵中值为0的位置
    inxrandi = randi(length(inx)); % 在位置中随机选择一个位置
    mymatrix(inx(inxrandi)) = randi(2) * 2; % 在选择的位置上生成随机的2或4
    for i = 1:16
        if mymatrix(i) == 0 % 如果矩阵元素为0
            set(hb(i), 'String', ''); % 设置按钮的显示内容为空
            set(hb(i), 'BackgroundColor', pbcolor); % 设置按钮的背景色为初始颜色
        else
            set(hb(i), 'String', mymatrix(i)); % 设置按钮的显示内容
            set(hb(i), 'BackgroundColor', mod(log2(mymatrix(i))*numcolor,1)); % 设置按钮的背景色
        end
    end

    if isempty(find(mymatrix == 0, 1)) % 如果矩阵中没有值为0的元素
        mymatrixtemp = [ones(1,6); ones(4,1) mymatrix ones(4,1); ones(1,6)]; % 扩展矩阵
        for i = 2:5
            for j = 2:5
                if mymatrixtemp(i,j)==mymatrixtemp(i+1,j)...
                        || mymatrixtemp(i,j)==mymatrixtemp(i-1,j)...
                        || mymatrixtemp(i,j)==mymatrixtemp(i,j+1)...
                        || mymatrixtemp(i,j)==mymatrixtemp(i,j-1)
                    return
                end
            end
        end
        set(hscoretext, 'String', 'GAME OVER') % 显示游戏结束
    end
end
end
