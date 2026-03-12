import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/App.css';

const ViewTotal = () => {
  const location = useLocation();
  const sortedStores = location.state?.sortedStores || [];
  const navigate = useNavigate();
  const openStoreDetails = (store) => {
    if (!store.items || store.items.length === 0) return;
    navigate('/breakdown', { state: { store } });
  };

  // No store has all items
  if (!sortedStores || sortedStores.length === 0) {
    return (
      <div className="total-page">
        <div className="total-empty-card">
          <h2>No single store has all your items right now</h2>
          <p className="lead">Try removing a few items from your list and calculate again!</p>
          <button 
            className="total-back-btn"
            onClick={() => window.history.back()}
          >
            Back to List
          </button>
        </div>
      </div>
    );
  }

  const cheapest = sortedStores[0];

  return (
    <div className="view-total-page">
      <h1 className="best-deal-title text-center mb-5">Best Deal Found!</h1>

      {/* Winner Card */}
      <div className="card mx-auto shadow-lg border-success best-deal-card" style={{ maxWidth: '600px' }} onClick={() => openStoreDetails(cheapest)}>
        <div className="card-header best-deal-header">
          <h5>Cheapest store with <strong>ALL</strong> your items</h5>
          <h2 className="mb-0">{cheapest.store}</h2>
          <p className="best-deal-address">{cheapest.address}</p>
        </div>
        <div className="card-body best-deal-body">
          <h1 className="best-deal-price">
            ${Number(cheapest.total_price).toFixed(2)}
          </h1>
        </div>
      </div>

      {/* Other stores */}
      {sortedStores.length > 1 && (
        <>
          <h4 className="mt-5 mb-4 text-center other-stores-title">Other stores that also have everything:</h4>
          <div className="row justify-content-center other-stores-list">
            {sortedStores.slice(1).map((store, index) => (
              <div key={index} className="col-md-4 mb-3 other-store-col">
                <div className="card h-100 text-center other-store-card" onClick={() => openStoreDetails(store)}>
                  <div className="card-body">
                    <h5 className="other-store-name">{store.store}</h5>
                    <p className="text-muted small other-store-address">{store.address}</p>
                    <h4 className="other-store-price">
                      ${Number(store.total_price).toFixed(2)}
                    </h4>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      <div className="text-center mt-5">
        <button 
          className="total-back-btn"
          onClick={() => window.history.back()}
        >
          Back to List
        </button>
      </div>
    </div>
  );
};

export default ViewTotal;