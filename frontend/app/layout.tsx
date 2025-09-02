export const metadata = {
  title: 'SmartAgent - מערכת ניהול טכנאים',
  description: 'מערכת ניהול טכנאים חכמה עם עיבוד שיחות אוטומטי',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="he" dir="rtl">
      <body className="font-sans antialiased">
        <nav className="bg-blue-600 text-white p-4">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold">SmartAgent</h1>
            <div className="space-x-4">
              <a href="/" className="hover:underline">בית</a>
              <a href="/calls" className="hover:underline">שיחות</a>
              <a href="/jobs" className="hover:underline">משימות</a>
              <a href="/calendar" className="hover:underline">יומן</a>
            </div>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  )
}
