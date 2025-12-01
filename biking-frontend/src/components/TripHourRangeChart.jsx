import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getTripHourRangeStats } from '../api/client';

const TripHourRangeChart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await getTripHourRangeStats();

        const chartData = response.hour_bucket.map((bucket, index) => ({
          hourBucket: `${bucket}:00`,
          count: response.count[index] ?? 0,
        }));

        setData(chartData);
        setError(null);
      } catch (err) {
        console.error(err);
        setError('Failed to load trip hour range statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div style={{ color: '#ffffff', padding: '20px' }}>Loading trip hour range statistics...</div>;
  }

  if (error) {
    return <div style={{ color: 'red', padding: '20px' }}>Error: {error}</div>;
  }

  if (!data || data.length === 0) {
    return <div style={{ color: '#ffffff', padding: '20px' }}>No hour range data available</div>;
  }

  return (
    <div style={{ width: '100%', height: '500px', padding: '20px', backgroundColor: '#000000', boxSizing: 'border-box' }}>
      <h2 style={{ color: '#ffffff' }}>Trips by Hour of Day</h2>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#333333" />
          <XAxis 
            dataKey="hourBucket" 
            label={{ value: 'Hour of Day', position: 'insideBottom', offset: -10 }}
            stroke="#ffffff"
            tick={{ fill: '#ffffff' }}
            interval={0}
          />
          <YAxis 
            label={{ value: 'Trip Count', angle: -90, position: 'insideLeft', offset: -10 }}
            stroke="#ffffff"
            tick={{ fill: '#ffffff' }}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333333', color: '#ffffff' }}
          />
          <Bar dataKey="count" name="Trip Count" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TripHourRangeChart;


