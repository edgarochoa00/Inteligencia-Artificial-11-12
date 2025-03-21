export interface SpamAnalysisResult {
  isSpam: boolean;
  confidence: number;
  reasons: string[];
  scores: {
    keywordScore: number;
    patternScore: number;
    characterScore: number;
    lengthScore: number;
    urlScore: number;
  };
}

export interface SpamDetectorStats {
  totalChecked: number;
  spamDetected: number;
  averageConfidence: number;
}