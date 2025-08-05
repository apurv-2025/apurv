 // hooks/useNotificationPreferences.js
 import { useState, useEffect, useCallback } from 'react';
  
 export const useNotificationPreferences = () => {
   const [preferences, setPreferences] = useState({
     email: true,
     push: true,
     sms: false,
     weeklyDigest: true,
   });
   const [loading, setLoading] = useState(true);
   const [error, setError] = useState(null);
   const [saving, setSaving] = useState(false);
 
   // Fetch preferences
   const fetchPreferences = useCallback(async () => {
     try {
       setLoading(true);
       setError(null);
       const data = await notificationService.getPreferences();
       setPreferences(data);
     } catch (err) {
       setError(err.message);
       console.error('Failed to fetch preferences:', err);
     } finally {
       setLoading(false);
     }
   }, []);
 
   // Update preferences
   const updatePreferences = useCallback(async (newPreferences) => {
     try {
       setSaving(true);
       setError(null);
       const updatedPrefs = { ...preferences, ...newPreferences };
       await notificationService.updatePreferences(updatedPrefs);
       setPreferences(updatedPrefs);
     } catch (err) {
       setError(err.message);
       console.error('Failed to update preferences:', err);
     } finally {
       setSaving(false);
     }
   }, [preferences]);
 
   // Toggle a specific preference
   const togglePreference = useCallback((key) => {
     const newValue = !preferences[key];
     updatePreferences({ [key]: newValue });
   }, [preferences, updatePreferences]);
 
   // Initial fetch
   useEffect(() => {
     fetchPreferences();
   }, [fetchPreferences]);
 
   return {
     preferences,
     loading,
     error,
     saving,
     updatePreferences,
     togglePreference,
     refresh: fetchPreferences,
   };
 };