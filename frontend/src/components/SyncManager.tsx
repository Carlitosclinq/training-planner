import React, { useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Calendar } from '@/components/ui/calendar';
import { Loader2 } from 'lucide-react';

interface SyncResult {
  success: number;
  failed: number;
  synced_workouts: Array<{
    date: string;
    name: string;
    intervals_id: string;
  }>;
  failed_workouts: Array<{
    date: string;
    name: string;
    error: string;
  }>;
}

const SyncManager: React.FC = () => {
  const [startDate, setStartDate] = useState<Date | undefined>(new Date());
  const [endDate, setEndDate] = useState<Date | undefined>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [syncResult, setSyncResult] = useState<SyncResult | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  const handleSync = async () => {
    if (!startDate || !endDate) {
      setError('Veuillez sélectionner les dates de début et de fin');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/sync-workouts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          start_date: startDate.toISOString(),
          end_date: endDate.toISOString(),
        }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la synchronisation');
      }

      const result = await response.json();
      setSyncResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  const handleResync = async () => {
    if (!syncResult?.failed_workouts.length) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/resync-failed', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(syncResult.failed_workouts),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la resynchronisation');
      }

      const result = await response.json();
      
      setSyncResult(prev => {
        if (!prev) return null;
        return {
          ...prev,
          success: prev.success + result.newly_synced.length,
          failed: result.still_failed.length,
          synced_workouts: [...prev.synced_workouts, ...result.newly_synced],
          failed_workouts: result.still_failed
        };
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Synchronisation Intervals.icu</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Date de début</label>
              <Calendar
                mode="single"
                selected={startDate}
                onSelect={setStartDate}
                className="rounded-md border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Date de fin</label>
              <Calendar
                mode="single"
                selected={endDate}
                onSelect={setEndDate}
                className="rounded-md border"
                disabled={(date) => date < (startDate || new Date())}
              />
            </div>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button
            onClick={handleSync}
            disabled={loading || !startDate || !endDate}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Synchronisation...
              </>
            ) : (
              'Synchroniser'
            )}
          </Button>

          {syncResult && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-sm text-gray-500">
                    Séances synchronisées: {syncResult.success}
                  </p>
                  <p className="text-sm text-gray-500">
                    Échecs: {syncResult.failed}
                  </p>
                </div>
                <Button
                  variant="outline"
                  onClick={() => setShowDetails(!showDetails)}
                >
                  {showDetails ? 'Masquer' : 'Détails'}
                </Button>
              </div>

              {showDetails && (
                <div className="space-y-4">
                  {syncResult.synced_workouts.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium mb-2">Séances synchronisées</h4>
                      <div className="space-y-2">
                        {syncResult.synced_workouts.map((workout, index) => (
                          <div
                            key={index}
                            className="p-2 bg-green-50 rounded text-sm"
                          >
                            {workout.date} - {workout.name}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {syncResult.failed_workouts.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium mb-2">Échecs</h4>
                      <div className="space-y-2">
                        {syncResult.failed_workouts.map((workout, index) => (
                          <div
                            key={index}
                            className="p-2 bg-red-50 rounded text-sm"
                          >
                            {workout.date} - {workout.name}
                            <p className="text-red-600 text-xs mt-1">
                              {workout.error}
                            </p>
                          </div>
                        ))}
                      </div>
                      <Button
                        onClick={handleResync}
                        disabled={loading}
                        className="mt-4"
                        variant="secondary"
                      >
                        Retenter la synchronisation
                      </Button>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default SyncManager;