import React, { useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Calendar } from '@/components/ui/calendar';
import { Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/useToast';

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
  
  const { addToast, ToastList } = useToast();

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
      
      // Afficher une notification de succès
      addToast(
        'success',
        'Synchronisation terminée',
        `${result.success} séances synchronisées, ${result.failed} échecs`
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur inconnue';
      setError(errorMessage);
      addToast('destructive', 'Erreur', errorMessage);
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

      // Afficher une notification pour la resynchronisation
      addToast(
        'success',
        'Resynchronisation terminée',
        `${result.newly_synced.length} séances resynchronisées`
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur inconnue';
      setError(errorMessage);
      addToast('destructive', 'Erreur', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Synchronisation Intervals.icu</CardTitle>
        </CardHeader>
        <CardContent>
          {/* ... Le reste du composant reste identique ... */}
        </CardContent>
      </Card>
      <ToastList />
    </>
  );
};

export default SyncManager;