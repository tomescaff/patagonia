% script for displaying yearly series of modeled variables

% read csv file from processing data output
filepath = '../../processing/data/year_piseries.txt';
strfmt = '%{yyyy-MM-dd}D%f%f%f%f%f%f';
T = readtable(filepath, 'Delimiter', ';', 'Format',strfmt);


mb = T.mb/1000;
pr = T.pr/1000;
acc = T.acc/1000;
abl = T.abl/1000;
time = 1980:2014;

mb_mean = mean(mb)*ones(1,numel(time));
pr_mean = mean(pr)*ones(1,numel(time));
acc_mean = mean(acc)*ones(1,numel(time));
abl_mean = mean(abl)*ones(1,numel(time));
tas_mean = mean(T.tas)*ones(1,numel(time));
rsds_mean = mean(T.rsds)*ones(1,numel(time));

[ax, xLine, xText] = stackedaxes(time, [mb, acc, pr, abl, T.tas, T.rsds]);
hold(ax(1),'on');
plot(time,mb_mean,'Parent',ax(1))

hold(ax(2),'on');
plot(time,acc_mean,'Parent',ax(2))

hold(ax(3),'on');
plot(time,pr_mean,'Parent',ax(3))

hold(ax(4),'on');
plot(time,abl_mean,'Parent',ax(4))

hold(ax(5),'on');
plot(time,tas_mean,'Parent',ax(5))

hold(ax(6),'on');
plot(time,rsds_mean,'Parent',ax(6))
