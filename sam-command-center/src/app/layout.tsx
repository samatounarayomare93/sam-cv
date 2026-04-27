import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Rita Command Center | God Mode",
  description: "Autonomous Agentic Glassmorphism Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
