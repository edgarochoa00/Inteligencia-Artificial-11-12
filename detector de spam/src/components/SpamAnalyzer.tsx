import React, { useState, useEffect } from 'react';
import { AlertTriangle, CheckCircle, BarChart3, AlertCircle } from 'lucide-react';
import { SpamDetector } from '../utils/spamDetector';
import type { SpamAnalysisResult, SpamDetectorStats } from '../types';

export default function SpamAnalyzer() {
  const [email, setEmail] = useState('');
  const [analysis, setAnalysis] = useState<SpamAnalysisResult | null>(null);
  const [stats, setStats] = useState<SpamDetectorStats>({
    totalChecked: 0,
    spamDetected: 0,
    averageConfidence: 0
  });

  useEffect(() => {
    if (email.trim()) {
      const result = SpamDetector.analyzeText(email);
      setAnalysis(result);
      setStats(prev => ({
        totalChecked: prev.totalChecked + 1,
        spamDetected: prev.spamDetected + (result.isSpam ? 1 : 0),
        averageConfidence: (prev.averageConfidence * prev.totalChecked + result.confidence) / (prev.totalChecked + 1)
      }));
    } else {
      setAnalysis(null);
    }
  }, [email]);

  const renderScoreBar = (score: number, label: string) => (
    <div className="mb-2">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className="text-sm font-medium text-gray-700">{Math.round(score * 100)}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${
            score > 0.6 ? 'bg-red-500' : score > 0.3 ? 'bg-yellow-500' : 'bg-green-500'
          }`}
          style={{ width: `${score * 100}%` }}
        />
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Detector Avanzado de Correo Spam
          </h1>
          <p className="text-gray-600">
            Analiza el contenido de tu correo para detectar indicadores de spam
          </p>
        </div>

        <div className="bg-white shadow-lg rounded-lg p-6 mb-8">
          <textarea
            className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Pega aquí el contenido del correo..."
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          {analysis && (
            <div className="mt-6">
              <div className="flex items-center mb-4">
                {analysis.isSpam ? (
                  <AlertTriangle className="h-6 w-6 text-red-500 mr-2" />
                ) : (
                  <CheckCircle className="h-6 w-6 text-green-500 mr-2" />
                )}
                <h2 className="text-xl font-semibold">
                  {analysis.isSpam ? 'Spam Potencial Detectado' : 'Probablemente No Es Spam'}
                </h2>
              </div>

              <div className="bg-gray-50 rounded-lg p-4 mb-6">
                <div className="text-lg mb-2">
                  Nivel de Confianza: {Math.round(analysis.confidence * 100)}%
                </div>
                {analysis.reasons.length > 0 && (
                  <ul className="list-disc list-inside text-gray-700">
                    {analysis.reasons.map((reason, index) => (
                      <li key={index}>{reason}</li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="space-y-4">
                <h3 className="text-lg font-medium mb-3">Análisis Detallado</h3>
                {renderScoreBar(analysis.scores.keywordScore, 'Análisis de Palabras Clave')}
                {renderScoreBar(analysis.scores.patternScore, 'Coincidencia de Patrones')}
                {renderScoreBar(analysis.scores.characterScore, 'Distribución de Caracteres')}
                {renderScoreBar(analysis.scores.lengthScore, 'Análisis de Longitud')}
                {renderScoreBar(analysis.scores.urlScore, 'Análisis de URLs')}
              </div>
            </div>
          )}
        </div>

        <div className="bg-white shadow-lg rounded-lg p-6">
          <div className="flex items-center mb-4">
            <BarChart3 className="h-6 w-6 text-blue-500 mr-2" />
            <h2 className="text-xl font-semibold">Estadísticas</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-sm text-gray-500">Total Analizados</div>
              <div className="text-2xl font-bold">{stats.totalChecked}</div>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-sm text-gray-500">Spam Detectado</div>
              <div className="text-2xl font-bold">{stats.spamDetected}</div>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-sm text-gray-500">Confianza Promedio</div>
              <div className="text-2xl font-bold">
                {Math.round(stats.averageConfidence * 100)}%
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}