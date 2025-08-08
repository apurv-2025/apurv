import React, { useState } from 'react';
import { Calendar as BigCalendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { Calendar, Clock, MapPin } from 'lucide-react';
import AppointmentModal from '../Modals/AppointmentModal';

const localizer = momentLocalizer(moment);

const CalendarComponent = ({ 
  events, 
  loading, 
  onSelectEvent, 
  onSelectSlot,
  practitioners,
  patients,
  appointmentTypes 
}) => {
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState(null);

  const handleSelectEvent = (event) => {
    setSelectedEvent(event);
    setIsModalOpen(true);
    if (onSelectEvent) {
      onSelectEvent(event);
    }
  };

  const handleSelectSlot = (slotInfo) => {
    setSelectedSlot(slotInfo);
    setIsModalOpen(true);
    if (onSelectSlot) {
      onSelectSlot(slotInfo);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedEvent(null);
    setSelectedSlot(null);
  };

  const eventStyleGetter = (event) => {
    const backgroundColor = event.resource?.color || '#3498db';
    const style = {
      backgroundColor,
      borderRadius: '4px',
      opacity: 0.8,
      color: 'white',
      border: '0px',
      display: 'block',
      padding: '2px 4px'
    };
    return { style };
  };

  const CustomEvent = ({ event }) => (
    <div className="flex flex-col text-xs">
      <div className="font-semibold truncate">{event.title}</div>
      <div className="flex items-center gap-1 text-xs opacity-90">
        <Clock className="w-3 h-3" />
        <span>
          {moment(event.start).format('HH:mm')} - {moment(event.end).format('HH:mm')}
        </span>
      </div>
      {event.resource?.patient_name && (
        <div className="text-xs opacity-90">
          <span className="font-medium">Person:</span> {event.resource.patient_name}
        </div>
      )}
      {event.resource?.practitioner_name && (
        <div className="text-xs opacity-90">
          <span className="font-medium">Dr:</span> {event.resource.practitioner_name}
        </div>
      )}
      {event.resource?.location && (
        <div className="flex items-center gap-1 text-xs opacity-90">
          <MapPin className="w-3 h-3" />
          <span className="truncate">{event.resource.location}</span>
        </div>
      )}
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="spinner w-8 h-8 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading calendar...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full">
      <div className="bg-white rounded-lg shadow-soft p-6">
        <div className="mb-4">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Appointment Calendar</h2>
          <p className="text-gray-600">View and manage appointments</p>
        </div>

        <div className="h-[600px]">
          <BigCalendar
            localizer={localizer}
            events={events}
            startAccessor="start"
            endAccessor="end"
            style={{ height: '100%' }}
            onSelectEvent={handleSelectEvent}
            onSelectSlot={handleSelectSlot}
            selectable
            eventPropGetter={eventStyleGetter}
            components={{
              event: CustomEvent
            }}
            views={['month', 'week', 'day', 'agenda']}
            defaultView="week"
            step={60}
            timeslots={1}
            min={moment().hour(8).minute(0).toDate()}
            max={moment().hour(18).minute(0).toDate()}
            tooltipAccessor={(event) => `
              ${event.title}
              ${event.resource?.patient_name ? `\nPerson: ${event.resource.patient_name}` : ''}
              ${event.resource?.patient_phone ? `\nPhone: ${event.resource.patient_phone}` : ''}
              ${event.resource?.practitioner_name ? `\nPractitioner: ${event.resource.practitioner_name}` : ''}
              ${event.resource?.location ? `\nLocation: ${event.resource.location}` : ''}
              ${event.resource?.duration_minutes ? `\nDuration: ${event.resource.duration_minutes} min` : ''}
              ${event.resource?.billing_type ? `\nBilling: ${event.resource.billing_type}` : ''}
              ${event.resource?.notes ? `\nNotes: ${event.resource.notes}` : ''}
            `}
          />
        </div>

        {/* Legend */}
        <div className="mt-4 flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">Legend:</span>
          </div>
          {appointmentTypes?.map((type) => (
            <div key={type.id} className="flex items-center gap-2">
              <div 
                className="w-3 h-3 rounded"
                style={{ backgroundColor: type.color }}
              ></div>
              <span className="text-sm text-gray-600">{type.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Appointment Modal */}
      {isModalOpen && (
        <AppointmentModal
          isOpen={isModalOpen}
          onClose={handleCloseModal}
          event={selectedEvent}
          slot={selectedSlot}
          practitioners={practitioners}
          appointmentTypes={appointmentTypes}
        />
      )}
    </div>
  );
};

export default CalendarComponent; 