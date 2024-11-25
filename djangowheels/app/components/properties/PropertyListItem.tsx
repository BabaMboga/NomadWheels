import React from 'react';
import Image from 'next/image';

const PropertyListItem = () => {
  return (
    <div className="cursor-pointer">
        <div className="overflow-hidden aspect-square rounded-xl">
            <Image 
                fill
                src = ""
                alt = "property image"
            />
        </div>
    </div>
  )
}

export default PropertyListItem