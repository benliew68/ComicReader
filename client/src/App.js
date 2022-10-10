import logo from './logo.svg';
import discord from './discord.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={discord} className="App-icon" alt="logo" />
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Test Link
        </a>
      </header>
    </div>
  );
}
export default App;