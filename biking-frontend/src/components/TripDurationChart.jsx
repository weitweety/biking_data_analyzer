import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getTripDurationStats } from '../api/client';

const TripDurationChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await getTripDurationStats();
        
        // Transform the data to match Recharts format
        // response has { hours: [0, 1, 2, ...], count: [10, 20, 30, ...] }
        const chartData = response.hours.map((hour, index) => ({
          hour: hour,
          count: response.count[index]
        }));
        
        setData(chartData);
        setError(null);
      } catch (err) {
        setError('Failed to load trip duration statistics');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading trip duration statistics...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  if (!data || data.length === 0) {
    return <div>No data available</div>;
  }

  return (
    <div style={{ width: '100%', height: '500px', padding: '20px' }}>
      <h2>Trip Duration Statistics</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="hour" 
            label={{ value: 'Hours', position: 'insideBottom', offset: -5 }}
          />
          <YAxis 
            label={{ value: 'Count', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="count" 
            stroke="#8884d8" 
            strokeWidth={2}
            name="Trip Count"
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TripDurationChart;

