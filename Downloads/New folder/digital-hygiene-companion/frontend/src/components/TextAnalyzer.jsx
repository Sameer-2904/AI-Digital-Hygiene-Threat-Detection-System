import React, { useState } from 'react'
import axios from 'axios'
import RiskResult from './RiskResult'
import { FiLoader } from 'react-icons/fi'

export default function TextAnalyzer() {
  const [content, setContent] = useState('')
  const [contentType, setContentType] = useState('email')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!content.trim()) {
      setError('Please enter some text to analyze')
      return
    }

    // Require explicit consent
    const consent = localStorage.getItem('dh_consent') === 'true' || window.confirm('Do you consent to sending this content for analysis? No raw data will be stored; only anonymized statistics are kept.')
    if (!consent) {
      setError('Consent required to perform analysis')
      return
    }

    // Compute client-side SHA-256 hash for anonymization token
    async function computeHash(str) {
      const enc = new TextEncoder()
      const data = enc.encode(str)
      const hashBuffer = await crypto.subtle.digest('SHA-256', data)
      const hashArray = Array.from(new Uint8Array(hashBuffer))
      return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const hashed = await computeHash(content)
      if (localStorage.getItem('dh_consent') !== 'true') localStorage.setItem('dh_consent', 'true')
      const response = await axios.post('/api/analyze/text', {
        content,
        content_type: contentType,
        consent: true,
        hashed_input: hashed
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">📧 Email & Message Analyzer</h2>
      
      <form onSubmit={handleAnalyze} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Content Type</label>
          <select
            value={contentType}
            onChange={(e) => setContentType(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="email">Email</option>
            <option value="message">Chat Message</option>
            <option value="sms">SMS</option>
            <option value="post">Social Media Post</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Text Content</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Paste the email, message, or text you want to check here..."
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 h-40"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <FiLoader className="animate-spin" /> Analyzing...
            </>
          ) : (
            '🔍 Analyze Text'
          )}
        </button>
      </form>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6">
          <RiskResult result={result} />
        </div>
      )}
    </div>
  )
}
