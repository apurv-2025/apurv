import React from 'react';
import { 
  Heart, 
  Stethoscope, 
  Building, 
  FileText 
} from 'lucide-react';
import { CLAIM_TYPE_CONFIG } from '../../utils/constants';

const ClaimTypeBadge = ({ type }) => {
  const config = CLAIM_TYPE_CONFIG[type] || CLAIM_TYPE_CONFIG.default;
  
  const getIcon = (iconName) => {
    const icons = {
      Heart,
      Stethoscope,
      Building,
      FileText
    };
    return icons[iconName] || FileText;
  };

  const Icon = getIcon(config.icon);

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
      <Icon className="w-3 h-3 mr-1" />
      {config.label}
    </span>
  );
};

export default ClaimTypeBadge;
