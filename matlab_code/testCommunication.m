%t = tcpip('0.0.0.0', 8089, 'NetworkRole', 'server', 'InputBufferSize', 4096);

t = udp('172.16.69.175', 'LocalPort', 8089, 'Timeout', 60);

%t.ReadAsyncMode = 'continuous';
fopen(t);
try
    data = fgetl(t);
    res = textscan(data, '%f,%f');
    res = [res{1:2}];
    disp(res);
catch exc
    getReport(exc)
end
fclose(t);
