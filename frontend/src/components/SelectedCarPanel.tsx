import { Car } from '../services/api';

interface SelectedCarPanelProps {
  car: Car;
  isSaved: boolean;
  onSave: (carId: number | string) => void;
  onClose: () => void;
}

export function SelectedCarPanel({ car, isSaved, onSave, onClose }: SelectedCarPanelProps) {
  return (
    <div style={{
      background: '#fff',
      border: '2px solid #3498db',
      borderRadius: '8px',
      padding: '1.2rem',
      marginBottom: '1rem',
      boxShadow: '0 4px 12px rgba(52, 152, 219, 0.15)',
      position: 'relative',
    }}>
      {/* Header row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.8rem' }}>
        <div>
          <span style={{
            fontSize: '0.7rem', fontWeight: 700, letterSpacing: '0.05em',
            background: '#3498db', color: '#fff',
            padding: '2px 8px', borderRadius: '3px', marginRight: '0.5rem',
          }}>
            NOW VIEWING
          </span>
          {car.source === 'marketcheck' && (
            <span style={{
              fontSize: '0.7rem', fontWeight: 700,
              background: '#2c3e50', color: '#fff',
              padding: '2px 6px', borderRadius: '3px',
            }}>
              LIVE
            </span>
          )}
        </div>
        <button
          onClick={onClose}
          style={{
            background: 'none', border: 'none', cursor: 'pointer',
            fontSize: '1.1rem', color: '#aaa', lineHeight: 1, padding: '0 4px',
          }}
          title="Dismiss"
        >
          ×
        </button>
      </div>

      {/* Main content */}
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        {/* Image */}
        <div style={{ flexShrink: 0 }}>
          <img
            src={car.image_url || ''}
            alt={`${car.make} ${car.model}`}
            style={{ width: '140px', height: '100px', objectFit: 'cover', borderRadius: '6px', background: '#ecf0f1' }}
            onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
          />
        </div>

        {/* Details */}
        <div style={{ flex: 1, minWidth: '180px' }}>
          <div style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '0.3rem' }}>
            {car.year} {car.make} {car.model}{car.trim ? ` ${car.trim}` : ''}
          </div>
          <div style={{ fontSize: '1.2rem', color: '#27ae60', fontWeight: 700, marginBottom: '0.5rem' }}>
            {car.price > 0 ? `$${car.price.toLocaleString()}` : 'Price on request'}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '0.15rem 0.8rem', fontSize: '0.88rem' }}>
            <span style={{ color: '#888' }}>Mileage</span>
            <span>{car.mileage > 0 ? `${car.mileage.toLocaleString()} miles` : 'N/A'}</span>
            <span style={{ color: '#888' }}>Location</span>
            <span>{car.location}</span>
            {car.vin && (
              <>
                <span style={{ color: '#888' }}>VIN</span>
                <span style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{car.vin}</span>
              </>
            )}
            {car.price > 0 && car.mileage > 0 && (
              <>
                <span style={{ color: '#888' }}>$/mile</span>
                <span>${(car.price / car.mileage).toFixed(2)}</span>
              </>
            )}
          </div>

          {car.description && (
            <p style={{ fontSize: '0.82rem', color: '#666', marginTop: '0.5rem', marginBottom: 0 }}>
              {car.description}
            </p>
          )}
        </div>
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.9rem', flexWrap: 'wrap' }}>
        <button
          className={`button button-small ${isSaved ? '' : 'button-secondary'}`}
          onClick={() => onSave(car.id)}
          disabled={isSaved}
        >
          {isSaved ? 'Saved ✓' : 'Save this car'}
        </button>
        {car.listing_url && (
          <a
            href={car.listing_url}
            target="_blank"
            rel="noopener noreferrer"
            className="button button-small"
            style={{ textDecoration: 'none', textAlign: 'center' }}
          >
            View full listing ↗
          </a>
        )}
      </div>
    </div>
  );
}
