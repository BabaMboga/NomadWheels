'use client';


import React from 'react';
import { useEffect, useState } from 'react';
import PropertyListItem from './PropertyListItem';
import apiService from '@/app/services/apiService';

export type PropertyType = {
  id: string;
  title: string;
  primary_image_url: string | null;
  price_per_day: number;
}
export type PropertyResponse ={
  data: PropertyType[]
}
const PropertyList = () => {
  const [properties, setProperties] = useState<PropertyType[]>([]);

  const getProperties = async () => {
    const tmpProperties = await apiService.get<PropertyResponse>('/api/properties')

    setProperties(tmpProperties.data);
  };

  useEffect(() => {
    
    getProperties();

  }, []);
  return (
    <>
        {properties.map((property) => {
          return (
            <PropertyListItem 
              key ={property.id}
              property = {property}
            />
          )
        })}
        
        
        
    </>
    
  )
}

export default PropertyList;