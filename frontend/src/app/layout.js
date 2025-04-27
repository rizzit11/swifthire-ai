// frontend/src/app/layout.js

import Link from 'next/link';

export const metadata = {
  title: 'SwiftHire AI',
  description: 'Resume parsing & interview question generator',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav className="p-4 bg-gray-100">
          <Link href="/" className="mr-4 text-blue-600">Home</Link>
          <Link href="/about" className="mr-4 text-blue-600">About</Link>
          <Link href="/questions" className="text-blue-600">Questions</Link>
        </nav>
        <main className="p-4">
          {children}
        </main>
      </body>
    </html>
  );
}
