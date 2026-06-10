import { Car } from '../services/api';

// Inline SVG fallback — no network request needed
const FALLBACK_IMAGE =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='200' viewBox='0 0 300 200'%3E%3Crect width='300' height='200' fill='%23ecf0f1'/%3E%3Ctext x='50%25' y='45%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='14' fill='%2395a5a6'%3ENo Image%3C/text%3E%3Ctext x='50%25' y='62%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='28' fill='%23bdc3c7'%3E%F0%9F%9A%97%3C/text%3E%3C/svg%3E";

interface CarCardProps {
  car: Car;
  onSelect: (car: Car) => void;
  onSave: (carId: number | string) => void;
  isSelected?: boolean;
  isSaved?: boolean;
}

export function CarCard({ car, onSelect, onSave, isSelected, isSaved }: CarCardProps) {
  const isMarketcheck = car.source === 'marketcheck';

  return (
    <div
      className="car-card"
      style={isSelected ? { outline: '2px solid #3498db', outlineOffset: '2px', boxShadow: '0 0 0 4px rgba(52,152,219,0.15)' } : undefined}
    >
      <div className="car-image" style={{ position: 'relative' }}>
        <img
          src={car.image_url || FALLBACK_IMAGE}
          alt={`${car.make} ${car.model}`}
          onError={(e) => {
            const img = e.target as HTMLImageElement;
            if (img.src !== FALLBACK_IMAGE) img.src = FALLBACK_IMAGE;
          }}
        />
        {isMarketcheck && (
          <span style={{
            position: 'absolute', top: '8px', left: '8px',
            background: '#2c3e50', color: '#fff',
            fontSize: '0.7rem', padding: '2px 6px', borderRadius: '3px', fontWeight: 600,
          }}>
            LIVE
          </span>
        )}
      </div>
      <div className="car-info">
        <div className="car-title">
          {car.year} {car.make} {car.model}{car.trim ? ` ${car.trim}` : ''}
        </div>
        <div className="car-price">
          {car.price > 0 ? `$${car.price.toLocaleString()}` : 'Price on request'}
        </div>
        <div className="car-details">
          {car.mileage > 0 ? `${car.mileage.toLocaleString()} miles` : 'Mileage N/A'}
        </div>
        <div className="car-location">{car.location}</div>
        {car.vin && (
          <div style={{ fontSize: '0.75rem', color: '#999', marginTop: '0.3rem' }}>
            VIN: {car.vin}
          </div>
        )}
        <p style={{ fontSize: '0.85rem', color: '#666', margin: '0.5rem 0 0.8rem' }}>
          {car.description}
        </p>
        <div className="car-actions">
          <button className="button button-small" onClick={() => onSelect(car)}>
            {isSelected ? 'Deselect' : 'View'}
          </button>
          {car.listing_url ? (
            <a
              href={car.listing_url}
              target="_blank"
              rel="noopener noreferrer"
              className="button button-small"
              style={{ textDecoration: 'none', textAlign: 'center' }}
            >
              Listing ↗
            </a>
          ) : null}
          <button
            className={`button button-small ${isSaved ? '' : 'button-secondary'}`}
            onClick={() => onSave(car.id)}
            disabled={isSaved}
          >
            {isSaved ? 'Saved ✓' : 'Save'}
          </button>
        </div>
      </div>
    </div>
  );
}
