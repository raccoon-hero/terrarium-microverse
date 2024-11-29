model GreenCell
    parameter Real initialPosition = 0;
    Real position;
    Real acceleration = 0.5;
    Real speed;

equation
    der(position) = speed;
    der(speed) = acceleration;

initial equation
    position = initialPosition;
    speed = 0;
end GreenCell;
