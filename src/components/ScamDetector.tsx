import { useState } from 'react';
import { AlertCircle, CheckCircle, Link, MessageSquare, Shield, AlertTriangle } from 'lucide-react';

interface URLAnalysis {
  url: string;
  suspicion_score: number;
  is_suspicious: boolean;
  reasons: string[];
}

interface DetectionResult {
  is_scam: boolean;
  confidence: number;
  verdict: string;
  text_scam_probability: number;
  text_safe_probability: number;
  urls_found: number;
  has_suspicious_urls: boolean;
  max_url_suspicion_score: number;
  url_analyses: URLAnalysis[];
  reasons: string[];
  text: string;
}

export default function ScamDetector() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [error, setError] = useState('');

  const analyzeMessage = async () => {
    if (!message.trim()) {
      setError('Please enter a message to analyze');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/detect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      if (data.success) {
        setResult(data.data);
      } else {
        setError(data.error || 'Failed to analyze message');
      }
    } catch (err) {
      setError('Failed to connect to ML API. Make sure the Python API server is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  const exampleMessages = [
    "Hi, how are you? Let's catch up tomorrow.",
    "URGENT! Your bank account has been suspended. Click http://secure-bank-verify.tk/login to restore access!",
    "Congratulations! You've won 10 lakhs. Pay 5000 processing fee to bit.ly/claim123",
    "Meeting at 3 PM today in conference room",
    "FREE iPhone 15! Limited offer! Click www.free-iphone-claim.xyz/winner",
    "Panam jeyikum! Investment guarantee 100%. Contact now!"
  ];

  const getRiskColor = (score: number) => {
    if (score >= 61) return 'text-red-600';
    if (score >= 41) return 'text-orange-600';
    if (score >= 21) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getRiskLabel = (score: number) => {
    if (score >= 61) return 'Critical';
    if (score >= 41) return 'High';
    if (score >= 21) return 'Medium';
    return 'Low';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Shield className="w-12 h-12 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">
              WhatsApp Scam Detector
            </h1>
          </div>
          <p className="text-gray-600 text-lg">
            ML-powered system to detect scam, spam, and phishing messages with advanced URL analysis
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Enter Message to Analyze
          </label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Paste your WhatsApp message here..."
            className="w-full h-32 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all resize-none"
          />

          <div className="flex items-center gap-3 mt-4">
            <button
              onClick={analyzeMessage}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors shadow-lg shadow-blue-500/30"
            >
              {loading ? 'Analyzing...' : 'Analyze Message'}
            </button>

            <button
              onClick={() => {
                setMessage('');
                setResult(null);
                setError('');
              }}
              className="px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-300 transition-colors"
            >
              Clear
            </button>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
              <div className="flex items-center">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          )}
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <MessageSquare className="w-5 h-5 mr-2" />
            Try Example Messages
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {exampleMessages.map((example, index) => (
              <button
                key={index}
                onClick={() => setMessage(example)}
                className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm text-gray-700 transition-colors border border-gray-200"
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {result && (
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <div className="mb-6">
              <div className={`flex items-center justify-between p-6 rounded-xl ${
                result.is_scam ? 'bg-red-50 border-2 border-red-500' : 'bg-green-50 border-2 border-green-500'
              }`}>
                <div className="flex items-center">
                  {result.is_scam ? (
                    <AlertTriangle className="w-8 h-8 text-red-600 mr-3" />
                  ) : (
                    <CheckCircle className="w-8 h-8 text-green-600 mr-3" />
                  )}
                  <div>
                    <h2 className={`text-2xl font-bold ${result.is_scam ? 'text-red-600' : 'text-green-600'}`}>
                      {result.verdict}
                    </h2>
                    <p className="text-gray-600">
                      Confidence: {(result.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-5 rounded-xl">
                <h3 className="font-semibold text-gray-800 mb-3 flex items-center">
                  <MessageSquare className="w-5 h-5 mr-2" />
                  Text Analysis
                </h3>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">Scam Probability:</span>
                    <span className="font-bold text-red-600">
                      {(result.text_scam_probability * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">Safe Probability:</span>
                    <span className="font-bold text-green-600">
                      {(result.text_safe_probability * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-5 rounded-xl">
                <h3 className="font-semibold text-gray-800 mb-3 flex items-center">
                  <Link className="w-5 h-5 mr-2" />
                  URL Analysis
                </h3>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">URLs Found:</span>
                    <span className="font-bold">{result.urls_found}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700">Suspicious URLs:</span>
                    <span className={`font-bold ${result.has_suspicious_urls ? 'text-red-600' : 'text-green-600'}`}>
                      {result.has_suspicious_urls ? 'YES' : 'NO'}
                    </span>
                  </div>
                  {result.max_url_suspicion_score > 0 && (
                    <div className="flex justify-between items-center">
                      <span className="text-gray-700">Max Suspicion:</span>
                      <span className={`font-bold ${getRiskColor(result.max_url_suspicion_score)}`}>
                        {result.max_url_suspicion_score}/100 ({getRiskLabel(result.max_url_suspicion_score)})
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {result.url_analyses.length > 0 && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-800 mb-3 text-lg">Detailed URL Analysis</h3>
                <div className="space-y-3">
                  {result.url_analyses.map((urlData, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-xl border-2 ${
                        urlData.is_suspicious ? 'bg-red-50 border-red-300' : 'bg-green-50 border-green-300'
                      }`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <p className="font-mono text-sm text-gray-800 break-all">{urlData.url}</p>
                        </div>
                        <span className={`ml-3 px-3 py-1 rounded-full text-xs font-bold ${
                          urlData.is_suspicious ? 'bg-red-200 text-red-800' : 'bg-green-200 text-green-800'
                        }`}>
                          {urlData.is_suspicious ? 'SUSPICIOUS' : 'OK'}
                        </span>
                      </div>
                      <div className="flex items-center mb-2">
                        <span className="text-sm text-gray-600 mr-2">Suspicion Score:</span>
                        <span className={`font-bold ${getRiskColor(urlData.suspicion_score)}`}>
                          {urlData.suspicion_score}/100
                        </span>
                      </div>
                      {urlData.reasons.length > 0 && (
                        <div className="mt-2">
                          <p className="text-xs font-semibold text-gray-700 mb-1">Reasons:</p>
                          <ul className="text-xs text-gray-600 space-y-1">
                            {urlData.reasons.map((reason, idx) => (
                              <li key={idx} className="flex items-start">
                                <span className="mr-2">•</span>
                                <span>{reason}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="bg-gray-50 p-5 rounded-xl">
              <h3 className="font-semibold text-gray-800 mb-3">Detection Reasons</h3>
              <ul className="space-y-2">
                {result.reasons.map((reason, index) => (
                  <li key={index} className="flex items-start text-gray-700">
                    <span className="mr-2 mt-1">•</span>
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        <div className="mt-8 bg-white rounded-2xl shadow-xl p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">How It Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-xl">
              <h4 className="font-semibold text-blue-900 mb-2">1. Text Analysis</h4>
              <p className="text-sm text-gray-700">
                Machine learning model analyzes message content using TF-IDF vectorization and Random Forest classification
              </p>
            </div>
            <div className="p-4 bg-purple-50 rounded-xl">
              <h4 className="font-semibold text-purple-900 mb-2">2. URL Detection</h4>
              <p className="text-sm text-gray-700">
                Extracts and analyzes URLs for phishing indicators: keywords, shortened links, suspicious TLDs, IP addresses
              </p>
            </div>
            <div className="p-4 bg-green-50 rounded-xl">
              <h4 className="font-semibold text-green-900 mb-2">3. Combined Decision</h4>
              <p className="text-sm text-gray-700">
                Weighted scoring combines text probability (60%) and URL risk (40%) for final verdict
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
