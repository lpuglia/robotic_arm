function [freq] = moveRobot(degrees, port)
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
        freq = cell2mat(textscan(s, '%d,%d,%d,%d,%d,%d'));
    catch
        freq = -1;
    end
    fclose(ser);
end