// src/components/ui/Alert.jsx
import React from 'react';
import { cn } from '../../utils/helpers';
import { 
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  InformationCircleIcon,
  XCircleIcon 
} from '@heroicons/react/20/solid';

const Alert = React.forwardRef(({ className, variant = 'default', ...props }, ref) => {
  return (
    <div
      ref={ref}
      role="alert"
      className={cn(
        "relative w-full rounded-lg border p-4",
        {
          'bg-white border-gray-200': variant === 'default',
          'bg-red-50 border-red-200 text-red-800': variant === 'destructive',
          'bg-yellow-50 border-yellow-200 text-yellow-800': variant === 'warning',
          'bg-green-50 border-green-200 text-green-800': variant === 'success',
          'bg-blue-50 border-blue-200 text-blue-800': variant === 'info'
        },
        className
      )}
      {...props}
    />
  );
});
Alert.displayName = "Alert";

const AlertDescription = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-sm [&_p]:leading-relaxed", className)}
    {...props}
  />
));
AlertDescription.displayName = "AlertDescription";

const AlertTitle = React.forwardRef(({ className, ...props }, ref) => (
  <h5
    ref={ref}
    className={cn("mb-1 font-medium leading-none tracking-tight", className)}
    {...props}
  />
));
AlertTitle.displayName = "AlertTitle";

export { Alert, AlertTitle, AlertDescription };
