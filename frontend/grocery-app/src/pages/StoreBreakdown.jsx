import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/App.css';

const StoreBreakdown = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const store = location.state?.store;

  // If user hits /breakdown directly with no state
  if (!store) {
    return (
      <div className="view-total-page">
        <h2 className="best-deal-title text-center mb-4">
          No store selected
        </h2>
        <div className="text-center">
          <button
            className="total-back-btn"
            onClick={() => navigate(-1)}
          >
            Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="view-total-page">
      <h1 className="best-deal-title text-center mb-4">
        Price Breakdown
      </h1>

      <div className="store-breakdown-card-full">
        <h2 className="store-breakdown-title">{store.store}</h2>
        <p className="store-breakdown-address">{store.address}</p>
        <p className="store-breakdown-total">
          Total: ${Number(store.total_price).toFixed(2)}
        </p>

        <div className="store-breakdown-table">
          <div className="sbt-head">
            <span>Item</span>
            <span>Price</span>
            <span>Availability</span>
          </div>

          {store.items?.map((item, idx) => (
            <div key={idx} className="sbt-row">
              <span>{item.item_name}</span>
              <span>${item.price.toFixed(2)}</span>
              <span>{item.availability_display}</span>
            </div>
          ))}
        </div>

        <div className="text-center mt-4">
          <button
            className="total-back-btn"
            onClick={() => navigate(-1)}
          >
            Back to Best Deals
          </button>
        </div>
      </div>
    </div>
  );
};

export default StoreBreakdown;
