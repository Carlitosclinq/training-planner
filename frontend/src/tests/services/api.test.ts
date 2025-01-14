import { fetchActivities, createGoal, generatePlan } from '../services/api';
import axios from 'axios';

jest.mock('axios');

describe('API Service', () => {
  beforeEach(() => {
    (axios.get as jest.Mock).mockClear();
    (axios.post as jest.Mock).mockClear();
  });

  it('fetches activities', async () => {
    const mockActivities = [{ id: 1, type: 'ride' }];
    (axios.get as jest.Mock).mockResolvedValue({ data: mockActivities });

    const result = await fetchActivities();
    expect(result).toEqual(mockActivities);
  });

  it('creates a goal', async () => {
    const mockGoal = { type: 'ftp', targetValue: 300 };
    (axios.post as jest.Mock).mockResolvedValue({ data: { id: 1, ...mockGoal } });

    const result = await createGoal(mockGoal);
    expect(result.id).toBe(1);
  });

  it('handles API errors', async () => {
    (axios.get as jest.Mock).mockRejectedValue(new Error('Network error'));

    await expect(fetchActivities()).rejects.toThrow('Network error');
  });
});