import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/items');
        setItems(response.data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching items');
        setLoading(false);
      }
    };

    fetchItems();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="App">
      <header className="App-header">
        <h1>FastAPI + React App</h1>
      </header>
      <main>
        <h2>Items from API:</h2>
        <ul className="items-list">
          {items.map(item => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      </main>
    </div>
  );
}

export default App;