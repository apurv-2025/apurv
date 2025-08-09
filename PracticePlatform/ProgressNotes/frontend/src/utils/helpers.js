export const calculateAge = (dateOfBirth) => {
  const today = new Date();
  const birth = new Date(dateOfBirth);
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return age;
};

export const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString();
};

export const formatDateForInput = (dateString) => {
  return new Date(dateString).toISOString().slice(0, 16);
};
