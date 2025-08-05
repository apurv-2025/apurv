// src/components/subscription/InvoiceList.jsx
import React from 'react';
import { Card, CardContent } from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { formatCurrency, formatDate } from '../../utils/formatters';

const InvoiceList = ({ invoices, onPayInvoice }) => {
  if (!invoices?.length) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No invoices found.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {invoices.map((invoice) => (
        <Card key={invoice.id}>
          <CardContent className="pt-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h4 className="text-lg font-semibold text-gray-900">
                  {formatCurrency(invoice.total_amount)}
                </h4>
                <p className="text-sm text-gray-600">Invoice #{invoice.id}</p>
              </div>
              <Badge variant={invoice.status === 'paid' ? 'success' : 'warning'}>
                {invoice.status.toUpperCase()}
              </Badge>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Amount:</span>
                <p className="font-medium">{formatCurrency(invoice.amount)}</p>
              </div>
              <div>
                <span className="text-gray-600">Tax:</span>
                <p className="font-medium">{formatCurrency(invoice.tax_amount)}</p>
              </div>
              <div>
                <span className="text-gray-600">Due Date:</span>
                <p className="font-medium">{formatDate(invoice.due_date)}</p>
              </div>
              {invoice.paid_at && (
                <div>
                  <span className="text-gray-600">Paid:</span>
                  <p className="font-medium">{formatDate(invoice.paid_at)}</p>
                </div>
              )}
            </div>
            
            {invoice.status === 'pending' && onPayInvoice && (
              <div className="mt-4">
                <Button 
                  onClick={() => onPayInvoice(invoice.id)}
                  size="sm"
                >
                  Pay Now
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default InvoiceList;
