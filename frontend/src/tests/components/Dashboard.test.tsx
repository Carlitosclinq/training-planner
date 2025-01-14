import React from 'react';
import { render, screen } from '@testing-library/react';
import { Dashboard } from '../components/Dashboard';

describe('Dashboard Component', () => {
  const mockData = {
    currentFTP: 250,
    weeklyTSS: 450,
    recentActivities: [
      {
        id: 1,
        type: 'ride',
        distance: 50000,
        duration: 7200
      }
    ]
  };

  it('renders dashboard metrics', () => {
    render(<Dashboard data={mockData} />);
    expect(screen.getByText('250W')).toBeInTheDocument();
    expect(screen.getByText('450')).toBeInTheDocument();
  });

  it('displays recent activities', () => {
    render(<Dashboard data={mockData} />);
    expect(screen.getByText('50.0 km')).toBeInTheDocument();
  });
});