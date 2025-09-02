import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">SmartAgent</h1>
        <p className="text-center text-gray-600 mb-8">
          מערכת ניהול טכנאים חכמה עם עיבוד שיחות אוטומטי
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <Link href="/calls" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-2">שיחות</h2>
            <p className="text-gray-600">צפייה וניהול שיחות לקוחות</p>
          </Link>

          <Link href="/jobs" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-2">קריאות שירות</h2>
            <p className="text-gray-600">ניהול משימות וטיקטים</p>
          </Link>

          <Link href="/calendar" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-2">יומן</h2>
            <p className="text-gray-600">פגישות ולוח זמנים</p>
          </Link>
        </div>
      </div>
    </div>
  )
}
