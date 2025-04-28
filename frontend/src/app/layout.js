// frontend/src/app/layout.js

import Link from 'next/link';

export const metadata = {
  title: 'SwiftHire AI',
  description: 'Resume parsing & interview question generator',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        <nav className="p-4 bg-gray-100">
          <Link href="/" className="mr-4 text-blue-600">Home</Link>
          <Link href="/about" className="mr-4 text-blue-600">About</Link>
          <Link href="/questions" className="mr-4 text-blue-600">Generate-Questions</Link>
          <Link href="/signup" className="mr-4 text-blue-600">Signup</Link>
          <Link href="/login" className="text-blue-600">Login</Link>
        </nav>
        <main className="flex-1 p-6">{children}</main>
      </body>
    </html>
  );
}
