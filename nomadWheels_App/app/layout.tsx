import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import Navbar from "./components/navbar/Navbar";
import Modal from "./components/modals/Modal";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Nomad Wheels",
  description: "Your ultimate platform to discover, book, and share vehicles effortlessly.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  const content = (
    <p className=""> Yo </p>
  )
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased inter.className`}
      >

        <Navbar />

        <div className="pt-32">
          {children}
        </div>

        <Modal 

          label = 'Modal Test'
          content = {content}
        />
        
      </body>
    </html>
  );
}
