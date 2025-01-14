import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, TrendingUp, TrendingDown, Refresh } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface Prediction {
  current_ftp: number;
  predicted_ftp: number;
  confidence: number;
  predicted_date: string;
  recommendations: string[];
  metrics_trends: {
    ctl_trend: string;
    atl_trend: string;
    tsb_trend: string;
  };
}

const PerformancePredictor = () => {
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPrediction = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/predictions/performance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ days_ahead: 30 }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des prédictions');
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrediction();
  }, []);

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'decreasing':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin" />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
          <Button
            onClick={fetchPrediction}
            variant="outline"
            className="mt-4"
          >
            <Refresh className="w-4 h-4 mr-2" />
            Réessayer
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!prediction) {
    return null;
  }

  const ftpData = [
    { name: 'Actuel', ftp: prediction.current_ftp },
    { name: 'Prédit', ftp: prediction.predicted_ftp }
  ];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Prédiction de Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">FTP</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={ftpData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="ftp"
                      stroke="#8884d8"
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <p className="text-sm text-gray-500 mt-2">
                Confiance: {prediction.confidence}%
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Tendances</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span>Charge (CTL)</span>
                  {getTrendIcon(prediction.metrics_trends.ctl_trend)}
                </div>
                <div className="flex items-center justify-between">
                  <span>Fatigue (ATL)</span>
                  {getTrendIcon(prediction.metrics_trends.atl_trend)}
                </div>
                <div className="flex items-center justify-between">
                  <span>Forme (TSB)</span>
                  {getTrendIcon(prediction.metrics_trends.tsb_trend)}
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-4">Recommandations</h3>
            <div className="space-y-2">
              {prediction.recommendations.map((recommendation, index) => (
                <p key={index} className="text-sm text-gray-600">
                  • {recommendation}
                </p>
              ))}
            </div>
          </div>

          <Button
            onClick={fetchPrediction}
            variant="outline"
            className="mt-6"
          >
            <Refresh className="w-4 h-4 mr-2" />
            Actualiser
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default PerformancePredictor;