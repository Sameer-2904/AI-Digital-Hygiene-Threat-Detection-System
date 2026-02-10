import React, { useState } from 'react'
import TextAnalyzer from './components/TextAnalyzer'
import URLAnalyzer from './components/URLAnalyzer'

function App() {
  const [activeTab, setActiveTab] = useState('text')

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-indigo-600 text-white shadow-lg">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-2">🛡️ Digital Hygiene Companion</h1>
          <p className="text-indigo-100">Stay safe online: Detect phishing, risky links, and suspicious behavior</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Tab Navigation */}
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setActiveTab('text')}
            className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
              activeTab === 'text'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            📧 Email & Messages
          </button>
          <button
            onClick={() => setActiveTab('url')}
            className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
              activeTab === 'url'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            🔗 Links
          </button>
        </div>

        {/* Content */}
        {activeTab === 'text' && <TextAnalyzer />}
        {activeTab === 'url' && <URLAnalyzer />}

        {/* Learning Resources Section */}
        <section className="mt-12 bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold mb-4">📚 Quick Safety Tips</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="border-l-4 border-blue-600 pl-4">
              <h3 className="font-semibold mb-2">🎣 About Phishing</h3>
              <p className="text-gray-700 text-sm">
                Phishing emails pretend to be from legitimate companies to trick you into revealing passwords or personal info. Be skeptical of urgent requests and always verify by visiting the official website directly.
              </p>
            </div>
            <div className="border-l-4 border-green-600 pl-4">
              <h3 className="font-semibold mb-2">🔗 About Suspicious Links</h3>
              <p className="text-gray-700 text-sm">
                Never click links from unknown senders. Hover over links to see where they really go. Legitimate companies don't ask you to click links to "verify" accounts.
              </p>
            </div>
            <div className="border-l-4 border-purple-600 pl-4">
              <h3 className="font-semibold mb-2">🎭 About Social Engineering</h3>
              <p className="text-gray-700 text-sm">
                Scammers use urgency ("Act now!"), fear ("Your account is locked!"), or appeals to authority to manipulate you. Always think before you act on suspicious requests.
              </p>
            </div>
            <div className="border-l-4 border-red-600 pl-4">
              <h3 className="font-semibold mb-2">🔐 Protect Your Passwords</h3>
              <p className="text-gray-700 text-sm">
                Never share passwords via email or chat. Legitimate services never ask for passwords. Use strong, unique passwords for each account.
              </p>
            </div>
          </div>
        </section>

        {/* Privacy Notice */}
        <section className="mt-8 bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="font-bold text-green-900 mb-2">🔒 Your Privacy is Protected</h3>
          <p className="text-green-800 text-sm">
            This tool processes all analysis locally on your device. Nothing you analyze is sent to external servers or stored. Your security checks stay completely private.
          </p>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 mt-12">
        <div className="max-w-6xl mx-auto px-4 py-8 text-center text-sm">
          <p>Digital Hygiene Companion v1.0 | Built to keep students safe online 🛡️</p>
          <p className="mt-2">Always report suspicious activity to your IT support team</p>
        </div>
      </footer>
    </div>
  )
}

export default App
