function [freq, robotErr] = moveRobot(degrees, port)
    if nargin < 2
        port = 'COM6';
    end
    ser = serial(port, 'DataBits', 8, 'BaudRate', 9600);
    fopen(ser);
    try
        readasync(ser);
        %ser.BytesAvailable
        fprintf(ser, '%d,%d,%d,%d,%d,%d&', degrees);
        s = fgetl(ser);
        res = textscan(s, '%d,%d,%d,%d,%d,%d (%[^\n)])');
        freq = [res{1:6}];
        robotErr = res{7};
    catch exc
        freq = -1;
        robotErr = cell(0,1);
        getReport(exc)
    end
    fclose(ser);
end