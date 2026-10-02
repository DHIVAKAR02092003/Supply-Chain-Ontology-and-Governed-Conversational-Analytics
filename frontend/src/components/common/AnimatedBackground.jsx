import './AnimatedBackground.css';

export default function AnimatedBackground() {
  return (
    <div className="animated-factory-bg">
      <svg className="factory-grid" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice">
        {/* Static Background Grid (Optional, but adds factory floor vibe) */}
        <pattern id="floor-grid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M 40 0 L 0 0 0 40" fill="none" className="floor-grid-line" />
        </pattern>
        <rect width="100%" height="100%" fill="url(#floor-grid)" />

        {/* Conveyor Belts / Tracks - Kept strictly to the edges */}
        <g className="tracks">
          {/* Left Side */}
          <path d="M 50 0 L 50 800" className="track" />
          <path d="M 150 0 L 150 800" className="track" />
          <path d="M 250 0 L 250 800" className="track" />
          <path d="M 0 280 L 300 280" className="track" />
          <path d="M 0 400 L 250 400" className="track" />
          <path d="M 0 600 L 300 600" className="track" />
          
          {/* Right Side */}
          <path d="M 950 0 L 950 800" className="track" />
          <path d="M 1050 0 L 1050 800" className="track" />
          <path d="M 1150 0 L 1150 800" className="track" />
          <path d="M 900 280 L 1200 280" className="track" />
          <path d="M 950 400 L 1200 400" className="track" />
          <path d="M 900 600 L 1200 600" className="track" />
        </g>
        
        {/* Moving items on the belts (Data/Materials) */}
        <g className="items">
          {/* Left flowing items */}
          <rect width="16" height="24" rx="4" className="item"><animateMotion dur="8s" repeatCount="indefinite" path="M 150 0 L 150 800" /></rect>
          <rect width="16" height="24" rx="4" className="item"><animateMotion dur="6s" repeatCount="indefinite" path="M 50 800 L 50 0" /></rect>
          <rect width="16" height="24" rx="4" className="item"><animateMotion dur="9s" repeatCount="indefinite" path="M 250 0 L 250 800" /></rect>
          
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="6s" repeatCount="indefinite" path="M 0 280 L 300 280" /></rect>
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="5s" repeatCount="indefinite" path="M 300 280 L 0 280" begin="2s" /></rect>
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="7s" repeatCount="indefinite" path="M 0 400 L 250 400" /></rect>
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="7s" repeatCount="indefinite" path="M 300 600 L 0 600" /></rect>
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="6s" repeatCount="indefinite" path="M 0 600 L 300 600" begin="3s" /></rect>

          {/* Right flowing items */}
          <rect width="16" height="24" rx="4" className="item"><animateMotion dur="11s" repeatCount="indefinite" path="M 1050 800 L 1050 0" /></rect>
          <rect width="16" height="24" rx="4" className="item"><animateMotion dur="7s" repeatCount="indefinite" path="M 950 0 L 950 800" /></rect>
          <rect width="16" height="24" rx="4" className="item"><animateMotion dur="9s" repeatCount="indefinite" path="M 1150 800 L 1150 0" /></rect>

          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="7s" repeatCount="indefinite" path="M 1200 280 L 900 280" /></rect>
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="8s" repeatCount="indefinite" path="M 900 280 L 1200 280" begin="1s" /></rect>
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="6s" repeatCount="indefinite" path="M 1200 400 L 950 400" /></rect>
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="6s" repeatCount="indefinite" path="M 900 600 L 1200 600" /></rect>
          <rect width="24" height="16" rx="4" className="item"><animateMotion dur="7s" repeatCount="indefinite" path="M 1200 600 L 900 600" begin="2s" /></rect>
        </g>
        
        {/* Machine Hubs / Processors - Kept strictly to the edges */}
        <g className="machines">
          {/* Left Hubs */}
          <rect x="100" y="230" width="100" height="100" rx="12" className="machine" />
          <rect x="100" y="550" width="100" height="100" rx="12" className="machine" />
          <circle cx="250" cy="400" r="16" className="machine-center" />
          
          <circle cx="150" cy="280" r="24" className="machine-gear" />
          <circle cx="150" cy="600" r="24" className="machine-gear" />
          <circle cx="250" cy="400" r="12" className="machine-gear-large" />
          
          {/* Right Hubs */}
          <rect x="1000" y="230" width="100" height="100" rx="12" className="machine" />
          <rect x="1000" y="550" width="100" height="100" rx="12" className="machine" />
          <circle cx="950" cy="400" r="16" className="machine-center" />
          
          <circle cx="1050" cy="280" r="24" className="machine-gear" />
          <circle cx="1050" cy="600" r="24" className="machine-gear" />
          <circle cx="950" cy="400" r="12" className="machine-gear-large" />
        </g>
      </svg>
    </div>
  );
}
