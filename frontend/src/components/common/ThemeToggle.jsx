import { useState, useEffect } from 'react';
import { Sun, Moon } from 'lucide-react';
import './ThemeToggle.css';

export default function ThemeToggle() {
  const [isLight, setIsLight] = useState(true);

  useEffect(() => {
    // Check initial preference from localStorage or body class
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsLight(false);
      document.body.classList.remove('light-mode');
    } else {
      setIsLight(true);
      document.body.classList.add('light-mode');
    }
  }, []);

  const toggleTheme = () => {
    setIsLight((prev) => {
      const newLight = !prev;
      if (newLight) {
        document.body.classList.add('light-mode');
        localStorage.setItem('theme', 'light');
      } else {
        document.body.classList.remove('light-mode');
        localStorage.setItem('theme', 'dark');
      }
      return newLight;
    });
  };

  return (
    <div className="theme-toggle" onClick={toggleTheme} title="Toggle theme">
      <div className={`toggle-track ${isLight ? 'light' : 'dark'}`}>
        <div className="toggle-thumb">
          {isLight ? <Sun size={18} color="#f59e0b" /> : <Moon size={18} color="#6366f1" />}
        </div>
        <div className="toggle-icons">
          <Sun size={16} className="icon-sun" />
          <Moon size={16} className="icon-moon" />
        </div>
      </div>
    </div>
  );
}
