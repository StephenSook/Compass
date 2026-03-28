export default function DanceText({ text, className = '' }) {
  return (
    <>
      <style>
        {`
          @keyframes compass-dance {
            0%, 100% {
              opacity: 1;
              transform: translate(-50%, -50%) scale(1) rotate(0deg);
              text-shadow: 0 0 10px rgba(27, 138, 74, 0.8), 0 0 20px rgba(117, 195, 143, 0.6);
            }
            25% {
              opacity: 0.7;
              transform: translate(-50%, -50%) scale(1.05) rotate(2deg);
              text-shadow: 0 0 15px rgba(27, 138, 74, 0.9), 0 0 25px rgba(117, 195, 143, 0.7);
            }
            50% {
              opacity: 0.9;
              transform: translate(-50%, -50%) scale(0.95) rotate(-2deg);
              text-shadow: 0 0 8px rgba(27, 138, 74, 0.7), 0 0 15px rgba(117, 195, 143, 0.5);
            }
            75% {
              opacity: 0.8;
              transform: translate(-50%, -50%) scale(1.05) rotate(1deg);
              text-shadow: 0 0 12px rgba(27, 138, 74, 0.8), 0 0 22px rgba(117, 195, 143, 0.6);
            }
          }

          .dance-container {
            position: relative;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            pointer-events: none;
          }

          .dance-layer {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-weight: 600;
            mix-blend-mode: screen;
            animation: compass-dance 2s infinite;
            white-space: nowrap;
            will-change: transform, opacity;
          }

          .dance-layer-1 {
            color: #1B8A4A;
            animation-delay: 0s;
            z-index: 1;
          }

          .dance-layer-2 {
            color: #47AF6A;
            animation-delay: 0.3s;
            animation-duration: 2.2s;
            z-index: 2;
          }

          .dance-layer-3 {
            color: #75C38F;
            animation-delay: 0.6s;
            animation-duration: 2.4s;
            z-index: 3;
          }
        `}
      </style>

      <div className={`dance-container ${className}`}>
        <div className="dance-layer dance-layer-1">{text}</div>
        <div className="dance-layer dance-layer-2">{text}</div>
        <div className="dance-layer dance-layer-3">{text}</div>
      </div>
    </>
  )
}
