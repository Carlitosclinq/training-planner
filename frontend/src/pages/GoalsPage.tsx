import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Calendar } from '@/components/ui/calendar';

interface Race {
  id?: number;
  name: string;
  date: Date;
  distance: number;
  elevation: number;
  priority: 'A' | 'B' | 'C';
}

interface PowerGoal {
  id?: number;
  targetFTP: number;
  targetDate: Date;
}

const GoalsPage = () => {
  const [races, setRaces] = useState<Race[]>([]);
  const [powerGoals, setPowerGoals] = useState<PowerGoal[]>([]);
  const [newRace, setNewRace] = useState<Partial<Race>>({
    name: '',
    distance: 0,
    elevation: 0,
    priority: 'B'
  });

  const handleAddRace = () => {
    if (newRace.name && newRace.date) {
      setRaces([...races, newRace as Race]);
      setNewRace({
        name: '',
        distance: 0,
        elevation: 0,
        priority: 'B'
      });
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Objectifs de courses</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                placeholder="Nom de la course"
                value={newRace.name}
                onChange={(e) => setNewRace({ ...newRace, name: e.target.value })}
              />
              <Input
                type="date"
                value={newRace.date?.toISOString().split('T')[0]}
                onChange={(e) => setNewRace({ ...newRace, date: new Date(e.target.value) })}
              />
              <Input
                type="number"
                placeholder="Distance (km)"
                value={newRace.distance}
                onChange={(e) => setNewRace({ ...newRace, distance: Number(e.target.value) })}
              />
              <Input
                type="number"
                placeholder="Dénivelé (m)"
                value={newRace.elevation}
                onChange={(e) => setNewRace({ ...newRace, elevation: Number(e.target.value) })}
              />
              <select
                className="border rounded p-2"
                value={newRace.priority}
                onChange={(e) => setNewRace({ ...newRace, priority: e.target.value as 'A' | 'B' | 'C' })}
              >
                <option value="A">Priorité A</option>
                <option value="B">Priorité B</option>
                <option value="C">Priorité C</option>
              </select>
              <Button onClick={handleAddRace}>Ajouter la course</Button>
            </div>

            <div className="mt-4">
              <h3 className="text-lg font-semibold mb-2">Courses planifiées</h3>
              <div className="space-y-2">
                {races.map((race, index) => (
                  <div key={index} className="p-4 border rounded">
                    <h4 className="font-medium">{race.name}</h4>
                    <p>Date: {race.date.toLocaleDateString()}</p>
                    <p>Distance: {race.distance}km</p>
                    <p>Dénivelé: {race.elevation}m</p>
                    <p>Priorité: {race.priority}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Objectifs de puissance</CardTitle>
        </CardHeader>
        <CardContent>
          {/* TODO: Implement power goals section */}
        </CardContent>
      </Card>
    </div>
  );
};

export default GoalsPage;