function [robDegrees, intDegrees, intErr] = moveRobotDH(degrees, port)
    if nargin < 2
        port = 'COM6';
    end
    %NaN = don't move the servo
    
    %0 - 150 massimi gradi per base motore 1
    %0 - 150 moptore 2
    %0 - 150 motore 3
    %0 - 140 motore 4
    %0 - 160 massimi gradi per rotazione pinza
    %80 aperto - 120
    
    % rotation limits
    lims = [0, 0, 0, 0, 0, 80;
            150, 150, 150, 140, 160, 130];
    % difference to 0 degrees
    diff = [90, 0, 60, -7, 157, 0];
    % -1 inverts the rotation
    invert = [1, 1, -1, -1, -1, 1];
    % servos move by different angles
    
    % this scaling fixes this
    scaling = [75/90, 78/90, 75/90, 75/90, 1, 1];
    
    %nans = isnan(degrees);
    degrees = diff + degrees .* scaling .* invert;
    
    %degrees = degrees .* scaling;
    
    % Fix degrees exceding limits
    wrongidx = degrees < lims(1,:);
    if (sum(wrongidx)>0)
        warning('Degree out of bounds');
    end
    degrees(wrongidx) = lims(1,wrongidx);
    wrongidx = degrees > lims(2,:);
    if (sum(wrongidx)>0)
        warning('Degree out of bounds');
    end
    degrees(wrongidx) = lims(2,wrongidx);
    degrees = round(degrees, 0);
    
    degrees(isnan(degrees)) = -1;
    
    robDegrees = degrees;
    [intDegrees, intErr] = moveRobot(degrees, port);
end