import React from 'react';
import { User, Calendar, Phone, Mail, Edit } from 'lucide-react';
import { calculateAge } from '../../utils/helpers';

const PatientCard = ({ patient, onSelect, onEdit }) => {
  return (
    <div
      className="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
      onClick={() => onSelect(patient)}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                <User className="h-5 w-5 text-blue-600" />
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2">
                <h3 className="text-lg font-medium text-gray-900 truncate">
                  {patient.first_name} {patient.last_name}
                </h3>
                <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">
                  MRN: {patient.medical_record_number}
                </span>
              </div>
              <div className="flex items-center space-x-4 mt-1 text-sm text-gray-600">
                <div className="flex items-center">
                  <Calendar className="h-4 w-4 mr-1" />
                  Age: {calculateAge(patient.date_of_birth)}
                </div>
                {patient.phone && (
                  <div className="flex items-center">
                    <Phone className="h-4 w-4 mr-1" />
                    {patient.phone}
                  </div>
                )}
                {patient.email && (
                  <div className="flex items-center">
                    <Mail className="h-4 w-4 mr-1" />
                    {patient.email}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onEdit(patient);
            }}
            className="p-2 text-gray-400 hover:text-gray-600"
          >
            <Edit className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PatientCard;
