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

const PropertyList = () => {
  const [properties, setProperties] = useState<PropertyType[]>([]);

  const getProperties = async () => {
    const url = 'http://localhost:8080/api/properties/';

    await fetch(url, {
      method: 'GET',
    })
      .then(response => response.json())
      .then((json) => {
        console.log('json', json);

        setProperties(json.data)
      })
      .catch((error) => {
        console.log('error',error)
      });
  };

  useEffect(() => {
    apiService.get("/api/properties/")
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