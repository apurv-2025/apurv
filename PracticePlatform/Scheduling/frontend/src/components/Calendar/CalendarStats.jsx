import React from 'react';
import { Users, UserCheck, Calendar, Clock, Activity } from 'lucide-react';

const CalendarStats = ({ appointments, patients, practitioners, selectedDate }) => {
  const today = new Date();
  const isToday = selectedDate.toDateString() === today.toDateString();
  
  // Calculate statistics
  const totalAppointments = appointments.length;
  const todayAppointments = appointments.filter(apt => {
    const aptDate = new Date(apt.start);
    return aptDate.toDateString() === today.toDateString();
  }).length;
  
  const selectedDateAppointments = appointments.filter(apt => {
    const aptDate = new Date(apt.start);
    return aptDate.toDateString() === selectedDate.toDateString();
  }).length;

  const uniquePatients = new Set(appointments.map(apt => apt.resource?.patient_id)).size;
  const uniquePractitioners = new Set(appointments.map(apt => apt.resource?.practitioner_id)).size;

  const upcomingAppointments = appointments.filter(apt => {
    const aptDate = new Date(apt.start);
    return aptDate > today;
  }).length;

  const completedToday = appointments.filter(apt => {
    const aptDate = new Date(apt.start);
    const aptEnd = new Date(apt.end);
    return aptDate.toDateString() === today.toDateString() && aptEnd < today;
  }).length;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-6">
      {/* Total Appointments */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Calendar className="h-5 w-5 text-blue-600" />
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-600">Total Appointments</p>
            <p className="text-lg font-semibold text-gray-900">{totalAppointments}</p>
          </div>
        </div>
      </div>

      {/* Today's Appointments */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center">
          <div className="p-2 bg-green-100 rounded-lg">
            <Clock className="h-5 w-5 text-green-600" />
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-600">Today's Appointments</p>
            <p className="text-lg font-semibold text-gray-900">{todayAppointments}</p>
          </div>
        </div>
      </div>

      {/* Selected Date Appointments */}
      {!isToday && (
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Calendar className="h-5 w-5 text-purple-600" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Selected Date</p>
              <p className="text-lg font-semibold text-gray-900">{selectedDateAppointments}</p>
            </div>
          </div>
        </div>
      )}

      {/* Active Persons */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center">
          <div className="p-2 bg-orange-100 rounded-lg">
            <Users className="h-5 w-5 text-orange-600" />
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-600">Active Persons</p>
            <p className="text-lg font-semibold text-gray-900">{uniquePatients}</p>
          </div>
        </div>
      </div>

      {/* Active Practitioners */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center">
          <div className="p-2 bg-indigo-100 rounded-lg">
            <UserCheck className="h-5 w-5 text-indigo-600" />
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-600">Active Practitioners</p>
            <p className="text-lg font-semibold text-gray-900">{uniquePractitioners}</p>
          </div>
        </div>
      </div>

      {/* Upcoming Appointments */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center">
          <div className="p-2 bg-yellow-100 rounded-lg">
            <Activity className="h-5 w-5 text-yellow-600" />
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-600">Upcoming</p>
            <p className="text-lg font-semibold text-gray-900">{upcomingAppointments}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CalendarStats; 