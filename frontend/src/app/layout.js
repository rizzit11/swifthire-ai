import Link from 'next/link';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav className="p-4 bg-gray-100">
          <Link href="/" className="mr-4 text-blue-600">Home</Link>
          <Link href="/about" className="text-blue-600">About</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}
