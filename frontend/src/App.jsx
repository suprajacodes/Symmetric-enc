import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  // const [apiKey, setApiKey] = useState('');
  const [encryptedData, setEncryptedData] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Sending request to backend with text:', text);
    try {
      const response = await axios.post('http://localhost:5000/encrypt', { text });
      console.log('Received response from backend:', response.data);
      if (response.data.error) {
        setError(response.data.error);
        setEncryptedData(null);
      } else {
        setEncryptedData(response.data);
        setError(null);
      }
    } catch (error) {
      console.error('Error encrypting data:', error);
      setError('Failed to encrypt data. Please check your API key and try again.');
      setEncryptedData(null);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Encrypt a String</h1>
      </header>
      <div className="container">
        <form onSubmit={handleSubmit}>
          {/* <input 
            type="text" 
            value={apiKey} 
            onChange={(e) => setApiKey(e.target.value)} 
            placeholder="Enter API key" 
          /> */}
          <input 
            type="text" 
            value={text} 
            onChange={(e) => setText(e.target.value)} 
            placeholder="Enter text to encrypt" 
          />
          <button type="submit">Encrypt</button>
        </form>
        {error && (
          <div className="error">
            <p>{error}</p>
          </div>
        )}
        {encryptedData && (
          <div className="result">
            <h2>Encrypted Data</h2>
            <p><strong>Cipher:</strong> {encryptedData.cipher}</p>
            <p><strong>IV:</strong> {encryptedData.iv}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
