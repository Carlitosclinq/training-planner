import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Calendar } from '@/components/ui/calendar';
import { Loader2, AlertTriangle, CheckCircle } from 'lucide-react';

interface ReadinessAnalysis {
  predicted_ftp: number;
  ftp_readiness: number;
  fitness_trend: string;
  recommendations: string[];
}

const RaceReadiness = () => {
  const [raceDate, setRaceDate] = useState<Date | undefined>();
  const [targetFTP, setTargetFTP] = useState<string>('');
  const [requiredCTL, setRequiredCTL] = useState<string>('');
  const [analysis, setAnalysis] = useState<ReadinessAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!raceDate || !targetFTP || !requiredCTL) {
      setError('Veuillez remplir tous les champs');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/predictions/race-readiness', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          race_date: raceDate.toISOString(),
          target_ftp: parseFloat(targetFTP),
          required_ctl: parseFloat(requiredCTL)
        }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de l\'analyse');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  const getReadinessIndicator = () => {
    if (!analysis) return null;

    if (analysis.ftp_readiness >= 95) {
      return (
        <div className="flex items-center text-green-600">
          <CheckCircle className="w-5 h-5 mr-2" />
          Prêt pour la course
        </div>
      );
    }

    if (analysis.ftp_readiness >= 80) {
      return (
        <div className="flex items-center text-yellow-600">
          <AlertTriangle className="w-5 h-5 mr-2" />
          Préparation en cours
        </div>
      );
    }

    return (
      <div className="flex items-center text-red-600">
        <AlertTriangle className="w-5 h-5 mr-2" />
        Préparation insuffisante
      </div>
    );
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Analyse de la préparation course</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Date de la course
              </label>
              <Calendar
                mode="single"
                selected={raceDate}
                onSelect={setRaceDate}
                className="rounded-md border"
                disabled={(date) => date < new Date()}
              />
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  FTP cible (W)
                </label>
                <Input
                  type="number"
                  value={targetFTP}
                  onChange={(e) => setTargetFTP(e.target.value)}
                  placeholder="Ex: 280"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">
                  CTL requis
                </label>
                <Input
                  type="number"
                  value={requiredCTL}
                  onChange={(e) => setRequiredCTL(e.target.value)}
                  placeholder="Ex: 80"
                />
              </div>
            </div>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyse en cours...
              </>
            ) : (
              'Analyser la préparation'
            )}
          </Button>

          {analysis && (
            <div className="space-y-6 mt-6">
              <div className="p-4 bg-gray-50 rounded-md">
                {getReadinessIndicator()}
                <div className="mt-4 grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500">FTP prédit</p>
                    <p className="text-lg font-semibold">{analysis.predicted_ftp}W</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Niveau de préparation</p>
                    <p className="text-lg font-semibold">{analysis.ftp_readiness}%</p>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="text-sm font-medium mb-2">Recommandations</h4>
                <div className="space-y-2">
                  {analysis.recommendations.map((recommendation, index) => (
                    <p key={index} className="text-sm text-gray-600">
                      • {recommendation}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default RaceReadiness;