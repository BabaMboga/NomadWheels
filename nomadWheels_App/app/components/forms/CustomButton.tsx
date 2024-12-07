import React from 'react';

interface CustomButtonProps {
    label : string;
    onClick: () => void;
    className?: string;
}

const CustomButton: React.FC<CustomButtonProps> = ({
    label,
    className,
    onClick
}) => {
  return (
    <div 
        onClick={onClick}
        className={`w-full py-4 bg-nomadWheels hover:bg-nomadWheels-dark text-white text-center rounded-xl transition cursor-pointer ${className}`}>
        {label}
    </div>
  )
}

export default CustomButton;