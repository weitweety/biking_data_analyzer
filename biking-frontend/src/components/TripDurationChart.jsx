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
    return <div style={{ color: '#ffffff', padding: '20px' }}>Loading trip duration statistics...</div>;
  }

  if (error) {
    return <div style={{ color: 'red', padding: '20px' }}>Error: {error}</div>;
  }

  if (!data || data.length === 0) {
    return <div style={{ color: '#ffffff', padding: '20px' }}>No data available</div>;
  }

  return (
    <div style={{ width: '100%', height: '500px', padding: '20px', backgroundColor: '#000000', boxSizing: 'border-box' }}>
      <h2 style={{ color: '#ffffff' }}>Trip Duration Statistics</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 30,
            right: 30,
            left: 30,
            bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#333333" />
          <XAxis 
            dataKey="hour" 
            label={{ value: 'Hours', position: 'insideBottom', offset: -20 }}
            stroke="#ffffff"
            tick={{ fill: '#ffffff' }}
          />
          <YAxis 
            label={{ value: 'Count', angle: -90, position: 'insideLeft', offset: -20 }}
            stroke="#ffffff"
            tick={{ fill: '#ffffff' }}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333333', color: '#ffffff' }}
          />
          <Legend 
            wrapperStyle={{ color: '#ffffff' }} 
            verticalAlign="top"
            align="right"
          />
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

