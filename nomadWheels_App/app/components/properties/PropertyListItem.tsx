import React from 'react';
import Image from 'next/image';

import { PropertyType } from './PropertyList';

interface PropertyProps {
    property: PropertyType
}

const PropertyListItem: React.FC<PropertyProps> = ({
    property
}) => {
    const imageUrl = property.primary_image_url || '/nomadWheels_App/public/properties/car-holder.jpg';
  return (
    <div className="cursor-pointer">
        <div className="relative overflow-hidden aspect-square rounded-xl">
            {property.primary_image_url ? (
                <Image 
                fill
                src = {imageUrl}
                alt = "property image"
                sizes = "(max-width: 768px) 768px, (max-width: 1200px): 768px, 768px"
                className='hover:scale-110 object-cover transition h-full w-full'
            />
            ):(
                <div className='flex items-center justify-center h-full w-full text-gray-500'>
                    No Image
                </div>
            )}
            
        </div>
        
        <div className="mt-2">
            <p className="text-lg font-bold">{property.title}</p>
        </div>

        <div className='mt-2'>
            <p className="text-sm text-gray-500">
                <strong>${property.price_per_day}</strong> per day
            </p>
        </div>
    </div>
  )
}

export default PropertyListItem