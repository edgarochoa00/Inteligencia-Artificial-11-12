// Utilidad completa de detección de spam
export class SpamDetector {
  private static readonly SPAM_KEYWORDS = [
    'viagra', 'cialis', 'casino', 'lotería', 'ganador', 
    'herencia', 'príncipe', 'transferencia bancaria', 'oportunidad de inversión',
    'criptomoneda', 'bitcoin', 'forex', 'trading', 'ganar dinero',
    'trabajo desde casa', 'dinero rápido', 'hazte rico', 'dinero gratis',
    'tiempo limitado', 'actúa ahora', 'urgente', 'felicitaciones', 'ganador afortunado',
    'millones de dólares', 'nigeriano', 'farmacia', 'descuento', 'oferta gratis',
    'sin riesgo', 'garantizado', 'mejores tarifas', '100% gratis', 'increíble',
    'bono en efectivo', 'deuda', 'crédito', 'oferta increíble', 'perder peso',
    'milagro', 'sin riesgo', 'satisfacción garantizada', 'promoción especial'
  ];

  private static readonly SUSPICIOUS_PATTERNS = [
    /^\s*RE:\s*\[?\d+\]?/i,
    /[A-Z]{10,}/,
    /\d{6,}/,
    /[!?]{2,}/,
    /[$€£¥]{2,}/,
    /\b[A-Z]+\s+[A-Z]+\s+[A-Z]+\b/,
    /[0-9]+%\s*(?:DESCUENTO|MENOS)/i,
    /(?:https?:\/\/[^\s]+){3,}/,
    /[^\s]+@[^\s]+\.[^\s]{2,}/g,
  ];

  private static calculateKeywordScore(text: string): number {
    const normalizedText = text.toLowerCase();
    const keywordMatches = SpamDetector.SPAM_KEYWORDS.filter(keyword => 
      normalizedText.includes(keyword.toLowerCase())
    );
    return keywordMatches.length / SpamDetector.SPAM_KEYWORDS.length;
  }

  private static calculatePatternScore(text: string): number {
    const patternMatches = SpamDetector.SUSPICIOUS_PATTERNS.filter(pattern => 
      pattern.test(text)
    );
    return patternMatches.length / SpamDetector.SUSPICIOUS_PATTERNS.length;
  }

  private static calculateCharacterScore(text: string): number {
    const uppercaseRatio = text.split('').filter(c => c >= 'A' && c <= 'Z').length / text.length;
    const specialCharRatio = text.split('').filter(c => '!@#$%^&*()'.includes(c)).length / text.length;
    const numberRatio = text.split('').filter(c => c >= '0' && c <= '9').length / text.length;
    
    return (uppercaseRatio + specialCharRatio + numberRatio) / 3;
  }

  private static calculateLengthScore(text: string): number {
    const words = text.split(/\s+/);
    const avgWordLength = words.reduce((sum, word) => sum + word.length, 0) / words.length;
    return Math.min(avgWordLength / 15, 1);
  }

  private static calculateUrlScore(text: string): number {
    const urlCount = (text.match(/https?:\/\/[^\s]+/g) || []).length;
    return Math.min(urlCount / 5, 1);
  }

  public static analyzeText(text: string): SpamAnalysisResult {
    const keywordScore = this.calculateKeywordScore(text);
    const patternScore = this.calculatePatternScore(text);
    const characterScore = this.calculateCharacterScore(text);
    const lengthScore = this.calculateLengthScore(text);
    const urlScore = this.calculateUrlScore(text);

    const scores = {
      keywordScore,
      patternScore,
      characterScore,
      lengthScore,
      urlScore
    };

    // Ponderación de los diferentes puntajes
    const weightedScore = 
      keywordScore * 0.35 +
      patternScore * 0.25 +
      characterScore * 0.15 +
      lengthScore * 0.1 +
      urlScore * 0.15;

    const reasons: string[] = [];
    if (keywordScore > 0.3) reasons.push('Contiene palabras clave sospechosas');
    if (patternScore > 0.3) reasons.push('Coincide con patrones de spam');
    if (characterScore > 0.4) reasons.push('Distribución inusual de caracteres');
    if (lengthScore > 0.6) reasons.push('Patrones inusuales de longitud de palabras');
    if (urlScore > 0.4) reasons.push('Contiene múltiples URLs');

    return {
      isSpam: weightedScore > 0.4,
      confidence: Math.round(weightedScore * 100) / 100,
      reasons,
      scores
    };
  }
}