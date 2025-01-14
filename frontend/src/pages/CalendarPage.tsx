import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Calendar } from '@/components/ui/calendar';
import { Switch } from '@/components/ui/switch';

interface DaySettings {
  date: Date;
  available: boolean;
  timeSlots: {
    start: string;
    end: string;
  }[];
  isRemoteWork: boolean;
}

const CalendarPage = () => {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());
  const [daySettings, setDaySettings] = useState<Record<string, DaySettings>>({});

  const handleDateSelect = (date: Date | undefined) => {
    if (!date) return;
    setSelectedDate(date);

    // Initialize settings for the selected date if not exists
    const dateKey = date.toISOString().split('T')[0];
    if (!daySettings[dateKey]) {
      setDaySettings({
        ...daySettings,
        [dateKey]: {
          date,
          available: true,
          timeSlots: [{ start: '09:00', end: '17:00' }],
          isRemoteWork: false,
        },
      });
    }
  };

  const updateDaySettings = (updates: Partial<DaySettings>) => {
    if (!selectedDate) return;
    const dateKey = selectedDate.toISOString().split('T')[0];
    setDaySettings({
      ...daySettings,
      [dateKey]: {
        ...daySettings[dateKey],
        ...updates,
      },
    });
  };

  const addTimeSlot = () => {
    if (!selectedDate) return;
    const dateKey = selectedDate.toISOString().split('T')[0];
    const settings = daySettings[dateKey];
    updateDaySettings({
      timeSlots: [...settings.timeSlots, { start: '09:00', end: '17:00' }],
    });
  };

  const removeTimeSlot = (index: number) => {
    if (!selectedDate) return;
    const dateKey = selectedDate.toISOString().split('T')[0];
    const settings = daySettings[dateKey];
    const newTimeSlots = settings.timeSlots.filter((_, i) => i !== index);
    updateDaySettings({ timeSlots: newTimeSlots });
  };

  const updateTimeSlot = (index: number, field: 'start' | 'end', value: string) => {
    if (!selectedDate) return;
    const dateKey = selectedDate.toISOString().split('T')[0];
    const settings = daySettings[dateKey];
    const newTimeSlots = settings.timeSlots.map((slot, i) =>
      i === index ? { ...slot, [field]: value } : slot
    );
    updateDaySettings({ timeSlots: newTimeSlots });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Calendrier</CardTitle>
        </CardHeader>
        <CardContent>
          <Calendar
            mode="single"
            selected={selectedDate}
            onSelect={handleDateSelect}
            className="rounded-md border w-full"
          />
        </CardContent>
      </Card>

      {selectedDate && (
        <Card>
          <CardHeader>
            <CardTitle>
              Configuration du {selectedDate.toLocaleDateString()}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label>Disponible</label>
                <Switch
                  checked={daySettings[selectedDate.toISOString().split('T')[0]]?.available}
                  onCheckedChange={(checked) => updateDaySettings({ available: checked })}
                />
              </div>

              <div className="flex items-center justify-between">
                <label>Télétravail</label>
                <Switch
                  checked={daySettings[selectedDate.toISOString().split('T')[0]]?.isRemoteWork}
                  onCheckedChange={(checked) => updateDaySettings({ isRemoteWork: checked })}
                />
              </div>

              <div className="space-y-2">
                <h3 className="text-sm font-medium">Plages horaires</h3>
                {daySettings[selectedDate.toISOString().split('T')[0]]?.timeSlots.map(
                  (slot, index) => (
                    <div key={index} className="flex space-x-2">
                      <Input
                        type="time"
                        value={slot.start}
                        onChange={(e) =>
                          updateTimeSlot(index, 'start', e.target.value)
                        }
                      />
                      <Input
                        type="time"
                        value={slot.end}
                        onChange={(e) =>
                          updateTimeSlot(index, 'end', e.target.value)
                        }
                      />
                      <Button
                        variant="destructive"
                        size="icon"
                        onClick={() => removeTimeSlot(index)}
                      >
                        ×
                      </Button>
                    </div>
                  )
                )}
                <Button onClick={addTimeSlot}>Ajouter une plage horaire</Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default CalendarPage;