import React from "react";
import Image from "next/image";
import ReservationSidebar from "@/app/components/properties/ReservationSidebar";

const PropertyDetailPage = () => {
  return (
    <main className="max-w-[1500px] mx-auto px-6">
      <div className="w-full h-[64vh] overflow-hidden rounded-xl relative">
        <Image
          src="/properties/property-image-two.jpeg"
          alt="property image"
          fill
          className="object-cover w-full h-full"
        />
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="py-6 pr-6 col-span-3">
          <h1 className="mb-4 text-4xl">Property Name</h1>

          <span className="mb-6 block text-lg text-gray-600">
            4 passengers - automatic - 1600cc engine
          </span>

          <hr />

          <div className="py-6 flex items-center space-x-4">
            <Image
              src="/profiles/profile-image-one.jpeg"
              alt="property owner"
              width={50}
              height={50}
              className="rounded-full"
            />

            <p>
              <strong>John Doe</strong> is your host
            </p>
          </div>

          <hr />

          <p className="mt-6 text-lg">
            This spacious and versatile SUV is perfect for family road trips,
            group adventures, or even a weekend getaway. With comfortable
            seating for up to 7 passengers and ample luggage space, it’s
            designed to keep everyone relaxed and ready for the journey ahead.
            The all-wheel-drive system ensures smooth handling on city streets
            and rugged trails alike.
          </p>
        </div>

        <ReservationSidebar />
      </div>
    </main>
  );
};

export default PropertyDetailPage;
