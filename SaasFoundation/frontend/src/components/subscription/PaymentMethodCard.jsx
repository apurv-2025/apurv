// src/components/subscription/PaymentMethodCard.jsx
import React, { useState } from 'react';
import { 
  CreditCardIcon, 
  EllipsisVerticalIcon,
  CheckIcon 
} from '@heroicons/react/24/outline';
import { Card, CardContent } from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import Modal, { ConfirmModal } from '../ui/Modal';
import { cn } from '../../utils/helpers';

const PaymentMethodCard = ({ 
  paymentMethod, 
  onSetDefault, 
  onEdit, 
  onRemove,
  loading = false,
  className 
}) => {
  const [showMenu, setShowMenu] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [actionLoading, setActionLoading] = useState('');

  const {
    id,
    type = 'card',
    brand,
    last_four,
    exp_month,
    exp_year,
    is_default,
    cardholder_name,
    billing_address,
    created_at
  } = paymentMethod;

  // Get card brand styling
  const getCardBrandInfo = (brand) => {
    const brandLower = brand?.toLowerCase();
    
    switch (brandLower) {
      case 'visa':
        return {
          name: 'Visa',
          color: 'bg-blue-600',
          textColor: 'text-white'
        };
      case 'mastercard':
        return {
          name: 'Mastercard',
          color: 'bg-red-600',
          textColor: 'text-white'
        };
      case 'american_express':
      case 'amex':
        return {
          name: 'Amex',
          color: 'bg-green-600',
          textColor: 'text-white'
        };
      case 'discover':
        return {
          name: 'Discover',
          color: 'bg-orange-600',
          textColor: 'text-white'
        };
      default:
        return {
          name: brand?.toUpperCase() || 'CARD',
          color: 'bg-gray-600',
          textColor: 'text-white'
        };
    }
  };

  const brandInfo = getCardBrandInfo(brand);

  const handleSetDefault = async () => {
    if (is_default) return;
    
    setActionLoading('default');
    try {
      await onSetDefault?.(id);
    } catch (error) {
      console.error('Failed to set default:', error);
    } finally {
      setActionLoading('');
    }
  };

  const handleEdit = async () => {
    setActionLoading('edit');
    try {
      await onEdit?.(id);
    } catch (error) {
      console.error('Failed to edit:', error);
    } finally {
      setActionLoading('');
    }
  };

  const handleRemove = async () => {
    setActionLoading('remove');
    try {
      await onRemove?.(id);
      setShowDeleteModal(false);
    } catch (error) {
      console.error('Failed to remove:', error);
    } finally {
      setActionLoading('');
    }
  };

  const formatExpiryDate = () => {
    return `${String(exp_month).padStart(2, '0')}/${String(exp_year).slice(-2)}`;
  };

  const formatCardNumber = () => {
    return `•••• •••• •••• ${last_four}`;
  };

  return (
    <>
      <Card className={cn("relative transition-all duration-200 hover:shadow-md", className)}>
        <CardContent className="pt-6">
          <div className="flex items-start justify-between">
            {/* Card Info */}
            <div className="flex items-start space-x-4">
              {/* Card Icon/Brand */}
              <div className={cn(
                "w-16 h-10 rounded-md flex items-center justify-center text-xs font-bold",
                brandInfo.color,
                brandInfo.textColor
              )}>
                {type === 'card' ? brandInfo.name : 'BANK'}
              </div>

              {/* Card Details */}
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-1">
                  <h3 className="font-semibold text-gray-900">
                    {formatCardNumber()}
                  </h3>
                  {is_default && (
                    <Badge variant="success" className="text-xs">
                      <CheckIcon className="h-3 w-3 mr-1" />
                      Default
                    </Badge>
                  )}
                </div>

                <div className="space-y-1 text-sm text-gray-600">
                  {cardholder_name && (
                    <p className="font-medium">{cardholder_name}</p>
                  )}
                  <p>Expires {formatExpiryDate()}</p>
                  {billing_address?.country && (
                    <p>{billing_address.country}</p>
                  )}
                  <p className="text-xs text-gray-500">
                    Added {new Date(created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>

            {/* Actions Menu */}
            <div className="relative">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowMenu(!showMenu)}
                className="p-2"
              >
                <EllipsisVerticalIcon className="h-4 w-4" />
              </Button>

              {showMenu && (
                <div className="absolute right-0 top-8 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-10">
                  <div className="py-1">
                    {!is_default && (
                      <button
                        onClick={handleSetDefault}
                        disabled={actionLoading === 'default'}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50"
                      >
                        {actionLoading === 'default' ? 'Setting...' : 'Set as Default'}
                      </button>
                    )}
                    
                    <button
                      onClick={handleEdit}
                      disabled={actionLoading === 'edit'}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50"
                    >
                      {actionLoading === 'edit' ? 'Loading...' : 'Edit Details'}
                    </button>
                    
                    <button
                      onClick={() => {
                        setShowDeleteModal(true);
                        setShowMenu(false);
                      }}
                      disabled={is_default || actionLoading === 'remove'}
                      className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 disabled:opacity-50 disabled:text-gray-400"
                    >
                      {actionLoading === 'remove' ? 'Removing...' : 'Remove Card'}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Quick Actions (Alternative to menu) */}
          <div className="mt-4 flex space-x-2">
            {!is_default && (
              <Button
                variant="secondary"
                size="sm"
                onClick={handleSetDefault}
                disabled={loading || actionLoading === 'default'}
                loading={actionLoading === 'default'}
              >
                Set Default
              </Button>
            )}
            
            <Button
              variant="secondary"
              size="sm"
              onClick={handleEdit}
              disabled={loading || actionLoading === 'edit'}
              loading={actionLoading === 'edit'}
            >
              Edit
            </Button>
            
            {!is_default && (
              <Button
                variant="danger"
                size="sm"
                onClick={() => setShowDeleteModal(true)}
                disabled={loading || actionLoading === 'remove'}
              >
                Remove
              </Button>
            )}
          </div>

          {/* Default card notice */}
          {is_default && (
            <div className="mt-3 p-2 bg-green-50 border border-green-200 rounded-md">
              <p className="text-xs text-green-800">
                This is your default payment method for all subscriptions and purchases.
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleRemove}
        title="Remove Payment Method"
        message={`Are you sure you want to remove the ${brand} card ending in ${last_four}? This action cannot be undone.`}
        confirmText="Remove Card"
        cancelText="Keep Card"
        variant="danger"
        loading={actionLoading === 'remove'}
      />

      {/* Click outside handler for menu */}
      {showMenu && (
        <div
          className="fixed inset-0 z-0"
          onClick={() => setShowMenu(false)}
        />
      )}
    </>
  );
};

// Payment Method List Component
const PaymentMethodList = ({ 
  paymentMethods = [], 
  onSetDefault, 
  onEdit, 
  onRemove,
  onAddNew,
  loading = false 
}) => {
  if (paymentMethods.length === 0) {
    return (
      <div className="text-center py-8">
        <CreditCardIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No payment methods</h3>
        <p className="mt-1 text-sm text-gray-500">
          Add a payment method to get started.
        </p>
        <div className="mt-6">
          <Button onClick={onAddNew}>
            Add Payment Method
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {paymentMethods.map((paymentMethod) => (
        <PaymentMethodCard
          key={paymentMethod.id}
          paymentMethod={paymentMethod}
          onSetDefault={onSetDefault}
          onEdit={onEdit}
          onRemove={onRemove}
          loading={loading}
        />
      ))}
      
      <Card className="border-dashed border-2 border-gray-300 hover:border-gray-400 transition-colors">
        <CardContent className="pt-6">
          <button
            onClick={onAddNew}
            className="w-full flex flex-col items-center justify-center py-6 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <CreditCardIcon className="h-8 w-8 mb-2" />
            <span className="font-medium">Add New Payment Method</span>
            <span className="text-sm text-gray-500 mt-1">
              Credit card, debit card, or bank account
            </span>
          </button>
        </CardContent>
      </Card>
    </div>
  );
};

export default PaymentMethodCard;
export { PaymentMethodList };
