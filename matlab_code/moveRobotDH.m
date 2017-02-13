function [robDegrees, intDegrees, intErr] = moveRobotDH(degrees, port)
    if nargin < 2
        port = 'COM6';
    end
    %0 - 150 massimi gradi per base motore 1
    %0 - 150 moptore 2
    %0 - 150 motore 3
    %0 - 140 motore 4
    %0 - 160 massimi gradi per rotazione pinza
    %80 aperto - 120
    
    lims = [0, 0, 0, 0, 0, 80;
            150, 150, 150, 140, 160, 120];
    diff = [0, 0, 0, 0, 157, 0];
    
    minones = degrees == -1;
    degrees = diff - degrees;
    
    % Fix degrees exceding limits
    wrongidx = degrees < lims(1,:) & ~minones;
    if (sum(wrongidx)>0)
        warning('Degree out of bounds');
    end
    degrees(wrongidx) = lims(1,wrongidx);
    wrongidx = degrees > lims(2,:);
    if (sum(wrongidx)>0)
        warning('Degree out of bounds');
    end
    degrees(wrongidx) = lims(2,wrongidx);
    
    degrees(minones) = -1;
    
    robDegrees = degrees;
    [intDegrees, intErr] = moveRobot(degrees, port);
end