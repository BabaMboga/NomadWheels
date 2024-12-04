import React from 'react';
import Image from 'next/image';

const Categories = () => {
  return (
    <div className='pt-3 cursor-pointer pb-6 flex items-center space-x-12'>
        <div className="pb-4 flex flex-col items-center space-y-2 border-b-2 border-white opacity-60 hover:border-gray-200 hover:opacity-100">
            <Image 
                src="/icons/suv.svg"
                alt="SUV icon"
                width={25}
                height={25}
            />
            <span className="text-xs">SUVs & Crossovers</span>
        </div>
        <div className="pb-4 flex flex-col items-center space-y-2 border-b-2 border-white opacity-60 hover:border-gray-200 hover:opacity-100">
            <Image 
                src="/icons/luxury-car.png"
                alt="SUV icon"
                width={25}
                height={25}
            />
            <span className="text-xs">Luxury Cars</span>
        </div>
        <div className="pb-4 flex flex-col items-center space-y-2 border-b-2 border-white opacity-60 hover:border-gray-200 hover:opacity-100">
            <Image 
                src="/icons/compact-car.png"
                alt="SUV icon"
                width={25}
                height={25}
            />
            <span className="text-xs">Compact Cars</span>
        </div>
        <div className="pb-4 flex flex-col items-center space-y-2 border-b-2 border-white opacity-60 hover:border-gray-200 hover:opacity-100">
            <Image 
                src="/icons/sports-car.png"
                alt="SUV icon"
                width={25}
                height={25}
            />
            <span className="text-xs">Sports Cars</span>
        </div>
        <div className="pb-4 flex flex-col items-center space-y-2 border-b-2 border-white opacity-60 hover:border-gray-200 hover:opacity-100">
            <Image 
                src="/icons/motorbike.png"
                alt="SUV icon"
                width={25}
                height={25}
            />
            <span className="text-xs">MotorCycles</span>
        </div>
    </div>
  )
}

export default Categories