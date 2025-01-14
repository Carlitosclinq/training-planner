import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Calendar } from '../components/Calendar';

describe('Calendar Component', () => {
  const mockWorkouts = [
    {
      id: 1,
      date: '2024-01-14',
      type: 'interval',
      duration: 60,
      description: 'Test workout'
    }
  ];

  it('renders calendar with workouts', () => {
    render(<Calendar workouts={mockWorkouts} />);
    expect(screen.getByText('Test workout')).toBeInTheDocument();
  });

  it('allows workout selection', () => {
    const onSelect = jest.fn();
    render(<Calendar workouts={mockWorkouts} onSelectWorkout={onSelect} />);
    
    fireEvent.click(screen.getByText('Test workout'));
    expect(onSelect).toHaveBeenCalledWith(mockWorkouts[0]);
  });

  it('handles empty workout list', () => {
    render(<Calendar workouts={[]} />);
    expect(screen.getByText('No workouts scheduled')).toBeInTheDocument();
  });
});