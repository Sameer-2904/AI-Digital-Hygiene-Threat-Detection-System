import React from 'react'
import { FiCheckCircle, FiAlertCircle, FiXCircle } from 'react-icons/fi'

export default function RiskResult({ result }) {
  if (!result) return null

  const getRiskColor = (level) => {
    switch(level) {
      case 'LOW': return 'green'
      case 'MEDIUM': return 'yellow'
      case 'HIGH': return 'orange'
      case 'CRITICAL': return 'red'
      default: return 'gray'
    }
  }

  const getRiskIcon = (level) => {
    switch(level) {
      case 'LOW': return <FiCheckCircle className="text-2xl text-green-500" />
      case 'MEDIUM': return <FiAlertCircle className="text-2xl text-yellow-500" />
      case 'HIGH': return <FiAlertCircle className="text-2xl text-orange-500" />
      case 'CRITICAL': return <FiXCircle className="text-2xl text-red-500" />
      default: return null
    }
  }

  const color = getRiskColor(result.risk_level)
  const bgColor = {
    green: 'bg-green-50 border-green-200',
    yellow: 'bg-yellow-50 border-yellow-200',
    orange: 'bg-orange-50 border-orange-200',
    red: 'bg-red-50 border-red-200',
    gray: 'bg-gray-50 border-gray-200'
  }[color]

  const textColor = {
    green: 'text-green-800',
    yellow: 'text-yellow-800',
    orange: 'text-orange-800',
    red: 'text-red-800',
    gray: 'text-gray-800'
  }[color]

  return (
    <div className={`border rounded-lg p-6 ${bgColor}`}>
      <div className="flex items-center gap-4 mb-4">
        {getRiskIcon(result.risk_level)}
        <div>
          <h3 className={`text-xl font-bold ${textColor}`}>
            {result.risk_level} Risk • {result.safety_label || ''}
          </h3>
          <p className="text-sm text-gray-600">
            Confidence: {(result.confidence * 100).toFixed(0)}% • Score: {result.risk_score ?? '-'}
          </p>
        </div>
      </div>

      {result.detected_risks.length > 0 && (
        <div className="mb-4">
          <h4 className="font-semibold mb-2">Detected Issues:</h4>
          <ul className="space-y-1">
            {result.detected_risks.map((risk, idx) => (
              <li key={idx} className="text-sm flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full bg-${color}-500`}></span>
                {risk}
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.explanation && (
        <div className="bg-white bg-opacity-50 rounded p-4 mb-4">
          <h4 className="font-semibold mb-2">What This Means:</h4>
          <p className="text-sm whitespace-pre-wrap">{result.explanation}</p>
        </div>
      )}

      {result.recommendations && result.recommendations.length > 0 && (
        <div>
          <h4 className="font-semibold mb-2">What You Should Do:</h4>
          <ul className="space-y-2">
            {result.recommendations.map((rec, idx) => (
              <li key={idx} className="text-sm">{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
