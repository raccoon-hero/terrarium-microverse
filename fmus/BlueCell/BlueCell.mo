model BlueCell
    parameter Real initialPositionX = 0;  // Starting X position
    parameter Real initialPositionY = 0;  // Starting Y position
    parameter Real boundaryLeft = 0;      // Box left boundary
    parameter Real boundaryRight = 500;   // Box right boundary
    parameter Real boundaryTop = 0;       // Box top boundary
    parameter Real boundaryBottom = 500;  // Box bottom boundary
    parameter Real acceleration = 1.5;    // Faster acceleration
    parameter Real speedMultiplier = 6.0; // Higher speed multiplier
    parameter Real dampingFactor = 0.1;   // Slightly higher damping for stability
    parameter Real energyDecay = 0.01;    // Energy decay rate

    input Real targetX;   // Target X position
    input Real targetY;   // Target Y position
    input Real direction; // Movement direction in radians
    input Real speed;     // Movement speed (scaled by speedMultiplier)

    output Real positionX(start=initialPositionX, fixed=true);
    output Real positionY(start=initialPositionY, fixed=true);
    output Real energyLevel;

    // Internal variables
    Real dx;
    Real dy;
    Real actualSpeed;
    Real energy;

equation
    // Adjust the speed with acceleration and damping
    der(actualSpeed) = (speed * speedMultiplier - actualSpeed) * acceleration;

    // Energy decreases with movement
    der(energy) = -energyDecay * actualSpeed;

    // Energy level reflects internal energy
    energyLevel = energy;

    // Calculate movement deltas
    dx = actualSpeed * cos(direction);
    dy = actualSpeed * sin(direction);

    // Update positions over time, clamped to boundaries
    der(positionX) = if (positionX + dx > boundaryRight) then 0
                     else if (positionX + dx < boundaryLeft) then 0
                     else dx;

    der(positionY) = if (positionY + dy > boundaryBottom) then 0
                     else if (positionY + dy < boundaryTop) then 0
                     else dy;

initial equation
    positionX = initialPositionX;
    positionY = initialPositionY;
    actualSpeed = 0;
    energy = 1.0;
end BlueCell;
