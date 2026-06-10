import { useState } from 'react';
import { MarketCheckFilters } from '../services/api';

interface FilterPanelProps {
  onFilterChange: (filters: MarketCheckFilters) => void;
  onClearFilters: () => void;
}

export function FilterPanel({ onFilterChange, onClearFilters }: FilterPanelProps) {
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [priceMin, setPriceMin] = useState('');
  const [priceMax, setPriceMax] = useState('');
  const [mileageMax, setMileageMax] = useState('');
  const [zip, setZip] = useState('');
  const [radius, setRadius] = useState('100');
  const [carType, setCarType] = useState('used');

  const handleClear = () => {
    setMake(''); setModel(''); setYear('');
    setPriceMin(''); setPriceMax(''); setMileageMax('');
    setZip(''); setRadius('100'); setCarType('used');
    onClearFilters();
  };

  return (
    <div className="sidebar">
      <div className="filter-section">
        <h3>🔍 Search</h3>
        <div className="filter-group">
          <label>Make</label>
          <input type="text" placeholder="e.g., BMW" value={make}
            onChange={(e) => { setMake(e.target.value); onFilterChange({ make: e.target.value || undefined }); }} />
        </div>
        <div className="filter-group">
          <label>Model</label>
          <input type="text" placeholder="e.g., 3 Series" value={model}
            onChange={(e) => { setModel(e.target.value); onFilterChange({ model: e.target.value || undefined }); }} />
        </div>
        <div className="filter-group">
          <label>Year</label>
          <input type="number" placeholder="e.g., 2022" value={year}
            onChange={(e) => { setYear(e.target.value); onFilterChange({ year: e.target.value ? parseInt(e.target.value) : undefined }); }} />
        </div>
        <div className="filter-group">
          <label>Inventory Type</label>
          <select value={carType} onChange={(e) => { setCarType(e.target.value); onFilterChange({ car_type: e.target.value }); }}>
            <option value="used">Used</option>
            <option value="new">New</option>
            <option value="certified">Certified</option>
          </select>
        </div>
      </div>

      <div className="filter-section">
        <h3>📍 Location</h3>
        <div className="filter-group">
          <label>Zip Code</label>
          <input type="text" placeholder="e.g., 94102" value={zip}
            onChange={(e) => { setZip(e.target.value); onFilterChange({ zip: e.target.value || undefined }); }} />
        </div>
        <div className="filter-group">
          <label>Radius (miles)</label>
          <input type="number" placeholder="100" value={radius}
            onChange={(e) => { setRadius(e.target.value); onFilterChange({ radius: e.target.value ? parseInt(e.target.value) : undefined }); }} />
        </div>
      </div>

      <div className="filter-section">
        <h3>💰 Price</h3>
        <div className="filter-group">
          <label>Min Price ($)</label>
          <input type="number" placeholder="Min" value={priceMin}
            onChange={(e) => { setPriceMin(e.target.value); onFilterChange({ price_min: e.target.value ? parseInt(e.target.value) : undefined }); }} />
        </div>
        <div className="filter-group">
          <label>Max Price ($)</label>
          <input type="number" placeholder="Max" value={priceMax}
            onChange={(e) => { setPriceMax(e.target.value); onFilterChange({ price_max: e.target.value ? parseInt(e.target.value) : undefined }); }} />
        </div>
      </div>

      <div className="filter-section">
        <h3>🔧 Mileage</h3>
        <div className="filter-group">
          <label>Max Mileage</label>
          <input type="number" placeholder="e.g., 50000" value={mileageMax}
            onChange={(e) => { setMileageMax(e.target.value); onFilterChange({ mileage_max: e.target.value ? parseInt(e.target.value) : undefined }); }} />
        </div>
      </div>

      <button className="button button-secondary" onClick={handleClear}>Clear Filters</button>
    </div>
  );
}
