ser = serial('COM6', 'DataBits', 8, 'BaudRate', 9600);
fopen(ser);
try
    readasync(ser);
    %ser.BytesAvailable
    s = fgetl(ser)
    c = textscan(s, '%c %d')
    %ser.BytesAvailable
    s = fgetl(ser)
    c = textscan(s, '%c %d')
catch
end
fclose(ser);