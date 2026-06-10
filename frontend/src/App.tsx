import { useState, useEffect, useCallback } from 'react';
import { Car, marketcheckAPI, MarketCheckFilters } from './services/api';
import { CarCard } from './components/CarCard';
import { FilterPanel } from './components/FilterPanel';
import { ChatAssistant } from './components/ChatAssistant';
import { SelectedCarPanel } from './components/SelectedCarPanel';
// import './App.css';

function App() {
  const [listings, setListings] = useState<Car[]>([]);
  const [selectedCar, setSelectedCar] = useState<Car | undefined>();
  const [savedCars, setSavedCars] = useState<Car[]>([]);
  const [filters, setFilters] = useState<MarketCheckFilters>({});
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dataSource, setDataSource] = useState<'live' | 'mock'>('live');

  const fetchCars = useCallback(async (activeFilters: MarketCheckFilters) => {
    setLoading(true);
    setError(null);
    try {
      const res = await marketcheckAPI.search(activeFilters);
      setListings(res.data.listings);
      setTotal(res.data.num_found);
      const source = res.headers['x-data-source'] as string;
      setDataSource(source === 'mock' ? 'mock' : 'live');
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(`Failed to load listings: ${message}`);
      setListings([]);
      setDataSource('live');
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    fetchCars({});
  }, [fetchCars]);

  const handleFilterChange = (newFilters: MarketCheckFilters) => {
    const merged = { ...filters, ...newFilters };
    setFilters(merged);
    fetchCars(merged);
  };

  const handleClearFilters = () => {
    setFilters({});
    fetchCars({});
  };

  const handleSaveCar = (carId: number | string) => {
    const car = listings.find(c => c.id === carId);
    if (car && !savedCars.find(c => c.id === carId)) {
      setSavedCars(prev => [...prev, car]);
    }
  };

  const handleSelectCar = (car: Car) => {
    setSelectedCar(prev => prev?.id === car.id ? undefined : car);
  };

  const handleDeselectCar = () => {
    setSelectedCar(undefined);
  };

  return (
    <div className="app">
      <header className="header">
        {dataSource === 'mock' && (
          <div style={{
            background: 'rgba(255, 193, 7, 0.1)',
            border: '1px solid rgba(255, 193, 7, 0.3)',
            borderRadius: '4px',
            padding: '0.4rem 0.8rem',
            marginBottom: '0.8rem',
            fontSize: '0.8rem',
            color: '#FFA500',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
          }}>
            <span>⚠️</span>
            <span>Using demo data — Marketcheck API unavailable</span>
          </div>
        )}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div>
            <h1>🚗 CarScope</h1>
            <p style={{ fontSize: '0.9rem', opacity: 0.9 }}>Live inventory powered by Marketcheck</p>
          </div>
          {total > 0 && (
            <span style={{ fontSize: '0.85rem', opacity: 0.85, background: 'rgba(255,255,255,0.15)', padding: '0.3rem 0.8rem', borderRadius: '4px' }}>
              {total.toLocaleString()} listings
            </span>
          )}
        </div>
      </header>

      <div className="main-container">
        <FilterPanel
          onFilterChange={handleFilterChange}
          onClearFilters={handleClearFilters}
        />

        <div className="content">
          <div>
            {total > 0 && (
              <p style={{ marginBottom: '1rem', color: '#555', fontSize: '0.9rem' }}>
                Showing {listings.length} of {total.toLocaleString()} listings
              </p>
            )}

            <div className="cars-grid">
              {loading ? (
                <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '2rem' }}>
                  <p>Loading cars...</p>
                </div>
              ) : error ? (
                <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '2rem', color: '#e74c3c' }}>
                  <p>{error}</p>
                </div>
              ) : listings.length === 0 ? (
                <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '2rem' }}>
                  <p>No cars found matching your criteria.</p>
                </div>
              ) : (
                listings.map(car => (
                  <CarCard
                    key={car.id}
                    car={car}
                    onSelect={handleSelectCar}
                    onSave={handleSaveCar}
                    isSelected={selectedCar?.id === car.id}
                    isSaved={savedCars.some(c => c.id === car.id)}
                  />
                ))
              )}
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {selectedCar && (
              <SelectedCarPanel
                car={selectedCar}
                isSaved={savedCars.some(c => c.id === selectedCar.id)}
                onSave={handleSaveCar}
                onClose={handleDeselectCar}
              />
            )}
            <ChatAssistant
              currentCar={selectedCar}
              currentCars={listings}
              savedCars={savedCars}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
